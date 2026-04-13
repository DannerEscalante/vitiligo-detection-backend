from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from core.database import Base

class Antecedente(Base):
    __tablename__ = "antecedentes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String)  
    descripcion = Column(Text)

    pacientes = relationship("PacienteAntecedente", back_populates="antecedente")