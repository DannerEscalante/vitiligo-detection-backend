from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Imagen(Base):
    __tablename__ = "imagenes"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    url_imagen = Column(Text)
    fecha_subida = Column(TIMESTAMP, default=datetime.utcnow)

    paciente = relationship("Paciente", back_populates="imagenes")
    predicciones = relationship("Prediccion", back_populates="imagen")