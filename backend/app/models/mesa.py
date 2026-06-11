from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Mesa(Base):
    __tablename__ = "mesas"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, unique=True, nullable=False)
    estado = Column(String(30), default="libre")
    # Estados: libre, ocupada, reservada, pendiente_cobro, en_limpieza

    # Una mesa tiene muchos pedidos
    pedidos = relationship("Pedido", back_populates="mesa")