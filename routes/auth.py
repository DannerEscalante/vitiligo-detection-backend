import token

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.usuario import Usuario
from app.schemas.auth import LoginSchema
from core.security import verify_password
from core.jwt import crear_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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