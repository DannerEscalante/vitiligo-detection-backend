from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class PacienteEnfermedad(Base):
    __tablename__ = "paciente_enfermedades"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    enfermedad_id = Column(Integer, ForeignKey("enfermedades.id"))

    enfermedad = relationship("Enfermedad", back_populates="pacientes")