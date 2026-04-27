from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from core.database import SessionLocal
from core.deps import obtener_usuario_actual

from models import Doctor, Cita, HistorialClinico, Prediccion
from models.paciente import Paciente

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
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(
        Doctor.usuario_id == int(usuario_id)
    ).first()

    if not doctor:
        raise HTTPException(status_code=403, detail="Solo doctores")

    cita = db.query(Cita).filter(Cita.id == cita_id).first()

    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    if cita.estado != "confirmada":
        raise HTTPException(status_code=400, detail="Cita no confirmada")

    existente = db.query(HistorialClinico).filter(
        HistorialClinico.cita_id == cita.id
    ).first()

    if existente:
        raise HTTPException(status_code=400, detail="Ya existe historial")

    historial = HistorialClinico(
        paciente_id=cita.paciente_id,
        doctor_id=doctor.id,
        cita_id=cita.id,
        diagnostico=diagnostico,
        fecha=datetime.utcnow()
    )

    db.add(historial)
    db.commit()
    db.refresh(historial)

    return historial

@router.get("/paciente")
def ver_historial_paciente(
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    paciente = db.query(Paciente).filter(
        Paciente.usuario_id == int(usuario_id)
    ).first()

    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    historiales = db.query(HistorialClinico).filter(
        HistorialClinico.paciente_id == paciente.id
    ).all()

    resultado = []

    for h in historiales:
        data = {
            "id": h.id,
            "fecha": h.fecha,
            "diagnostico": h.diagnostico,
            "tratamientos": []
        }

        for t in h.tratamientos:
            tratamiento_data = {
                "id": t.id,
                "estado": t.estado,
                "fecha_inicio": t.fecha_inicio,
                "fecha_fin": t.fecha_fin,
                "notas": t.notas,
                "predicciones": []
            }

            for p in t.predicciones:
                tratamiento_data["predicciones"].append({
                    "resultado": p.resultado,
                    "confianza": float(p.confianza),
                    "imagen": p.imagen.url_imagen if p.imagen else None
                })

            data["tratamientos"].append(tratamiento_data)

        resultado.append(data)

    return resultado

@router.get("/doctor")
def ver_historial_doctor(
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(Doctor.usuario_id == int(usuario_id)).first()

    if not doctor:
        raise HTTPException(status_code=403, detail="Solo doctores")

    historiales = db.query(HistorialClinico).filter(
        HistorialClinico.doctor_id == doctor.id
    ).all()

    return historiales






