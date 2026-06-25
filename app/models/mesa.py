"""
Modelo Mesa — Mesa del restaurante.
"""
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship


class Mesa(Model, AuditMixin):
    """Mesa del restaurante."""

    __tablename__ = "mesas"

    id = Column(Integer, primary_key=True)
    numero = Column(Integer, unique=True, nullable=False)
    capacidad = Column(Integer, default=4)
    ubicacion = Column(String(100))
    activa = Column(Boolean, default=True)
    qr_code_url = Column(String(300))

    pedidos = relationship("Pedido", back_populates="mesa")

    def __repr__(self):
        return f"Mesa {self.numero}"
