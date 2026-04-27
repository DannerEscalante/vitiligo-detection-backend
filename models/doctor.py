from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from core.database import Base

class Doctor(Base):
    __tablename__ = "doctores"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True)
    nombre = Column(String)
    fecha_nacimiento = Column(Date, nullable=True)
    sexo = Column(String, nullable=True)

    usuario = relationship("Usuario")
    historiales = relationship("HistorialClinico", back_populates="doctor")
    citas = relationship("Cita", back_populates="doctor", cascade="all, delete")
    tratamientos = relationship("Tratamiento", back_populates="doctor")