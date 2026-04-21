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
    doctor_id: int,
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):

    paciente = db.query(Paciente).filter(Paciente.usuario_id == int(usuario_id)).first()

    if not paciente:
        raise HTTPException(status_code=403, detail="Solo pacientes pueden crear citas")

    # 🔴 1. Validar fecha en el futuro
    if fecha_hora < datetime.utcnow():
        raise HTTPException(status_code=400, detail="No puedes agendar en el pasado")

    # 🔴 2. Validar doctor existe
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")

    # 🔴 3. Evitar doble cita del mismo paciente a la misma hora
    cita_existente = db.query(Cita).filter(
        Cita.paciente_id == paciente.id,
        Cita.fecha_hora == fecha_hora
    ).first()

    if cita_existente:
        raise HTTPException(status_code=400, detail="Ya tienes una cita en ese horario")

    # 🔴 4. Evitar que el doctor tenga dos citas al mismo tiempo
    conflicto_doctor = db.query(Cita).filter(
        Cita.doctor_id == doctor_id,
        Cita.fecha_hora == fecha_hora
    ).first()

    if conflicto_doctor:
        raise HTTPException(status_code=400, detail="El doctor ya tiene una cita en ese horario")

    # 🟢 Crear cita
    nueva_cita = Cita(
        paciente_id=paciente.id,
        doctor_id=doctor_id,
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