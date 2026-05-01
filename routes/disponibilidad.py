from datetime import datetime, time, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import SessionLocal
from models import Cita

router = APIRouter(prefix="/citas", tags=["Citas"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/disponibilidad")
def obtener_disponibilidad(
    fecha: str,
    db: Session = Depends(get_db)
):
    try:
        fecha_base = datetime.strptime(fecha, "%Y-%m-%d").date()
    except:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Usa YYYY-MM-DD")

    # horario de atención
    inicio_dia = datetime.combine(fecha_base, time(6, 0))
    fin_dia = datetime.combine(fecha_base, time(22, 0))

    # generar slots cada 30 minutos
    slots = []
    actual = inicio_dia

    while actual < fin_dia:
        slots.append({
            "hora": actual.strftime("%H:%M"),
            "estado": "disponible"
        })
        actual += timedelta(minutes=30)

    # obtener citas confirmadas de ese día
    citas_confirmadas = db.query(Cita).filter(
        Cita.estado == "confirmada",
        Cita.fecha_hora >= inicio_dia,
        Cita.fecha_hora < fin_dia
    ).all()

    # marcar slots ocupados
    horas_ocupadas = set([
        c.fecha_hora.strftime("%H:%M") for c in citas_confirmadas
    ])

    for slot in slots:
        if slot["hora"] in horas_ocupadas:
            slot["estado"] = "ocupado"

    return {
        "fecha": fecha,
        "slots": slots
    }