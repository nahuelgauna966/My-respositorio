from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class CajaApertura(BaseModel):
    monto_inicial: Decimal


class CajaCierre(BaseModel):
    monto_final: Decimal


class CajaResponse(BaseModel):
    id: int
    fecha_apertura: datetime
    fecha_cierre: datetime | None
    monto_inicial: Decimal
    monto_final: Decimal | None
    estado: str

    class Config:
        from_attributes = True