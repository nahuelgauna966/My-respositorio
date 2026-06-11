from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base
from app.routes import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Al iniciar la app — crea las tablas si no existen
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Al apagar la app — cierra las conexiones
    await engine.dispose()


app = FastAPI(
    title="CafecitoApp API",
    description="Sistema de Administración de Cafetería",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — permite que el Frontend (Next.js en puerto 3000) hable con el Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar todas las rutas
app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "CafecitoApp API funcionando", "version": "1.0.0"}