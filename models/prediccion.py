from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class Prediccion(Base):
    __tablename__ = "predicciones"

    id = Column(Integer, primary_key=True, index=True)

    tratamiento_id = Column(Integer, ForeignKey("tratamientos.id"))

    resultado = Column(String)
    confianza = Column(Float)

    # relaciones
    tratamiento = relationship("Tratamiento", back_populates="predicciones")
    imagen = relationship("Imagen", back_populates="prediccion", uselist=False)