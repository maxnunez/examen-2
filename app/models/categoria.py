"""
Modelo Categoria — Categoría de platos del menú.
"""
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship


class Categoria(Model, AuditMixin):
    """Categoría de platos del menú."""

    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text)
    icono = Column(String(50))
    activo = Column(Boolean, default=True)
    orden = Column(Integer, default=0)

    platos = relationship("Plato", back_populates="categoria")

    def __repr__(self):
        return self.nombre
