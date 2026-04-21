from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime,timedelta

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
from datetime import datetime, timedelta

@router.post("/")
def crear_cita(
    fecha_hora: datetime,
    doctor_id: int,
    duracion: int = 30,
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):

    paciente = db.query(Paciente).filter(Paciente.usuario_id == int(usuario_id)).first()

    if not paciente:
        raise HTTPException(status_code=403, detail="Solo pacientes pueden crear citas")

    # 🔴 1. Validar fecha futura
    if fecha_hora < datetime.utcnow():
        raise HTTPException(status_code=400, detail="No puedes agendar en el pasado")

    # 🔴 2. Validar horario (06:00 - 22:00)
    if fecha_hora.hour < 6 or fecha_hora.hour >= 22:
        raise HTTPException(status_code=400, detail="Fuera de horario de atención")

    # 🔴 3. Validar duración
    if duracion < 15 or duracion > 120:
        raise HTTPException(status_code=400, detail="Duración inválida (15-120 min)")

    # 🔴 4. Validar doctor
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")

    # 🔴 5. Calcular rango de tiempo
    inicio_nueva = fecha_hora
    fin_nueva = fecha_hora + timedelta(minutes=duracion)

    # 🔥 6. Validar solapamiento con citas del doctor
    citas_doctor = db.query(Cita).filter(Cita.doctor_id == doctor_id).all()

    for cita in citas_doctor:
        inicio_existente = cita.fecha_hora
        fin_existente = cita.fecha_hora + timedelta(minutes=cita.duracion)

        if (inicio_nueva < fin_existente) and (fin_nueva > inicio_existente):
            raise HTTPException(
                status_code=400,
                detail="El doctor ya tiene una cita en ese horario"
            )

    # 🔥 7. Validar que el paciente no tenga solapamientos
    citas_paciente = db.query(Cita).filter(Cita.paciente_id == paciente.id).all()

    for cita in citas_paciente:
        inicio_existente = cita.fecha_hora
        fin_existente = cita.fecha_hora + timedelta(minutes=cita.duracion)

        if (inicio_nueva < fin_existente) and (fin_nueva > inicio_existente):
            raise HTTPException(
                status_code=400,
                detail="Ya tienes una cita en ese horario"
            )

    # 🟢 Crear cita
    nueva_cita = Cita(
        paciente_id=paciente.id,
        doctor_id=doctor_id,
        fecha_hora=fecha_hora,
        duracion=duracion,
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