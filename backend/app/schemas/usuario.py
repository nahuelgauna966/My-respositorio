from typing import Literal
from pydantic import BaseModel, EmailStr, Field


# Lo que llega cuando se crea un usuario
class UsuarioCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)
    rol: Literal["admin", "mozo"]


# Lo que devuelve la API (nunca incluye el password)
class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str
    rol: str
    activo: bool

    class Config:
        from_attributes = True  # Permite convertir objetos SQLAlchemy a este schema


# Lo que llega en el login
class LoginRequest(BaseModel):
    email: str
    password: str


# Lo que devuelve el login
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse