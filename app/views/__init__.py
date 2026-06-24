"""
Vistas Flask-AppBuilder para la app Restaurante.
Cada vista en su propio archivo dentro de este paquete.
"""

from app.views.categoria import CategoriaModelView
from app.views.plato import PlatoModelView
from app.views.mesa import MesaModelView
from app.views.cliente import ClienteModelView
from app.views.pedido import PedidoModelView, ItemPedidoModelView
from app.views.resena import ResenaModelView
from app.views.pago import PagoModelView
from app.views.configuracion import ConfiguracionModelView
from app.views.dashboard import DashboardView
from app.views.menu import MenuView
from app.views.errors import page_not_found, internal_error
from app.views.reportes import ReportesView, GraficosView


# API REST automática
api_models = {
    "categoria": CategoriaModelView,
    "plato": PlatoModelView,
    "mesa": MesaModelView,
    "cliente": ClienteModelView,
    "pedido": PedidoModelView,
    "item_pedido": ItemPedidoModelView,
    "resena": ResenaModelView,
    "pago": PagoModelView,
    "configuracion": ConfiguracionModelView,
}

__all__ = [
    "CategoriaModelView",
    "PlatoModelView",
    "MesaModelView",
    "ClienteModelView",
    "PedidoModelView",
    "ItemPedidoModelView",
    "ResenaModelView",
    "PagoModelView",
    "ConfiguracionModelView",
    "DashboardView",
    "MenuView",
    "page_not_found",
    "internal_error",
    "ReportesView",
    "GraficosView",
    "api_models",
]
