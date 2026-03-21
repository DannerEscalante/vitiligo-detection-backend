from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String, nullable=False)