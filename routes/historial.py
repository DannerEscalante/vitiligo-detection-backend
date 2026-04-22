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
    tipo_tratamiento_id: int = None,
    descripcion_tratamiento: str = None,
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    from models import Tratamiento, Paciente

    doctor = db.query(Doctor).filter(Doctor.usuario_id == int(usuario_id)).first()

    if not doctor:
        raise HTTPException(status_code=403, detail="Solo doctores pueden crear historial")

    cita = db.query(Cita).filter(Cita.id == cita_id).first()

    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    if cita.estado != "confirmada":
        raise HTTPException(status_code=400, detail="La cita debe estar confirmada")

    existente = db.query(HistorialClinico).filter(
        HistorialClinico.cita_id == cita.id
    ).first()

    if existente:
        raise HTTPException(status_code=400, detail="Ya existe historial para esta cita")

    tratamiento = None

    # 🔥 SI SE ENVÍA TRATAMIENTO → CREARLO
    if tipo_tratamiento_id:

        # cerrar tratamiento activo anterior
        tratamiento_activo = db.query(Tratamiento).filter(
            Tratamiento.paciente_id == cita.paciente_id,
            Tratamiento.estado == "activo"
        ).first()

        if tratamiento_activo:
            tratamiento_activo.estado = "finalizado"
            tratamiento_activo.fecha_fin = datetime.utcnow()

        tratamiento = Tratamiento(
            paciente_id=cita.paciente_id,
            doctor_id=doctor.id,
            tipo_tratamiento_id=tipo_tratamiento_id,
            descripcion=descripcion_tratamiento,
            fecha_inicio=datetime.utcnow(),
            estado="activo"
        )

        db.add(tratamiento)
        db.commit()
        db.refresh(tratamiento)

    # 🟢 CREAR HISTORIAL
    historial = HistorialClinico(
        paciente_id=cita.paciente_id,
        doctor_id=doctor.id,
        cita_id=cita.id,
        prediccion_id=cita.prediccion_id,
        diagnostico=diagnostico,
        notas=notas,
        fecha=datetime.utcnow(),
        tratamiento_id=tratamiento.id if tratamiento else None
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
    from models import Paciente

    paciente = db.query(Paciente).filter(Paciente.usuario_id == int(usuario_id)).first()

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
            "notas": h.notas
        }

        if h.prediccion:
            data["prediccion"] = {
                "resultado": h.prediccion.resultado,
                "confianza": float(h.prediccion.confianza),
                "imagen": h.prediccion.imagen.url_imagen if h.prediccion.imagen else None
            }

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