from fastapi import APIRouter
from app.routes import auth, mesas, productos, pedidos, caja

# Router principal que agrupa todos los routers
api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router)
api_router.include_router(mesas.router)
api_router.include_router(productos.router)
api_router.include_router(pedidos.router)
api_router.include_router(caja.router)