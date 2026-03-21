from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True)
    nombre = Column(String)
    fecha_nacimiento = Column(Date)
    sexo = Column(String)

    usuario = relationship("Usuario")
    imagenes = relationship("Imagen", back_populates="paciente")
    historiales = relationship("HistorialClinico", back_populates="paciente")