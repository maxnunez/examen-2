"""
Modelo Pago — Registro de pagos.
"""
from datetime import datetime
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Pago(Model, AuditMixin):
    """Registro de pagos."""

    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    monto = Column(Numeric(12, 2), nullable=False)
    metodo = Column(String(30))
    referencia = Column(String(100))
    fecha = Column(DateTime, default=datetime.utcnow)

    pedido = relationship("Pedido")

    def __repr__(self):
        return f"${self.monto} - {self.metodo}"
