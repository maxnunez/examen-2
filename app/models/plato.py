"""
Modelo Plato — Plato del menú.
"""
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import relationship


class Plato(Model, AuditMixin):
    """Plato del menú."""

    __tablename__ = "platos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text)
    imagen_url = Column(String(300))
    precio = Column(Numeric(10, 2), nullable=False)
    costo = Column(Numeric(10, 2), default=0)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    disponible = Column(Boolean, default=True)
    destacado = Column(Boolean, default=False)
    tiempo_preparacion_min = Column(Integer, default=15)
    calorias = Column(Integer)
    es_vegetariano = Column(Boolean, default=False)
    es_vegano = Column(Boolean, default=False)
    sin_gluten = Column(Boolean, default=False)

    categoria = relationship("Categoria", back_populates="platos")
    items_pedido = relationship("ItemPedido", back_populates="plato")

    def __repr__(self):
        return self.nombre

    @property
    def margen(self):
        costo = float(self.costo or 0)
        if costo > 0:
            return round((float(self.precio) - costo) / costo * 100, 1)
        return 100.0
