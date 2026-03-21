from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Enfermedad(Base):
    __tablename__ = "enfermedades"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)

    pacientes = relationship("PacienteEnfermedad", back_populates="enfermedad")