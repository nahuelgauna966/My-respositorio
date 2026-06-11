from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.usuario import Usuario
from app.schemas.caja import CajaApertura, CajaCierre, CajaResponse
from app.services.auth_service import get_current_user, require_rol
from app.services.caja_service import abrir_caja, cerrar_caja, get_caja_actual

router = APIRouter(prefix="/caja", tags=["Caja"])


@router.get("/", response_model=CajaResponse | None)
async def estado_caja(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Devuelve la caja actual (abierta o la última cerrada)."""
    return await get_caja_actual(db)


@router.post("/apertura", response_model=CajaResponse, status_code=201)
async def apertura_caja(
    data: CajaApertura,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(require_rol("admin")),
):
    try:
        return await abrir_caja(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/cierre", response_model=CajaResponse)
async def cierre_caja(
    data: CajaCierre,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(require_rol("admin")),
):
    try:
        return await cerrar_caja(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))