from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Prediccion(Base):
    __tablename__ = "predicciones"

    id = Column(Integer, primary_key=True, index=True)
    imagen_id = Column(Integer, ForeignKey("imagenes.id"))
    resultado = Column(String)
    confianza = Column(DECIMAL(5,2))
    fecha_prediccion = Column(TIMESTAMP, default=datetime.utcnow)

    imagen = relationship("Imagen", back_populates="predicciones")