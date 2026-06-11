from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# El "motor" — es la conexión real a la base de datos
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
)

# La "fábrica de sesiones" — cada request HTTP abre una sesión y la cierra al terminar
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Clase base de la que heredan todos los modelos
class Base(DeclarativeBase):
    pass


# Dependencia de FastAPI — abre una sesión por request y la cierra automáticamente
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise