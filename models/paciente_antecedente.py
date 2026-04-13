from sqlalchemy import Column, Integer, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class PacienteAntecedente(Base):
    __tablename__ = "paciente_antecedentes"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    antecedente_id = Column(Integer, ForeignKey("antecedentes.id"))
    observacion = Column(Text)
    fecha_registro = Column(TIMESTAMP, default=datetime.utcnow)

    paciente = relationship("Paciente")
    antecedente = relationship("Antecedente", back_populates="pacientes")
    