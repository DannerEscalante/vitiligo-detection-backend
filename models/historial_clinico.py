from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class HistorialClinico(Base):
    __tablename__ = "historiales_clinicos"

    id = Column(Integer, primary_key=True, index=True)

    paciente_id = Column(Integer, ForeignKey("pacientes.id", ondelete="CASCADE"))
    doctor_id = Column(Integer, ForeignKey("doctores.id", ondelete="CASCADE"))
    cita_id = Column(Integer, ForeignKey("citas.id"))

    diagnostico = Column(Text)
    fecha = Column(DateTime, default=datetime.utcnow)

    # relaciones
    paciente = relationship("Paciente", back_populates="historiales")
    doctor = relationship("Doctor", back_populates="historiales")
    cita = relationship("Cita")

    tratamientos = relationship("Tratamiento", back_populates="historial")