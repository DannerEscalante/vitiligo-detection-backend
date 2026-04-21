from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from core.database import SessionLocal
from core.deps import obtener_usuario_actual

from models import Paciente, Doctor, Cita

router = APIRouter(prefix="/citas", tags=["Citas"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREAR CITA (PACIENTE)
@router.post("/")
def crear_cita(
    fecha_hora: datetime,
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):

    paciente = db.query(Paciente).filter(Paciente.usuario_id == int(usuario_id)).first()

    if not paciente:
        raise HTTPException(status_code=403, detail="Solo pacientes pueden crear citas")

    if fecha_hora < datetime.utcnow():
        raise HTTPException(status_code=400, detail="No puedes agendar en el pasado")

    doctor = db.query(Doctor).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="No hay doctores disponibles")

    nueva_cita = Cita(
        paciente_id=paciente.id,
        doctor_id=doctor.id,
        fecha_hora=fecha_hora,
        estado="pendiente",
        fecha_creacion=datetime.utcnow()
    )

    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)

    return nueva_cita


# 🟢 VER MIS CITAS
@router.get("/mis-citas")
def ver_mis_citas(
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):

    paciente = db.query(Paciente).filter(Paciente.usuario_id == int(usuario_id)).first()

    if not paciente:
        raise HTTPException(status_code=403, detail="Solo pacientes")

    citas = db.query(Cita).filter(Cita.paciente_id == paciente.id).all()

    return citas


# 🟢 VER CITAS DEL DOCTOR
@router.get("/doctor")
def ver_citas_doctor(
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):

    doctor = db.query(Doctor).filter(Doctor.usuario_id == int(usuario_id)).first()

    if not doctor:
        raise HTTPException(status_code=403, detail="Solo doctores")

    citas = db.query(Cita).filter(Cita.doctor_id == doctor.id).all()

    return citas


# 🟢 CAMBIAR ESTADO
@router.patch("/{cita_id}")
def cambiar_estado_cita(
    cita_id: int,
    estado: str,
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):

    doctor = db.query(Doctor).filter(Doctor.usuario_id == int(usuario_id)).first()

    if not doctor:
        raise HTTPException(status_code=403, detail="Solo doctores")

    cita = db.query(Cita).filter(Cita.id == cita_id).first()

    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    cita.estado = estado

    db.commit()
    db.refresh(cita)

    return cita