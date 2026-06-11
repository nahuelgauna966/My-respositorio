from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.usuario import Usuario
from app.schemas.mesa import MesaCreate, MesaResponse, MesaUpdate
from app.services.auth_service import get_current_user
from app.services.mesa_service import (
    actualizar_estado_mesa,
    crear_mesa,
    get_all_mesas,
    get_mesa_by_id,
)

router = APIRouter(prefix="/mesas", tags=["Mesas"])


@router.get("/", response_model=list[MesaResponse])
async def listar_mesas(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Devuelve todas las mesas del local."""
    return await get_all_mesas(db)


@router.get("/{mesa_id}", response_model=MesaResponse)
async def obtener_mesa(
    mesa_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Devuelve una mesa por su ID."""
    mesa = await get_mesa_by_id(db, mesa_id)
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return mesa


@router.post("/", response_model=MesaResponse, status_code=201)
async def crear_nueva_mesa(
    data: MesaCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Crea una nueva mesa."""
    try:
        return await crear_mesa(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{mesa_id}", response_model=MesaResponse)
async def actualizar_mesa(
    mesa_id: int,
    data: MesaUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Actualiza el estado de una mesa."""
    mesa = await actualizar_estado_mesa(db, mesa_id, data)
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return mesa