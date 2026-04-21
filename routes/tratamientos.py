from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from core.database import SessionLocal
from core.deps import obtener_usuario_actual

from models import Tratamiento, Paciente, Doctor

router = APIRouter(prefix="/tratamientos", tags=["Tratamientos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def iniciar_tratamiento(
    paciente_id: int,
    tipo_tratamiento_id: int,
    descripcion: str = None,
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):

    # 🔴 validar doctor
    doctor = db.query(Doctor).filter(Doctor.usuario_id == int(usuario_id)).first()
    if not doctor:
        raise HTTPException(status_code=403, detail="Solo doctores pueden iniciar tratamientos")

    # 🔴 validar paciente
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    # 🔥 1. cerrar tratamiento activo si existe
    tratamiento_activo = db.query(Tratamiento).filter(
        Tratamiento.paciente_id == paciente_id,
        Tratamiento.estado == "activo"
    ).first()

    if tratamiento_activo:
        tratamiento_activo.estado = "finalizado"
        tratamiento_activo.fecha_fin = datetime.utcnow()

    # 🟢 2. crear nuevo tratamiento
    nuevo_tratamiento = Tratamiento(
        paciente_id=paciente_id,
        doctor_id=doctor.id,
        tipo_tratamiento_id=tipo_tratamiento_id,
        fecha_inicio=datetime.utcnow(),
        estado="activo",
        descripcion=descripcion
    )

    db.add(nuevo_tratamiento)
    db.commit()
    db.refresh(nuevo_tratamiento)

    return nuevo_tratamiento