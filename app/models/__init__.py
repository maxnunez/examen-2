"""
Modelos SQLAlchemy para la aplicación Restaurante.
Cada modelo en su propio archivo dentro de este paquete.
"""

from app.models.enums import EstadoPedido
from app.models.categoria import Categoria
from app.models.plato import Plato
from app.models.mesa import Mesa
from app.models.cliente import Cliente
from app.models.pedido import Pedido, ItemPedido
from app.models.resena import Resena
from app.models.pago import Pago
from app.models.configuracion import Configuracion

__all__ = [
    "EstadoPedido",
    "Categoria",
    "Plato",
    "Mesa",
    "Cliente",
    "Pedido",
    "ItemPedido",
    "Resena",
    "Pago",
    "Configuracion",
]
