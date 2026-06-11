from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, Numeric, String
from app.core.database import Base


class Caja(Base):
    __tablename__ = "cajas"

    id = Column(Integer, primary_key=True, index=True)
    fecha_apertura = Column(DateTime, default=datetime.utcnow)
    fecha_cierre = Column(DateTime, nullable=True)
    monto_inicial = Column(Numeric(10, 2), nullable=False)
    monto_final = Column(Numeric(10, 2), nullable=True)
    estado = Column(String(20), default="abierta")  # abierta, cerrada