from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import SessionLocal
from core.deps import obtener_usuario_actual

from models import Doctor, Usuario
from models.historial_clinico import HistorialClinico
from models.tratamiento import Tratamiento
from core.security import verify_password, hash_password
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
    fecha_nacimiento: str,
    sexo: str,
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(
        Usuario.id == int(usuario_id)
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    existente = db.query(Doctor).filter(
        Doctor.usuario_id == usuario.id
    ).first()

    if existente:
        raise HTTPException(
            status_code=400,
            detail="El doctor ya existe"
        )

    doctor = Doctor(
        usuario_id=usuario.id,
        nombre=nombre,
        fecha_nacimiento=fecha_nacimiento,
        sexo=sexo
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
        "id": doctor.id,
        "nombre": doctor.nombre,
        "email": doctor.usuario.email,
        "fecha_nacimiento": doctor.fecha_nacimiento,
        "sexo": doctor.sexo
    }
    
@router.put("/perfil")
def actualizar_perfil_doctor(
    email: str = None,
    contrasena: str = None,
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(
        Doctor.usuario_id == int(usuario_id)
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor no encontrado"
        )

    usuario = db.query(Usuario).filter(
        Usuario.id == doctor.usuario_id
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
    
# -------------------------------
# PACIENTES DEL DOCTOR
# -------------------------------
@router.get("/doctor")
def obtener_pacientes_doctor(
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

    historiales = db.query(HistorialClinico).filter(
        HistorialClinico.doctor_id == doctor.id
    ).all()

    pacientes_unicos = {}

    for h in historiales:

        paciente = h.paciente

        if paciente.id not in pacientes_unicos:

            tratamiento_activo = db.query(Tratamiento).filter(
                Tratamiento.paciente_id == paciente.id,
                Tratamiento.estado == "activo"
            ).first()

            pacientes_unicos[paciente.id] = {
                "id": paciente.id,
                "nombre": paciente.nombre,
                "sexo": paciente.sexo,
                "fecha_nacimiento": paciente.fecha_nacimiento,
                "tratamiento_activo": (
                    True if tratamiento_activo else False
                )
            }

    return list(pacientes_unicos.values())    
    
    
    
    
    
    
    