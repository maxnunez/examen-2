"""
Vista pública del Menú / Carta.
"""
from flask_appbuilder import BaseView, expose
from app import appbuilder, db
from app.models import Categoria, Plato


class MenuView(BaseView):
    """Menú público para clientes (sin autenticación requerida)."""

    route_base = "/menu"
    default_view = "index"

    @expose("/")
    def index(self):
        categorias = db.session.query(Categoria).filter(
            Categoria.activo.is_(True)
        ).order_by(Categoria.orden).all()

        platos_por_categoria = {}
        for cat in categorias:
            platos = db.session.query(Plato).filter(
                Plato.categoria_id == cat.id,
                Plato.disponible.is_(True),
            ).all()
            if platos:
                platos_por_categoria[cat] = platos

        return self.render_template(
            "menu.html",
            categorias=categorias,
            platos_por_categoria=platos_por_categoria,
            appbuilder=appbuilder,
        )
