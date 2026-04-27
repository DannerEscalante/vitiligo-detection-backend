from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Tratamiento(Base):
    __tablename__ = "tratamientos"

    id = Column(Integer, primary_key=True, index=True)

    historial_id = Column(Integer, ForeignKey("historiales_clinicos.id"))

    paciente_id = Column(Integer, ForeignKey("pacientes.id", ondelete="CASCADE"))
    doctor_id = Column(Integer, ForeignKey("doctores.id", ondelete="CASCADE"))
    tipo_tratamiento_id = Column(Integer, ForeignKey("tipos_tratamiento.id"))

    fecha_inicio = Column(DateTime, default=datetime.utcnow)
    fecha_fin = Column(DateTime, nullable=True)
    estado = Column(String, default="activo")

    notas = Column(Text)  # resultado final

    # relaciones
    historial = relationship("HistorialClinico", back_populates="tratamientos")
    paciente = relationship("Paciente", back_populates="tratamientos")
    doctor = relationship("Doctor", back_populates="tratamientos")
    tipo_tratamiento = relationship("TipoTratamiento", back_populates="tratamientos")

    predicciones = relationship("Prediccion", back_populates="tratamiento")