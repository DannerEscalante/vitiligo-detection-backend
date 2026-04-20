from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class HistorialClinico(Base):
    __tablename__ = "historiales_clinicos"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    doctor_id = Column(Integer, ForeignKey("doctores.id"))
    prediccion_id = Column(Integer, ForeignKey("predicciones.id"), nullable=True)
    notas = Column(Text)
    diagnostico = Column(Text)
    fecha = Column(TIMESTAMP, default=datetime.utcnow)
    cita_id = Column(Integer, ForeignKey("citas.id"), nullable=True)


    prediccion = relationship("Prediccion")
    paciente = relationship("Paciente", back_populates="historiales")
    doctor = relationship("Doctor", back_populates="historiales")
    
    
    cita = relationship("Cita", back_populates="historial")
    tratamiento_id = Column(Integer, ForeignKey("tratamientos.id"), nullable=True)
    tratamiento = relationship("Tratamiento", back_populates="historiales")