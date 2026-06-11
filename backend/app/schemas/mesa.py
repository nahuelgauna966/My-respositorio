from typing import Literal
from pydantic import BaseModel, Field

ESTADOS_MESA = Literal["libre", "ocupada", "reservada", "pendiente_cobro", "en_limpieza"]


class MesaCreate(BaseModel):
    numero: int = Field(gt=0)


class MesaUpdate(BaseModel):
    estado: ESTADOS_MESA


class MesaResponse(BaseModel):
    id: int
    numero: int
    estado: str

    class Config:
        from_attributes = True