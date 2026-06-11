from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.usuario import Usuario
from app.schemas.pedido import PedidoCreate, PedidoResponse, PedidoUpdate
from app.services.auth_service import get_current_user
from app.services.pedido_service import (
    actualizar_estado_pedido,
    crear_pedido,
    get_pedido_by_id,
    get_pedidos_activos,
)

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.get("/", response_model=list[PedidoResponse])
async def listar_pedidos_activos(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Devuelve todos los pedidos activos (no pagados ni cancelados)."""
    return await get_pedidos_activos(db)


@router.get("/{pedido_id}", response_model=PedidoResponse)
async def obtener_pedido(
    pedido_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    pedido = await get_pedido_by_id(db, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido


@router.post("/", response_model=PedidoResponse, status_code=201)
async def crear_nuevo_pedido(
    data: PedidoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    try:
        return await crear_pedido(db, data, usuario_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{pedido_id}", response_model=PedidoResponse)
async def actualizar_pedido(
    pedido_id: int,
    data: PedidoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    pedido = await actualizar_estado_pedido(db, pedido_id, data)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido