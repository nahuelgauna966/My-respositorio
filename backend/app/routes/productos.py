from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.usuario import Usuario
from app.schemas.producto import ProductoCreate, ProductoResponse, ProductoUpdate
from app.services.auth_service import get_current_user, require_rol
from app.services.producto_service import (
    actualizar_producto as actualizar_producto_svc,
    crear_producto,
    eliminar_producto as eliminar_producto_svc,
    get_all_productos,
    get_producto_by_id,
)

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("/", response_model=list[ProductoResponse])
async def listar_productos(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    return await get_all_productos(db)


@router.get("/{producto_id}", response_model=ProductoResponse)
async def obtener_producto(
    producto_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    producto = await get_producto_by_id(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.post("/", response_model=ProductoResponse, status_code=201)
async def crear_nuevo_producto(
    data: ProductoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(require_rol("admin")),
):
    return await crear_producto(db, data)


@router.patch("/{producto_id}", response_model=ProductoResponse)
async def actualizar_producto(
    producto_id: int,
    data: ProductoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(require_rol("admin")),
):
    producto = await actualizar_producto_svc(db, producto_id, data)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.delete("/{producto_id}", status_code=204)
async def eliminar_producto(
    producto_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(require_rol("admin")),
):
    eliminado = await eliminar_producto_svc(db, producto_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")