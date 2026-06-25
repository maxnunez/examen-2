"""
Modelo Resena — Reseña / calificación del cliente.
"""
from datetime import datetime
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Resena(Model, AuditMixin):
    """Reseña / calificación del cliente."""

    __tablename__ = "resenas"

    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    calificacion = Column(Integer, nullable=False)
    comentario = Column(Text)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)

    pedido = relationship("Pedido", back_populates="resena")
    cliente = relationship("Cliente", back_populates="resenas")

    def __repr__(self):
        return f"<Resena {self.calificacion}*"
