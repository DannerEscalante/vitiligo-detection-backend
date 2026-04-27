from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from core.database import SessionLocal
from core.deps import obtener_usuario_actual

from models import Paciente, Doctor, Cita, Prediccion, Imagen

router = APIRouter(prefix="/citas", tags=["Citas"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def crear_cita(
    fecha_hora: datetime,
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    paciente = db.query(Paciente).filter(
        Paciente.usuario_id == int(usuario_id)
    ).first()

    if not paciente:
        raise HTTPException(status_code=403, detail="Solo pacientes")

    if fecha_hora < datetime.utcnow():
        raise HTTPException(status_code=400, detail="No puedes agendar en el pasado")

    if fecha_hora.hour < 6 or fecha_hora.hour >= 22:
        raise HTTPException(status_code=400, detail="Fuera de horario")

    nueva_cita = Cita(
        paciente_id=paciente.id,
        fecha_hora=fecha_hora,
        duracion=30,
        estado="pendiente",
        fecha_creacion=datetime.utcnow()
    )

    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)

    return nueva_cita


@router.patch("/{cita_id}/confirmar")
def confirmar_cita(
    cita_id: int,
    doctor_id: int,
    duracion: int = 30,
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    doctor_auth = db.query(Doctor).filter(Doctor.usuario_id == int(usuario_id)).first()
    if not doctor_auth:
        raise HTTPException(status_code=403, detail="Solo doctores pueden confirmar citas")

    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")

    if duracion < 15 or duracion > 120:
        raise HTTPException(status_code=400, detail="Duración inválida")

    inicio_nueva = cita.fecha_hora
    fin_nueva = cita.fecha_hora + timedelta(minutes=duracion)

    citas_doctor = db.query(Cita).filter(
        Cita.doctor_id == doctor_id,
        Cita.id != cita.id,
        Cita.estado == "confirmada"
    ).all()

    for c in citas_doctor:
        inicio_existente = c.fecha_hora
        fin_existente = c.fecha_hora + timedelta(minutes=c.duracion)

        if (inicio_nueva < fin_existente) and (fin_nueva > inicio_existente):
            raise HTTPException(status_code=400, detail="Conflicto con otra cita confirmada")

    cita.doctor_id = doctor_id
    cita.duracion = duracion
    cita.estado = "confirmada"

    db.commit()
    db.refresh(cita)

    return cita


@router.get("/doctor")
def ver_citas_doctor(
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(Doctor.usuario_id == int(usuario_id)).first()

    if not doctor:
        raise HTTPException(status_code=403, detail="Solo doctores pueden ver sus citas")

    citas = db.query(Cita).filter(
        (Cita.doctor_id == doctor.id) | (Cita.doctor_id == None)
    ).all()

    resultado = []

    for c in citas:
        data = {
            "id": c.id,
            "fecha_hora": c.fecha_hora,
            "estado": c.estado,
            "duracion": c.duracion,
            "paciente_id": c.paciente_id
        }

        if c.prediccion:
            data["prediccion"] = {
                "resultado": c.prediccion.resultado,
                "confianza": float(c.prediccion.confianza),
                "imagen": c.prediccion.imagen.url_imagen if c.prediccion.imagen else None
            }

        resultado.append(data)

    return resultado


@router.get("/mis-citas")
def ver_mis_citas(
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    paciente = db.query(Paciente).filter(Paciente.usuario_id == int(usuario_id)).first()

    if not paciente:
        raise HTTPException(status_code=403, detail="Solo pacientes pueden ver sus citas")

    citas = db.query(Cita).filter(Cita.paciente_id == paciente.id).all()

    return citas


@router.patch("/{cita_id}/estado")
def cambiar_estado_cita(
    cita_id: int,
    estado: str,
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    from models import Paciente

    cita = db.query(Cita).filter(Cita.id == cita_id).first()

    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    # no modificar si ya finalizada
    if cita.estado == "finalizada":
        raise HTTPException(status_code=400, detail="La cita ya está finalizada")

    doctor = db.query(Doctor).filter(Doctor.usuario_id == int(usuario_id)).first()
    paciente = db.query(Paciente).filter(Paciente.usuario_id == int(usuario_id)).first()

    # validar estado permitido
    if estado not in ["pendiente", "confirmada", "cancelada", "finalizada"]:
        raise HTTPException(status_code=400, detail="Estado inválido")

    # 🔵 SI ES DOCTOR
    if doctor:
        # no puede confirmar si está cancelada
        if estado == "confirmada" and cita.estado == "cancelada":
            raise HTTPException(status_code=400, detail="No puedes confirmar una cita cancelada")

        # no puede finalizar si no está confirmada
        if estado == "finalizada" and cita.estado != "confirmada":
            raise HTTPException(status_code=400, detail="Solo puedes finalizar citas confirmadas")

        cita.estado = estado

    # 🟢 SI ES PACIENTE
    elif paciente:
        # solo puede cancelar sus propias citas
        if cita.paciente_id != paciente.id:
            raise HTTPException(status_code=403, detail="No puedes modificar esta cita")

        if estado != "cancelada":
            raise HTTPException(status_code=403, detail="Solo puedes cancelar la cita")

        cita.estado = "cancelada"

    else:
        raise HTTPException(status_code=403, detail="Usuario no autorizado")

    db.commit()
    db.refresh(cita)

    return cita