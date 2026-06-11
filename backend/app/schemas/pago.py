from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class PagoCreate(BaseModel):
    pedido_id: int
    metodo_pago: str  # efectivo, debito, credito, transferencia, mercado_pago
    monto: Decimal


class PagoResponse(BaseModel):
    id: int
    pedido_id: int
    metodo_pago: str
    monto: Decimal
    fecha: datetime

    class Config:
        from_attributes = True