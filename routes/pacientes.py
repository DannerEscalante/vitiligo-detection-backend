from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import SessionLocal
from core.deps import obtener_usuario_actual
from core.security import verify_password, hash_password

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

@router.get("/perfil")
def obtener_perfil_paciente(
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    paciente = db.query(Paciente).filter(
        Paciente.usuario_id == int(usuario_id)
    ).first()

    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    return {
        "id": paciente.id,
        "nombre": paciente.nombre,
        "email": paciente.usuario.email,
        "fecha_nacimiento": paciente.fecha_nacimiento,
        "sexo": paciente.sexo
    }
    
@router.put("/perfil")
def actualizar_perfil_paciente(
    email: str = None,
    contrasena: str = None,
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

    usuario = db.query(Usuario).filter(
        Usuario.id == paciente.usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if email:

        existente = db.query(Usuario).filter(
            Usuario.email == email
        ).first()

        if existente and existente.id != usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El email ya está en uso"
            )

        usuario.email = email

    if contrasena:

        usuario.contrasena = hash_password(contrasena)

    db.commit()
    db.refresh(usuario)

    return {
        "mensaje": "Perfil actualizado correctamente"
    }
    
    
    
    
    
    
    
    
    