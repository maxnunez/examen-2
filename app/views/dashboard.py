"""
Dashboard con estadísticas del restaurante.
"""
from datetime import datetime

from flask_appbuilder import BaseView, expose, has_access
from app import appbuilder, db
from app.models import (
    Mesa, Pedido, Plato, Cliente, Pago, Resena, EstadoPedido,
)


class DashboardView(BaseView):
    """Dashboard con estadísticas del restaurante."""

    route_base = "/dashboard"
    default_view = "index"

    @expose("/")
    @has_access
    def index(self):
        session = db.session

        hoy = datetime.utcnow().date()
        inicio_dia = datetime.combine(hoy, datetime.min.time())
        fin_dia = datetime.combine(hoy, datetime.max.time())

        total_ingresos = float(
            session.query(db.func.sum(Pago.monto)).scalar() or 0
        )
        total_pedidos = session.query(Pedido).count()
        pedido_promedio = (
            total_ingresos / total_pedidos if total_pedidos > 0 else 0.0
        )

        stats = {
            "total_mesas": session.query(Mesa).filter(
                Mesa.activa.is_(True)).count(),
            "pedidos_hoy": session.query(Pedido).filter(
                Pedido.fecha >= inicio_dia,
                Pedido.fecha <= fin_dia,
            ).count(),
            "ingresos_hoy": session.query(
                db.func.sum(Pago.monto)
            ).filter(
                Pago.fecha >= inicio_dia,
                Pago.fecha <= fin_dia,
            ).scalar() or 0,
            "pedidos_pendientes": session.query(Pedido).filter(
                Pedido.estado == EstadoPedido.PENDIENTE
            ).count(),
            "total_clientes": session.query(Cliente).count(),
            "resena_promedio": session.query(
                db.func.avg(Resena.calificacion)
            ).scalar() or 0,
            "total_ingresos": total_ingresos,
            "total_pedidos": total_pedidos,
            "pedido_promedio": pedido_promedio,
        }

        ultimos_pedidos = session.query(Pedido).order_by(
            Pedido.fecha.desc()
        ).limit(8).all()

        top_platos = session.query(Plato).filter(
            Plato.destacado.is_(True),
            Plato.disponible.is_(True),
        ).limit(6).all()

        return self.render_template(
            "dashboard.html",
            **stats,
            ultimos_pedidos=ultimos_pedidos,
            top_platos=top_platos,
            appbuilder=appbuilder,
        )
