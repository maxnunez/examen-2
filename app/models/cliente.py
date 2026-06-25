"""
Modelo Cliente — Cliente registrado.
"""
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Integer, String, Text, Boolean, Date
from sqlalchemy.orm import relationship


class Cliente(Model, AuditMixin):
    """Cliente registrado."""

    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(120), nullable=False)
    apellido = Column(String(120))
    telefono = Column(String(20))
    email = Column(String(120))
    direccion = Column(Text)
    notas = Column(Text)
    fecha_nacimiento = Column(Date)
    total_pedidos = Column(Integer, default=0)
    cliente_vip = Column(Boolean, default=False)

    pedidos = relationship("Pedido", back_populates="cliente")
    resenas = relationship("Resena", back_populates="cliente")

    def __repr__(self):
        return self.nombre_completo

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido or ''}".strip()
