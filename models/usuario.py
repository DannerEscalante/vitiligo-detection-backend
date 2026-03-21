from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    contrasena = Column(String, nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id"))
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)

    rol = relationship("Rol")