from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.caja import Caja
from app.schemas.caja import CajaApertura, CajaCierre


async def get_caja_abierta(db: AsyncSession) -> Caja | None:
    """Busca si hay una caja abierta actualmente."""
    result = await db.execute(
        select(Caja).where(Caja.estado == "abierta")
    )
    return result.scalar_one_or_none()


async def get_caja_actual(db: AsyncSession) -> Caja | None:
    """Devuelve la caja más reciente (abierta o cerrada)."""
    result = await db.execute(
        select(Caja).order_by(Caja.id.desc()).limit(1)
    )
    return result.scalar_one_or_none()


async def abrir_caja(db: AsyncSession, data: CajaApertura) -> Caja:
    """Abre la caja. Falla si ya hay una abierta."""
    caja_existente = await get_caja_abierta(db)
    if caja_existente:
        raise ValueError("Ya hay una caja abierta")

    caja = Caja(monto_inicial=data.monto_inicial)
    db.add(caja)
    await db.flush()
    return caja


async def cerrar_caja(db: AsyncSession, data: CajaCierre) -> Caja:
    """Cierra la caja abierta con el monto final."""
    caja = await get_caja_abierta(db)
    if not caja:
        raise ValueError("No hay una caja abierta")

    caja.fecha_cierre = datetime.utcnow()
    caja.monto_final = data.monto_final
    caja.estado = "cerrada"
    await db.flush()
    return caja