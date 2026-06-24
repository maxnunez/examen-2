from flask import current_app
from flask_appbuilder.security.sqla.models import User
from flask_appbuilder.security.sqla.manager import SecurityManager
from typing import Optional


ROL_ADMIN = "Admin"
ROL_MESERO = "Mesero"
ROL_COCINERO = "Cocinero"
ROL_CAJERO = "Cajero"
ROL_CLIENTE = "Cliente"

ALL_ROLES = [ROL_ADMIN, ROL_MESERO, ROL_COCINERO, ROL_CAJERO, ROL_CLIENTE]


def setup_roles_permissions(appbuilder):
    """Asigna permisos específicos a cada rol no-admin."""
    sm = appbuilder.sm
    session = sm.session

    permisos_rol = {
        ROL_ADMIN: {
            "menu_access": [
                "Reportes", "Ventas", "Platos mas vendidos", "Clientes frecuentes",
                "Graficos", "Ingresos", "Estados de pedidos", "Platos por categoria",
            ],
            "acciones_por_vista": {
                "ReportesView": ["can_ventas", "can_platos", "can_clientes"],
                "GraficosView": ["can_ingresos", "can_estados", "can_categorias"],
            },
        },
        ROL_MESERO: {
            "menu_access": [
                "Principal", "Dashboard", "Menu Publico",
                "Menu", "Categorias", "Platos",
                "Operaciones", "Mesas", "Pedidos", "Items Pedido",
                "CRM", "Clientes",
                "Reportes", "Ventas", "Platos mas vendidos", "Clientes frecuentes",
            ],
            "acciones_por_vista": {
                "DashboardView": ["can_index"],
                "CategoriaModelView": ["can_list", "can_show"],
                "PlatoModelView": ["can_list", "can_show"],
                "MesaModelView": ["can_list", "can_add", "can_edit", "can_show"],
                "ClienteModelView": ["can_list", "can_add", "can_edit", "can_show"],
                "PedidoModelView": ["can_list", "can_add", "can_edit", "can_show"],
                "ItemPedidoModelView": ["can_list", "can_add", "can_edit", "can_show"],
                "ReportesView": ["can_ventas", "can_platos", "can_clientes"],
            },
        },
        ROL_COCINERO: {
            "menu_access": [
                "Principal", "Dashboard",
                "Operaciones", "Pedidos", "Items Pedido",
            ],
            "acciones_por_vista": {
                "DashboardView": ["can_index"],
                "PedidoModelView": ["can_list", "can_show", "can_edit"],
                "ItemPedidoModelView": ["can_list", "can_show", "can_edit"],
            },
        },
        ROL_CAJERO: {
            "menu_access": [
                "Principal", "Dashboard", "Menu Publico",
                "Menu", "Categorias", "Platos",
                "Operaciones", "Pedidos", "Items Pedido",
                "CRM", "Clientes",
                "Finanzas", "Pagos",
                "Reportes", "Ventas", "Platos mas vendidos", "Clientes frecuentes",
                "Graficos", "Ingresos", "Estados de pedidos", "Platos por categoria",
            ],
            "acciones_por_vista": {
                "DashboardView": ["can_index"],
                "CategoriaModelView": ["can_list", "can_show"],
                "PlatoModelView": ["can_list", "can_show"],
                "ClienteModelView": ["can_list", "can_show"],
                "PedidoModelView": ["can_list", "can_show"],
                "ItemPedidoModelView": ["can_list", "can_show"],
                "PagoModelView": ["can_list", "can_add", "can_edit", "can_show"],
                "ReportesView": ["can_ventas", "can_platos", "can_clientes"],
                "GraficosView": ["can_ingresos", "can_estados", "can_categorias"],
            },
        },
        ROL_CLIENTE: {
            "menu_access": [
                "Principal", "Menu Publico",
            ],
            "acciones_por_vista": {
                "MenuView": ["can_index"],
            },
        },
    }

    for nombre_rol, config in permisos_rol.items():
        role = sm.find_role(nombre_rol)
        if not role:
            current_app.logger.warning(f"Rol '{nombre_rol}' no encontrado, saltando permisos")
            continue

        # menu_access sobre nombres de menú (DisplayName)
        for nombre_menu in config["menu_access"]:
            pv = sm.find_permission_view_menu("menu_access", nombre_menu)
            if pv and pv not in role.permissions:
                sm.add_permission_role(role, pv)

        # permisos CRUD sobre clases de vista (ModelViewName)
        for vista, acciones in config["acciones_por_vista"].items():
            for accion in acciones:
                pv = sm.find_permission_view_menu(accion, vista)
                if pv and pv not in role.permissions:
                    sm.add_permission_role(role, pv)

    session.commit()


class CustomSecurityManager(SecurityManager):
    """Security Manager personalizado con roles de restaurante."""

    def __init__(self, appbuilder):
        super().__init__(appbuilder)
        self._create_default_roles()

    def _create_default_roles(self) -> None:
        from flask_appbuilder.security.sqla.models import Role

        for role_name in ALL_ROLES:
            existing = (
                self.session.query(Role)
                .filter(Role.name == role_name)
                .first()
            )
            if not existing:
                role = Role(name=role_name)
                self.session.add(role)
                self.session.commit()
                current_app.logger.info(f"Rol creado: {role_name}")
            else:
                current_app.logger.debug(f"Rol ya existe: {role_name}")

    def auth_user_db(self, username, password):
        return super().auth_user_db(username, password)

    def get_user_by_username(self, username: str) -> Optional[User]:
        return (
            self.session.query(User)
            .filter(User.username == username)
            .first()
        )

    def register_views(self):
        super().register_views()

    def add_user(self, username, first_name, last_name, email, role, password):
        return super().add_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=role,
            password=password,
        )
