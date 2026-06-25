"""
Modelo Configuracion — Configuraciones generales (clave-valor).
"""
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Integer, String, Text


class Configuracion(Model, AuditMixin):
    """Configuraciones generales (clave-valor)."""

    __tablename__ = "configuraciones"

    id = Column(Integer, primary_key=True)
    clave = Column(String(100), unique=True, nullable=False)
    valor = Column(Text)
    descripcion = Column(String(200))

    def __repr__(self):
        return f"<Config {self.clave}>"
