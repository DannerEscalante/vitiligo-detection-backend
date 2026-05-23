from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from core.database import SessionLocal
from core.deps import obtener_usuario_actual, requerir_admin_o_gerente

from models import Doctor, Tratamiento, Usuario
from models.tipo_tratamiento import TipoTratamiento

router = APIRouter(
    prefix="/tipos-tratamiento",
    tags=["Tipos Tratamiento"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def calcular_continuaciones_por_tipo(db: Session):
    tratamientos = db.query(Tratamiento).all()
    historiales_por_id = {}

    for tratamiento in tratamientos:
        if tratamiento.historial and tratamiento.tipo_tratamiento_id:
            historiales_por_id[tratamiento.historial.id] = tratamiento.historial

    historiales_por_paciente = defaultdict(list)

    for historial in historiales_por_id.values():
        historiales_por_paciente[historial.paciente_id].append(historial)

    continuaciones = defaultdict(int)

    for historiales in historiales_por_paciente.values():
        historiales_ordenados = sorted(
            historiales,
            key=lambda h: (h.fecha, h.id)
        )

        for indice in range(1, len(historiales_ordenados)):
            anterior = historiales_ordenados[indice - 1]
            actual = historiales_ordenados[indice]

            tipos_anteriores = {
                t.tipo_tratamiento_id
                for t in anterior.tratamientos
                if t.tipo_tratamiento_id
            }
            tipos_actuales = {
                t.tipo_tratamiento_id
                for t in actual.tratamientos
                if t.tipo_tratamiento_id
            }

            for tipo_id in tipos_anteriores.intersection(tipos_actuales):
                continuaciones[tipo_id] += 1

    return continuaciones


# -------------------------------
# CREAR TIPO DE TRATAMIENTO (móvil — solo doctores)
# -------------------------------
@router.post("/")
def crear_tipo_tratamiento(
    nombre: str,
    descripcion: str = None,
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(
        Doctor.usuario_id == int(usuario_id)
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=403,
            detail="Solo doctores"
        )

    existente = db.query(TipoTratamiento).filter(
        TipoTratamiento.nombre == nombre
    ).first()

    if existente:
        raise HTTPException(
            status_code=400,
            detail="El tipo de tratamiento ya existe"
        )

    nuevo = TipoTratamiento(
        nombre=nombre,
        descripcion=descripcion
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


# -------------------------------
# LISTAR TIPOS DE TRATAMIENTO (móvil — lista mínima para dropdowns)
# -------------------------------
@router.get("/")
def obtener_tipos_tratamiento(
    db: Session = Depends(get_db)
):
    tipos = db.query(TipoTratamiento).all()

    resultado = []

    for t in tipos:

        resultado.append({
            "id": t.id,
            "nombre": t.nombre
        })

    return resultado


# -----------------------------------------------------------------------------
# SCHEMAS Y ENDPOINTS ADMINISTRATIVOS (EXCLUSIVOS PARA PANEL GERENCIAL / WEB)
# -----------------------------------------------------------------------------

class TipoTratamientoCreate(BaseModel):
    nombre: str
    descripcion: str = None


class TipoTratamientoUpdate(BaseModel):
    nombre: str = None
    descripcion: str = None


@router.post("/admin")
def crear_tipo_tratamiento_admin(
    datos: TipoTratamientoCreate,
    usuario: Usuario = Depends(requerir_admin_o_gerente),
    db: Session = Depends(get_db)
):
    """Crea un nuevo tipo de tratamiento desde el panel administrativo."""
    existente = db.query(TipoTratamiento).filter(
        TipoTratamiento.nombre == datos.nombre
    ).first()

    if existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un tipo de tratamiento con ese nombre."
        )

    nuevo = TipoTratamiento(
        nombre=datos.nombre,
        descripcion=datos.descripcion
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {
        "id": nuevo.id,
        "nombre": nuevo.nombre,
        "descripcion": nuevo.descripcion
    }


@router.get("/admin")
def listar_tipos_tratamiento_admin(
    usuario: Usuario = Depends(requerir_admin_o_gerente),
    db: Session = Depends(get_db)
):
    """Lista el catálogo completo con estadísticas de uso real."""
    tipos = db.query(TipoTratamiento).order_by(TipoTratamiento.nombre.asc()).all()
    continuaciones = calcular_continuaciones_por_tipo(db)

    resultado = []
    for tipo in tipos:
        tratamientos = tipo.tratamientos

        total_usos = len(tratamientos)
        activos = sum(1 for t in tratamientos if t.estado == "activo")
        pacientes_unicos = len({t.paciente_id for t in tratamientos if t.paciente_id})
        doctores_unicos = len({t.doctor_id for t in tratamientos if t.doctor_id})

        resultado.append({
            "id": tipo.id,
            "nombre": tipo.nombre,
            "descripcion": tipo.descripcion,
            "total_usos": total_usos,
            "activos": activos,
            "continuaciones": continuaciones.get(tipo.id, 0),
            "pacientes_unicos": pacientes_unicos,
            "doctores_unicos": doctores_unicos,
        })

    return resultado


@router.put("/{tipo_id}")
def editar_tipo_tratamiento(
    tipo_id: int,
    datos: TipoTratamientoUpdate,
    usuario: Usuario = Depends(requerir_admin_o_gerente),
    db: Session = Depends(get_db)
):
    """Edita nombre y/o descripción de un tipo de tratamiento existente."""
    tipo = db.query(TipoTratamiento).filter(TipoTratamiento.id == tipo_id).first()

    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de tratamiento no encontrado.")

    if datos.nombre and datos.nombre != tipo.nombre:
        duplicado = db.query(TipoTratamiento).filter(
            TipoTratamiento.nombre == datos.nombre,
            TipoTratamiento.id != tipo_id
        ).first()
        if duplicado:
            raise HTTPException(
                status_code=400,
                detail="Ya existe otro tipo de tratamiento con ese nombre."
            )
        tipo.nombre = datos.nombre

    if datos.descripcion is not None:
        tipo.descripcion = datos.descripcion

    db.commit()
    db.refresh(tipo)

    return {
        "mensaje": "Tipo de tratamiento actualizado correctamente.",
        "id": tipo.id,
        "nombre": tipo.nombre,
        "descripcion": tipo.descripcion
    }


@router.get("/{tipo_id}/estadisticas")
def estadisticas_tipo_tratamiento(
    tipo_id: int,
    usuario: Usuario = Depends(requerir_admin_o_gerente),
    db: Session = Depends(get_db)
):
    """Detalle estadístico completo de un tipo de tratamiento."""
    tipo = db.query(TipoTratamiento).filter(TipoTratamiento.id == tipo_id).first()

    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de tratamiento no encontrado.")

    tratamientos = (
        db.query(Tratamiento)
        .filter(Tratamiento.tipo_tratamiento_id == tipo_id)
        .order_by(Tratamiento.fecha_inicio.desc())
        .all()
    )

    total_usos = len(tratamientos)
    activos = sum(1 for t in tratamientos if t.estado == "activo")
    finalizados = sum(1 for t in tratamientos if t.estado == "finalizado")
    pacientes_unicos = len({t.paciente_id for t in tratamientos if t.paciente_id})
    doctores_unicos = len({t.doctor_id for t in tratamientos if t.doctor_id})
    continuaciones = calcular_continuaciones_por_tipo(db).get(tipo_id, 0)

    # Top 5 doctores que más lo aplicaron
    conteo_doctores: dict = defaultdict(int)
    nombres_doctores: dict = {}
    for t in tratamientos:
        if t.doctor_id:
            conteo_doctores[t.doctor_id] += 1
            if t.doctor and t.doctor_id not in nombres_doctores:
                nombres_doctores[t.doctor_id] = t.doctor.nombre

    top_doctores = sorted(
        [
            {"doctor_id": did, "nombre": nombres_doctores.get(did, "Desconocido"), "usos": usos}
            for did, usos in conteo_doctores.items()
        ],
        key=lambda x: x["usos"],
        reverse=True
    )[:5]

    conteo_pacientes: dict = defaultdict(int)
    nombres_pacientes: dict = {}
    for t in tratamientos:
        if t.paciente_id:
            conteo_pacientes[t.paciente_id] += 1
            if t.paciente and t.paciente_id not in nombres_pacientes:
                nombres_pacientes[t.paciente_id] = t.paciente.nombre

    pacientes_relacionados = sorted(
        [
            {"paciente_id": pid, "nombre": nombres_pacientes.get(pid, "Desconocido"), "usos": usos}
            for pid, usos in conteo_pacientes.items()
        ],
        key=lambda x: x["usos"],
        reverse=True
    )[:10]

    doctores_relacionados = sorted(
        [
            {"doctor_id": did, "nombre": nombres_doctores.get(did, "Desconocido"), "usos": usos}
            for did, usos in conteo_doctores.items()
        ],
        key=lambda x: x["usos"],
        reverse=True
    )[:10]

    # Últimos 5 usos
    ultimos_usos = []
    for t in tratamientos[:5]:
        ultimos_usos.append({
            "id": t.id,
            "paciente_nombre": t.paciente.nombre if t.paciente else "Desconocido",
            "doctor_nombre": t.doctor.nombre if t.doctor else "Desconocido",
            "estado": t.estado,
            "fecha_inicio": t.fecha_inicio.isoformat() if t.fecha_inicio else None,
            "fecha_fin": t.fecha_fin.isoformat() if t.fecha_fin else None,
        })

    return {
        "datos_basicos": {
            "id": tipo.id,
            "nombre": tipo.nombre,
            "descripcion": tipo.descripcion,
        },
        "total_usos": total_usos,
        "activos": activos,
        "finalizados": finalizados,
        "continuaciones": continuaciones,
        "pacientes_unicos": pacientes_unicos,
        "doctores_unicos": doctores_unicos,
        "top_doctores": top_doctores,
        "pacientes_relacionados": pacientes_relacionados,
        "doctores_relacionados": doctores_relacionados,
        "ultimos_usos": ultimos_usos,
    }
