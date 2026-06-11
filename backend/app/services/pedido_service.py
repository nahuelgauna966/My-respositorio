from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.pedido import Pedido
from app.models.detalle_pedido import DetallePedido
from app.models.mesa import Mesa
from app.services.producto_service import get_producto_by_id
from app.schemas.pedido import PedidoCreate, PedidoUpdate


async def get_pedidos_activos(db: AsyncSession) -> list[Pedido]:
    """Devuelve pedidos que no están pagados ni cancelados."""
    result = await db.execute(
        select(Pedido)
        .options(
            selectinload(Pedido.mesa),
            selectinload(Pedido.usuario),
            selectinload(Pedido.detalles),
        )
        .where(Pedido.estado.notin_(["pagado", "cancelado"]))
    )
    return result.scalars().all()


async def get_pedido_by_id(db: AsyncSession, pedido_id: int) -> Pedido | None:
    result = await db.execute(
        select(Pedido)
        .options(
            selectinload(Pedido.mesa),
            selectinload(Pedido.usuario),
            selectinload(Pedido.detalles),
            selectinload(Pedido.pagos),
        )
        .where(Pedido.id == pedido_id)
    )
    return result.scalar_one_or_none()


async def crear_pedido(
    db: AsyncSession, data: PedidoCreate, usuario_id: int
) -> Pedido:
    """Crea un pedido y calcula el total automáticamente."""
    # Verificar que la mesa existe
    result_mesa = await db.execute(select(Mesa).where(Mesa.id == data.mesa_id))
    mesa = result_mesa.scalar_one_or_none()
    if not mesa:
        raise ValueError(f"Mesa {data.mesa_id} no encontrada")
    if mesa.estado == "ocupada":
        raise ValueError(f"La mesa {mesa.numero} ya está ocupada")

    total = Decimal("0")
    detalles = []

    for item in data.detalles:
        producto = await get_producto_by_id(db, item.producto_id)
        if not producto:
            raise ValueError(f"Producto {item.producto_id} no encontrado")
        if not producto.disponible:
            raise ValueError(f"El producto '{producto.nombre}' no está disponible")
        if producto.stock < item.cantidad:
            raise ValueError(
                f"Stock insuficiente para '{producto.nombre}': "
                f"disponible {producto.stock}, solicitado {item.cantidad}"
            )

        subtotal = producto.precio * item.cantidad
        total += subtotal

        detalles.append(
            DetallePedido(
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                subtotal=subtotal,
            )
        )

    pedido = Pedido(
        mesa_id=data.mesa_id,
        usuario_id=usuario_id,
        total=total,
        detalles=detalles,
    )
    db.add(pedido)
    await db.flush()

    mesa.estado = "ocupada"

    return await get_pedido_by_id(db, pedido.id)


async def actualizar_estado_pedido(
    db: AsyncSession, pedido_id: int, data: PedidoUpdate
) -> Pedido | None:
    pedido = await get_pedido_by_id(db, pedido_id)
    if not pedido:
        return None
    if pedido.estado in ("pagado", "cancelado"):
        raise ValueError(f"No se puede modificar un pedido en estado '{pedido.estado}'")
    pedido.estado = data.estado

    # Si el pedido se paga, liberar la mesa
    if data.estado == "pagado":
        result = await db.execute(select(Mesa).where(Mesa.id == pedido.mesa_id))
        mesa = result.scalar_one_or_none()
        if mesa:
            mesa.estado = "libre"

    await db.flush()
    return pedido