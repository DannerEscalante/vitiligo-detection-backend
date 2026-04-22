from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.usuario import Usuario
from app.schemas.user import UsuarioCreate
from core.security import hash_password

router = APIRouter()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/registro")
def registrar_usuario(datos: UsuarioCreate, db: Session = Depends(get_db)):
    
    nuevo_usuario = Usuario(
        email=datos.email,
        contrasena=hash_password(datos.contrasena),
        rol_id=datos.rol_id
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {
        "mensaje": "Usuario registrado correctamente",
        "usuario_id": nuevo_usuario.id
    }
    
    
    
    
