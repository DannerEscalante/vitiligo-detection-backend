from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import SessionLocal
from core.deps import obtener_usuario_actual

from models import Doctor, Usuario

router = APIRouter(prefix="/doctores", tags=["Doctores"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def crear_doctor(
    nombre: str,
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id == int(usuario_id)).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    existente = db.query(Doctor).filter(Doctor.usuario_id == usuario.id).first()

    if existente:
        raise HTTPException(status_code=400, detail="El doctor ya existe")

    doctor = Doctor(
        usuario_id=usuario.id,
        nombre=nombre
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return doctor


@router.get("/perfil")
def obtener_perfil_doctor(
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(
        Doctor.usuario_id == int(usuario_id)
    ).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")

    return {
        "nombre": doctor.nombre,
        "fecha_nacimiento": doctor.fecha_nacimiento,
        "sexo": doctor.sexo
    }