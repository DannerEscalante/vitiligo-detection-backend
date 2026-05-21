from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from core.database import SessionLocal
from core.deps import requerir_admin_o_gerente
from models import HistorialClinico, TipoTratamiento, Tratamiento, Usuario

router = APIRouter(prefix="/reportes", tags=["Reportes"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/tratamientos-mas-usados")
def tratamientos_mas_usados(
    usuario: Usuario = Depends(requerir_admin_o_gerente),
    db: Session = Depends(get_db)
):
    resultados = db.query(
        TipoTratamiento.nombre.label("tipo_tratamiento"),
        func.count(Tratamiento.id).label("cantidad")
    ).join(
        Tratamiento,
        Tratamiento.tipo_tratamiento_id == TipoTratamiento.id
    ).group_by(
        TipoTratamiento.nombre
    ).order_by(
        func.count(Tratamiento.id).desc()
    ).all()

    return [
        {
            "tipo_tratamiento": resultado.tipo_tratamiento,
            "cantidad": resultado.cantidad
        }
        for resultado in resultados
    ]


@router.get("/tratamientos-mas-continuados")
def tratamientos_mas_continuados(
    usuario: Usuario = Depends(requerir_admin_o_gerente),
    db: Session = Depends(get_db)
):
    historiales = db.query(HistorialClinico).order_by(
        HistorialClinico.paciente_id.asc(),
        HistorialClinico.fecha.asc(),
        HistorialClinico.id.asc()
    ).all()

    historiales_por_paciente = defaultdict(list)

    for historial in historiales:
        historiales_por_paciente[historial.paciente_id].append(historial)

    continuaciones_por_tipo = defaultdict(int)
    nombres_por_tipo = {}

    for historiales_paciente in historiales_por_paciente.values():
        for indice in range(1, len(historiales_paciente)):
            historial_anterior = historiales_paciente[indice - 1]
            historial_actual = historiales_paciente[indice]

            tipos_anteriores = {
                tratamiento.tipo_tratamiento_id
                for tratamiento in historial_anterior.tratamientos
                if tratamiento.tipo_tratamiento_id
            }

            tipos_actuales = {
                tratamiento.tipo_tratamiento_id
                for tratamiento in historial_actual.tratamientos
                if tratamiento.tipo_tratamiento_id
            }

            tipos_continuados = tipos_anteriores.intersection(tipos_actuales)

            for tipo_id in tipos_continuados:
                continuaciones_por_tipo[tipo_id] += 1

    if not continuaciones_por_tipo:
        return []

    tipos = db.query(TipoTratamiento).filter(
        TipoTratamiento.id.in_(continuaciones_por_tipo.keys())
    ).all()

    for tipo in tipos:
        nombres_por_tipo[tipo.id] = tipo.nombre

    resultado = [
        {
            "tipo_tratamiento": nombres_por_tipo[tipo_id],
            "continuaciones": continuaciones
        }
        for tipo_id, continuaciones in continuaciones_por_tipo.items()
        if tipo_id in nombres_por_tipo
    ]

    return sorted(
        resultado,
        key=lambda item: item["continuaciones"],
        reverse=True
    )
