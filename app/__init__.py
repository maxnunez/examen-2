"""
Aplicacion Restaurante — Flask + Flask-AppBuilder
"""

import logging
from datetime import datetime

from flask import Flask
from flask_appbuilder import AppBuilder
from flask_sqlalchemy import SQLAlchemy
from config import config


db = SQLAlchemy()
appbuilder = AppBuilder()


def create_app(config_name: str = "default") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    app.config["FAB_SECURITY_MANAGER_CLASS"] = "app.security.CustomSecurityManager"

    logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    logging.getLogger().setLevel(logging.WARNING)
    app.logger.setLevel(logging.INFO)

    @app.context_processor
    def inject_now():
        return {"now": datetime.utcnow}

    @app.context_processor
    def inject_appbuilder():
        return {"appbuilder": appbuilder}

    with app.app_context():
        appbuilder.init_app(app, db.session)
        register_views()
        from flask_appbuilder.models.sqla import Base
        Base.metadata.create_all(db.engine)
        from app.security import setup_roles_permissions
        setup_roles_permissions(appbuilder)
        register_error_handlers(app)

    return app


def register_views() -> None:
    from app.views import (
        CategoriaModelView, PlatoModelView, MesaModelView,
        ClienteModelView, PedidoModelView, ItemPedidoModelView,
        ResenaModelView, PagoModelView, ConfiguracionModelView,
        DashboardView, MenuView,
    )
    from app.views.reportes import ReportesView, GraficosView

    appbuilder.add_view(DashboardView(), "Dashboard", category="Principal", category_icon="fa-home")
    appbuilder.add_view(MenuView(), "Menu Publico", category="Principal", category_icon="fa-home")

    appbuilder.add_view(CategoriaModelView(), "Categorias", category="Menu", category_icon="fa-list")
    appbuilder.add_view(PlatoModelView(), "Platos", category="Menu", category_icon="fa-utensils")
    appbuilder.add_view(MesaModelView(), "Mesas", category="Operaciones", category_icon="fa-chair")
    appbuilder.add_view(PedidoModelView(), "Pedidos", category="Operaciones", category_icon="fa-clipboard-list")
    appbuilder.add_view(ItemPedidoModelView(), "Items Pedido", category="Operaciones", category_icon="fa-list-ol")
    appbuilder.add_view(ClienteModelView(), "Clientes", category="CRM", category_icon="fa-users")
    appbuilder.add_view(ResenaModelView(), "Resenas", category="CRM", category_icon="fa-star")
    appbuilder.add_view(PagoModelView(), "Pagos", category="Finanzas", category_icon="fa-dollar-sign")
    appbuilder.add_view(ConfiguracionModelView(), "Configuracion", category="Sistema", category_icon="fa-cog")

    appbuilder.add_view(ReportesView(), "Ventas", category="Reportes", category_icon="fa-chart-line")
    appbuilder.add_link("Platos mas vendidos", href="/reportes/platos/", category="Reportes", icon="fa-trophy")
    appbuilder.add_link("Clientes frecuentes", href="/reportes/clientes/", category="Reportes", icon="fa-users")
    appbuilder.add_view(GraficosView(), "Ingresos", category="Graficos", category_icon="fa-chart-bar")
    appbuilder.add_link("Estados de pedidos", href="/graficos/estados/", category="Graficos", icon="fa-chart-pie")
    appbuilder.add_link("Platos por categoria", href="/graficos/categorias/", category="Graficos", icon="fa-chart-simple")


def register_error_handlers(app) -> None:
    from app.views import page_not_found, internal_error
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_error)
