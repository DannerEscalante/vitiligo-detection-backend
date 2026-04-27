from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Imagen(Base):
    __tablename__ = "imagenes"

    id = Column(Integer, primary_key=True, index=True)

    paciente_id = Column(Integer, ForeignKey("pacientes.id", ondelete="CASCADE"))

    url_imagen = Column(String)
    fecha = Column(DateTime, default=datetime.utcnow)

    # relación 1 a 1 con predicción
    prediccion_id = Column(Integer, ForeignKey("predicciones.id"))

    prediccion = relationship("Prediccion", back_populates="imagen")