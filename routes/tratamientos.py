from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from core.database import SessionLocal
from core.deps import obtener_usuario_actual

from models import Tratamiento, Paciente, Doctor
from models.historial_clinico import HistorialClinico

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

    return nuevo







