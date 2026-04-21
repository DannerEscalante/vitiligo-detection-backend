from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from core.database import get_db
from models.cita import Cita
from models.paciente import Paciente
from models.doctor import Doctor
from models.usuario import Usuario

from routes.auth import get_current_user

router = APIRouter(prefix="/citas", tags=["Citas"])


# CREAR CITA (PACIENTE)
@router.post("/")
def crear_cita(fecha_hora: datetime, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):

    paciente = db.query(Paciente).filter(Paciente.usuario_id == user.id).first()
    if not paciente:
        raise HTTPException(status_code=403, detail="Solo pacientes pueden crear citas")

    # ⚠️ Validación básica (no citas en el pasado)
    if fecha_hora < datetime.utcnow():
        raise HTTPException(status_code=400, detail="No puedes agendar en el pasado")

    # ⚠️ (opcional luego) evitar duplicadas

    # por ahora asignamos doctor 1 (luego lo haces dinámico)
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


# VER MIS CITAS (PACIENTE)
@router.get("/mis-citas")
def ver_mis_citas(db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):

    paciente = db.query(Paciente).filter(Paciente.usuario_id == user.id).first()
    if not paciente:
        raise HTTPException(status_code=403, detail="Solo pacientes")

    citas = db.query(Cita).filter(Cita.paciente_id == paciente.id).all()

    return citas


# VER CITAS DEL DOCTOR
@router.get("/doctor")
def ver_citas_doctor(db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):

    doctor = db.query(Doctor).filter(Doctor.usuario_id == user.id).first()
    if not doctor:
        raise HTTPException(status_code=403, detail="Solo doctores")

    citas = db.query(Cita).filter(Cita.doctor_id == doctor.id).all()

    return citas


# CAMBIAR ESTADO (DOCTOR)
@router.patch("/{cita_id}")
def cambiar_estado_cita(cita_id: int, estado: str, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):

    doctor = db.query(Doctor).filter(Doctor.usuario_id == user.id).first()
    if not doctor:
        raise HTTPException(status_code=403, detail="Solo doctores")

    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    cita.estado = estado

    db.commit()
    db.refresh(cita)

    return cita