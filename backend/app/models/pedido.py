from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    mesa_id = Column(Integer, ForeignKey("mesas.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    estado = Column(String(30), default="pendiente")
    # Estados: pendiente, en_preparacion, listo, entregado, pagado, cancelado
    total = Column(Numeric(10, 2), default=0)
    fecha = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    mesa = relationship("Mesa", back_populates="pedidos")
    usuario = relationship("Usuario")
    detalles = relationship("DetallePedido", back_populates="pedido")
    pagos = relationship("Pago", back_populates="pedido")