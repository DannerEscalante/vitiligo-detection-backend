from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import SessionLocal
from core.deps import obtener_usuario_actual

from models.tipo_tratamiento import TipoTratamiento
from models import Doctor

router = APIRouter(
    prefix="/tipos-tratamiento",
    tags=["Tipos Tratamiento"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------
# CREAR TIPO DE TRATAMIENTO
# -------------------------------
@router.post("/")
def crear_tipo_tratamiento(
    nombre: str,
    descripcion: str = None,
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(
        Doctor.usuario_id == int(usuario_id)
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=403,
            detail="Solo doctores"
        )

    existente = db.query(TipoTratamiento).filter(
        TipoTratamiento.nombre == nombre
    ).first()

    if existente:
        raise HTTPException(
            status_code=400,
            detail="El tipo de tratamiento ya existe"
        )

    nuevo = TipoTratamiento(
        nombre=nombre,
        descripcion=descripcion
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


# -------------------------------
# LISTAR TIPOS DE TRATAMIENTO
# -------------------------------
@router.get("/")
def obtener_tipos_tratamiento(
    db: Session = Depends(get_db)
):
    tipos = db.query(TipoTratamiento).all()

    resultado = []

    for t in tipos:

        resultado.append({
            "id": t.id,
            "nombre": t.nombre
        })

    return resultado