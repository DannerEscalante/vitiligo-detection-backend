from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from core.database import Base


class TipoTratamiento(Base):
    __tablename__ = "tipos_tratamiento"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(Text)

    # relación
    tratamientos = relationship("Tratamiento", back_populates="tipo_tratamiento")