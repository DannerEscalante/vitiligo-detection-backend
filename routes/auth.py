from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import SessionLocal
from models.usuario import Usuario
from models.paciente import Paciente

from app.schemas.auth import LoginSchema
from core.security import verify_password, hash_password
from core.jwt import crear_token

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# LOGIN
@router.post("/login")
def login(datos: LoginSchema, db: Session = Depends(get_db)):
    
    usuario = db.query(Usuario).filter(Usuario.email == datos.email).first()

    if not usuario or not verify_password(datos.contrasena, usuario.contrasena):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = crear_token({"sub": str(usuario.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }



@router.post("/register-completo")
def register_completo(
    email: str,
    contrasena: str,
    nombre: str,
    fecha_nacimiento: str,
    sexo: str,
    db: Session = Depends(get_db)
):

    existente = db.query(Usuario).filter(Usuario.email == email).first()
    if existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    nuevo_usuario = Usuario(
        email=email,
        contrasena=hash_password(contrasena),
        rol_id=1  # paciente por defecto
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    paciente = Paciente(
        usuario_id=nuevo_usuario.id,
        nombre=nombre,
        fecha_nacimiento=fecha_nacimiento,
        sexo=sexo
    )

    db.add(paciente)
    db.commit()

    token = crear_token({"sub": str(nuevo_usuario.id)})

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario_id": nuevo_usuario.id,
        "rol_id": nuevo_usuario.rol_id 
    }