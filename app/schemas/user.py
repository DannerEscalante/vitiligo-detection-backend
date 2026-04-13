from pydantic import BaseModel, EmailStr, Field

class UsuarioCreate(BaseModel):
    email: EmailStr
    contrasena: str = Field(min_length=6, max_length=50)
    rol_id: int