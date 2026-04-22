from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from core.database import SessionLocal
from core.deps import obtener_usuario_actual

from models import Doctor, Cita, HistorialClinico, Prediccion

router = APIRouter(prefix="/historial-clinico", tags=["Historial Clínico"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/desde-cita/{cita_id}")
def crear_historial_desde_cita(
    cita_id: int,
    diagnostico: str,
    notas: str = None,
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(Doctor.usuario_id == int(usuario_id)).first()

    if not doctor:
        raise HTTPException(status_code=403, detail="Solo doctores pueden crear historial")

    cita = db.query(Cita).filter(Cita.id == cita_id).first()

    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    if cita.estado != "confirmada":
        raise HTTPException(status_code=400, detail="La cita debe estar confirmada")

    # evitar duplicados
    existente = db.query(HistorialClinico).filter(HistorialClinico.cita_id == cita.id).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe historial para esta cita")

    historial = HistorialClinico(
        paciente_id=cita.paciente_id,
        doctor_id=doctor.id,
        cita_id=cita.id,
        prediccion_id=cita.prediccion_id,
        diagnostico=diagnostico,
        notas=notas,
        fecha=datetime.utcnow()
    )

    db.add(historial)
    db.commit()
    db.refresh(historial)

    return historial