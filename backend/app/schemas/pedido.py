from typing import Literal
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from app.schemas.mesa import MesaResponse
from app.schemas.usuario import UsuarioResponse

ESTADOS_PEDIDO = Literal["pendiente", "en_preparacion", "listo", "entregado", "pagado", "cancelado"]


class DetallePedidoCreate(BaseModel):
    producto_id: int = Field(gt=0)
    cantidad: int = Field(ge=1)


class DetallePedidoResponse(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    subtotal: Decimal

    class Config:
        from_attributes = True


class PedidoCreate(BaseModel):
    mesa_id: int = Field(gt=0)
    detalles: list[DetallePedidoCreate] = Field(min_length=1)


class PedidoUpdate(BaseModel):
    estado: ESTADOS_PEDIDO


class PedidoResponse(BaseModel):
    id: int
    estado: str
    total: Decimal
    fecha: datetime
    mesa: MesaResponse
    usuario: UsuarioResponse
    detalles: list[DetallePedidoResponse]

    class Config:
        from_attributes = True