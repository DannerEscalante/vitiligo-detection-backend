from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from core.database import SessionLocal
from core.jwt import SECRET_KEY, ALGORITHM
from models import Usuario

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def obtener_usuario_actual(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = payload.get("sub")

        if usuario_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        return usuario_id

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


def obtener_usuario_actual_obj(
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    # Mantiene el JWT actual intacto: el token solo trae el id en "sub".
    usuario = db.query(Usuario).filter(
        Usuario.id == int(usuario_id)
    ).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    return usuario


def requerir_admin_o_gerente(
    usuario: Usuario = Depends(obtener_usuario_actual_obj)
):
    # Permite usar el rol especifico gerente o el rol admin si ya existe en la BD.
    if not usuario_es_admin_o_gerente(usuario):
        raise HTTPException(status_code=403, detail="Solo administradores o gerentes")

    return usuario


def usuario_es_admin_o_gerente(usuario: Usuario):
    nombre_rol = (
        usuario.rol.nombre_rol.strip().lower()
        if usuario.rol and usuario.rol.nombre_rol
        else ""
    )

    return nombre_rol in ["admin", "gerente"]
