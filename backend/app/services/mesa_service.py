from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.mesa import Mesa
from app.schemas.mesa import MesaCreate, MesaUpdate


async def get_all_mesas(db: AsyncSession) -> list[Mesa]:
    """Devuelve todas las mesas ordenadas por número."""
    result = await db.execute(select(Mesa).order_by(Mesa.numero))
    return result.scalars().all()


async def get_mesa_by_id(db: AsyncSession, mesa_id: int) -> Mesa | None:
    """Busca una mesa por su ID."""
    result = await db.execute(select(Mesa).where(Mesa.id == mesa_id))
    return result.scalar_one_or_none()


async def crear_mesa(db: AsyncSession, data: MesaCreate) -> Mesa:
    """Crea una nueva mesa."""
    result = await db.execute(select(Mesa).where(Mesa.numero == data.numero))
    if result.scalar_one_or_none():
        raise ValueError(f"Ya existe una mesa con el número {data.numero}")
    mesa = Mesa(numero=data.numero)
    db.add(mesa)
    await db.flush()
    return mesa


async def actualizar_estado_mesa(
    db: AsyncSession, mesa_id: int, data: MesaUpdate
) -> Mesa | None:
    """Actualiza el estado de una mesa."""
    mesa = await get_mesa_by_id(db, mesa_id)
    if not mesa:
        return None
    mesa.estado = data.estado
    await db.flush()
    return mesa