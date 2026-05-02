from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import SessionLocal
from models import usuario
from models.usuario import Usuario
from models.paciente import Paciente

from app.schemas.auth import LoginSchema
from core.security import verify_password, hash_password
from core.jwt import ALGORITHM, SECRET_KEY, crear_access_token, crear_refresh_token
from jose import jwt, JWTError
from fastapi import APIRouter, HTTPException

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
    
    
    access_token = crear_access_token({"sub": str(usuario.id)})
    refresh_token = crear_refresh_token({"sub": str(usuario.id)})
    print("USUARIO EN LOGIN:", usuario.id, usuario.email)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "rol_id": usuario.rol_id,
        "token_type": "bearer"
    }

   
   


router = APIRouter()

@router.post("/refresh")
def refresh_token(refresh_token: str):

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Token inválido")

        user_id = payload.get("sub")

        new_access_token = crear_access_token({"sub": user_id})

        return {
            "access_token": new_access_token
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Refresh token inválido") 




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

    access_token = crear_access_token({"sub": str(nuevo_usuario.id)})
    refresh_token = crear_refresh_token({"sub": str(nuevo_usuario.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "usuario_id": nuevo_usuario.id,
        "rol_id": nuevo_usuario.rol_id
    }