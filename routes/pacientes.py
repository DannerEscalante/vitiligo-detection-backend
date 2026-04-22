from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import SessionLocal
from core.deps import obtener_usuario_actual

from models import Paciente, Usuario

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def crear_paciente(
    nombre: str,
    fecha_nacimiento: str,
    sexo: str,
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id == int(usuario_id)).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    existente = db.query(Paciente).filter(Paciente.usuario_id == usuario.id).first()

    if existente:
        raise HTTPException(status_code=400, detail="El paciente ya existe")

    paciente = Paciente(
        usuario_id=usuario.id,
        nombre=nombre,
        fecha_nacimiento=fecha_nacimiento,
        sexo=sexo
    )

    db.add(paciente)
    db.commit()
    db.refresh(paciente)

    return paciente