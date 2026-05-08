from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from core.database import SessionLocal
from core.deps import obtener_usuario_actual

from models import Tratamiento, Paciente, Doctor, cita
from models.historial_clinico import HistorialClinico
from models.prediccion import Prediccion
from routes import historial

router = APIRouter(prefix="/tratamientos", tags=["Tratamientos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def iniciar_tratamiento(
    historial_id: int,
    tipo_tratamiento_id: int,
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(
        Doctor.usuario_id == int(usuario_id)
    ).first()

    if not doctor:
        raise HTTPException(status_code=403, detail="Solo doctores")

    historial = db.query(HistorialClinico).filter(
        HistorialClinico.id == historial_id
    ).first()

    if not historial:
        raise HTTPException(status_code=404, detail="Historial no encontrado")

    # cerrar tratamiento activo
    tratamiento_activo = db.query(Tratamiento).filter(
        Tratamiento.paciente_id == historial.paciente_id,
        Tratamiento.estado == "activo"
    ).first()

    if tratamiento_activo:
        tratamiento_activo.estado = "finalizado"
        tratamiento_activo.fecha_fin = datetime.utcnow()

    nuevo = Tratamiento(
        historial_id=historial.id,
        paciente_id=historial.paciente_id,
        doctor_id=doctor.id,
        tipo_tratamiento_id=tipo_tratamiento_id,
        fecha_inicio=datetime.utcnow(),
        estado="activo"
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    # asignar predicción inicial después de crear tratamiento
    cita = historial.cita

    if cita and cita.prediccion_id:
        pred_inicial = db.query(Prediccion).filter(
            Prediccion.id == cita.prediccion_id
        ).first()

        if pred_inicial:
            pred_inicial.tratamiento_id = nuevo.id
            db.commit()

    return nuevo


@router.get("/activo")
def obtener_tratamiento_activo(
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    paciente = db.query(Paciente).filter(
        Paciente.usuario_id == int(usuario_id)
    ).first()

    if not paciente:
        raise HTTPException(
            status_code=404,
            detail="Paciente no encontrado"
        )

    tratamiento = db.query(Tratamiento).filter(
        Tratamiento.paciente_id == paciente.id,
        Tratamiento.estado == "activo"
    ).first()

    if not tratamiento:

        return {
            "tiene_tratamiento": False,
            "tratamiento_id": None,
            "tipo_tratamiento": None,
            "fecha_inicio": None,
            "estado": None,
            "notas": None
        }

    return {
        "tiene_tratamiento": True,
        "tratamiento_id": tratamiento.id,
        "tipo_tratamiento": tratamiento.tipo_tratamiento.nombre,
        "fecha_inicio": tratamiento.fecha_inicio,
        "estado": tratamiento.estado,
        "notas": tratamiento.notas
    }


@router.get("/activo/paciente/{paciente_id}")
def obtener_tratamiento_activo_paciente(

    paciente_id: int,

    usuario_id: str = Depends(obtener_usuario_actual),

    db: Session = Depends(get_db)
):

    doctor = db.query(Doctor).filter(
        Doctor.usuario_id == int(usuario_id)
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor no encontrado"
        )

    paciente = db.query(Paciente).filter(
        Paciente.id == paciente_id
    ).first()

    if not paciente:
        raise HTTPException(
            status_code=404,
            detail="Paciente no encontrado"
        )

    tratamiento = db.query(Tratamiento).filter(

        Tratamiento.paciente_id == paciente.id,

        Tratamiento.estado == "activo"

    ).first()

    if not tratamiento:

        return {
            "tiene_tratamiento": False,
            "tratamiento_id": None,
            "tipo_tratamiento": None,
            "fecha_inicio": None,
            "estado": None,
            "notas": None
        }

    return {

        "tiene_tratamiento": True,

        "tratamiento_id": tratamiento.id,

        "tipo_tratamiento":
            tratamiento.tipo_tratamiento.nombre,

        "fecha_inicio": tratamiento.fecha_inicio,

        "estado": tratamiento.estado,

        "notas": tratamiento.notas
    }




# -------------------------------
# ACTUALIZAR NOTAS DEL TRATAMIENTO
# -------------------------------
@router.patch("/{tratamiento_id}/notas")
def actualizar_notas_tratamiento(
    tratamiento_id: int,
    notas: str,
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

    tratamiento = db.query(Tratamiento).filter(
        Tratamiento.id == tratamiento_id
    ).first()

    if not tratamiento:
        raise HTTPException(
            status_code=404,
            detail="Tratamiento no encontrado"
        )

    tratamiento.notas = notas

    db.commit()
    db.refresh(tratamiento)

    return {
        "mensaje": "Notas actualizadas correctamente"
    }


# -------------------------------
# FINALIZAR TRATAMIENTO
# -------------------------------
@router.patch("/{tratamiento_id}/finalizar")
def finalizar_tratamiento(
    tratamiento_id: int,
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

    tratamiento = db.query(Tratamiento).filter(
        Tratamiento.id == tratamiento_id
    ).first()

    if not tratamiento:
        raise HTTPException(
            status_code=404,
            detail="Tratamiento no encontrado"
        )

    if tratamiento.estado == "finalizado":
        raise HTTPException(
            status_code=400,
            detail="El tratamiento ya está finalizado"
        )

    tratamiento.estado = "finalizado"
    tratamiento.fecha_fin = datetime.utcnow()

    db.commit()
    db.refresh(tratamiento)

    return {
        "mensaje": "Tratamiento finalizado correctamente"
    }









