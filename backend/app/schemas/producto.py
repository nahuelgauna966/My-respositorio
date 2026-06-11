from decimal import Decimal
from pydantic import BaseModel, Field
from app.schemas.categoria import CategoriaResponse


class ProductoCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=500)
    precio: Decimal = Field(gt=0, decimal_places=2)
    stock: int = Field(default=0, ge=0)
    disponible: bool = True
    categoria_id: int = Field(gt=0)


class ProductoUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=500)
    precio: Decimal | None = Field(default=None, gt=0, decimal_places=2)
    stock: int | None = Field(default=None, ge=0)
    disponible: bool | None = None
    categoria_id: int | None = Field(default=None, gt=0)


class ProductoResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    precio: Decimal
    stock: int
    disponible: bool
    categoria: CategoriaResponse

    class Config:
        from_attributes = True