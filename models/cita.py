from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base


class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id", ondelete="CASCADE"))
    doctor_id = Column(Integer, ForeignKey("doctores.id", ondelete="CASCADE"))
    fecha_hora = Column(DateTime, nullable=False)
    estado = Column(String, default="pendiente")
    motivo = Column(Text)
    observaciones = Column(Text)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    duracion = Column(Integer, default=30)  # minutos
    prediccion_id = Column(Integer, ForeignKey("predicciones.id"), nullable=True)

    
    # relaciones
    paciente = relationship("Paciente", back_populates="citas")
    doctor = relationship("Doctor", back_populates="citas")
    historial = relationship("HistorialClinico", back_populates="cita", uselist=False)
    prediccion = relationship("Prediccion")
    
    
    

    
    