from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.producto import Producto
from app.schemas.producto import ProductoCreate, ProductoUpdate


async def get_all_productos(db: AsyncSession) -> list[Producto]:
    """Devuelve todos los productos con su categoría incluida."""
    result = await db.execute(
        select(Producto).options(selectinload(Producto.categoria))
    )
    return result.scalars().all()


async def get_producto_by_id(db: AsyncSession, producto_id: int) -> Producto | None:
    result = await db.execute(
        select(Producto)
        .options(selectinload(Producto.categoria))
        .where(Producto.id == producto_id)
    )
    return result.scalar_one_or_none()


async def crear_producto(db: AsyncSession, data: ProductoCreate) -> Producto:
    producto = Producto(**data.model_dump())
    db.add(producto)
    await db.flush()
    return await get_producto_by_id(db, producto.id)


async def actualizar_producto(
    db: AsyncSession, producto_id: int, data: ProductoUpdate
) -> Producto | None:
    producto = await get_producto_by_id(db, producto_id)
    if not producto:
        return None
    # Solo actualiza los campos que llegaron (los que no son None)
    for campo, valor in data.model_dump(exclude_none=True).items():
        setattr(producto, campo, valor)
    await db.flush()
    return producto


async def eliminar_producto(db: AsyncSession, producto_id: int) -> bool:
    producto = await get_producto_by_id(db, producto_id)
    if not producto:
        return False
    await db.delete(producto)
    return True