"""
Modelos Pedido e ItemPedido.
"""
from datetime import datetime
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.models.enums import EstadoPedido
from app.models.cliente import Cliente
from app.models.mesa import Mesa


class Pedido(Model, AuditMixin):
    """Pedido / orden del restaurante."""

    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True)
    codigo = Column(String(20), unique=True, nullable=False)
    estado = Column(String(20), default=EstadoPedido.PENDIENTE)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    mesa_id = Column(Integer, ForeignKey("mesas.id"))
    usuario_mesero_id = Column(Integer, ForeignKey("ab_user.id"))
    subtotal = Column(Numeric(12, 2), default=0)
    impuesto = Column(Numeric(12, 2), default=0)
    descuento = Column(Numeric(12, 2), default=0)
    total = Column(Numeric(12, 2), default=0)
    metodo_pago = Column(String(30))
    notas_cocina = Column(Text)
    atendido_en = Column(DateTime)
    pagado_en = Column(DateTime)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)

    cliente = relationship("Cliente", back_populates="pedidos")
    mesa = relationship("Mesa", back_populates="pedidos")
    usuario_mesero = relationship(
        "User", foreign_keys=[usuario_mesero_id]
    )
    items = relationship("ItemPedido", back_populates="pedido",
                         cascade="all, delete-orphan")
    resena = relationship("Resena", back_populates="pedido", uselist=False)

    def __repr__(self):
        return self.codigo


class ItemPedido(Model, AuditMixin):
    """Línea de detalle de un pedido."""

    __tablename__ = "items_pedido"

    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    plato_id = Column(Integer, ForeignKey("platos.id"), nullable=False)
    cantidad = Column(Integer, default=1, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    notas = Column(String(200))
    entregado = Column(Boolean, default=False)
    entregado_en = Column(DateTime)

    pedido = relationship("Pedido", back_populates="items")
    plato = relationship("Plato", back_populates="items_pedido")

    def __repr__(self):
        return (
            f"<ItemPedido "
            f"{self.plato.nombre if self.plato else '?'} x{self.cantidad}>"
        )
