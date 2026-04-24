from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.usuario import Usuario
from app.schemas.user import UsuarioCreate
from core.security import hash_password
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.deps import obtener_usuario_actual


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
    
 
@router.put("/perfil")
def actualizar_usuario(
    email: str = None,
    contrasena: str = None,
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(
        Usuario.id == int(usuario_id)
    ).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # 🔴 validar email único
    if email:
        existente = db.query(Usuario).filter(Usuario.email == email).first()
        if existente and existente.id != usuario.id:
            raise HTTPException(status_code=400, detail="El email ya está en uso")

        usuario.email = email

    # 🔴 actualizar contraseña
    if contrasena:
        usuario.contrasena = hash_password(contrasena)

    db.commit()
    db.refresh(usuario)

    return {
        "mensaje": "Usuario actualizado correctamente"
    }   
    
    
    
    
