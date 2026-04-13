from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class Doctor(Base):
    __tablename__ = "doctores"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True)
    nombre = Column(String)
    especialidad = Column(String)
    numero_colegiatura = Column(String)

    usuario = relationship("Usuario")
    historiales = relationship("HistorialClinico", back_populates="doctor")