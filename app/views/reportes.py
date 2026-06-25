from datetime import datetime, timedelta
from sqlalchemy import func, desc, text
from flask_appbuilder import BaseView, expose, has_access

from app import appbuilder, db
from app.services.recomendaciones import (
    generar_recomendaciones_ventas,
    generar_recomendaciones_platos,
    generar_recomendaciones_clientes,
)
from app.models import (
    Pedido, ItemPedido, Plato, Categoria,
    Cliente, Pago, Resena, EstadoPedido,
)


class ReportesView(BaseView):
    route_base = "/reportes"
    default_view = "ventas"

    @expose("/ventas/")
    @has_access
    def ventas(self):
        hoy = datetime.utcnow().date()
        hace_7 = hoy - timedelta(days=7)
        hace_30 = hoy - timedelta(days=30)

        ventas_diarias = (
            db.session.query(
                func.date(Pedido.fecha).label("dia"),
                func.sum(Pedido.total).label("total"),
                func.count(Pedido.id).label("cantidad"),
            )
            .filter(Pedido.fecha >= hace_7, Pedido.estado != EstadoPedido.CANCELADO)
            .group_by(func.date(Pedido.fecha))
            .order_by(desc("dia"))
            .all()
        )

        ventas_mensuales = (
            db.session.query(
                func.date_format(Pedido.fecha, text("'%Y-%m'")).label("mes"),
            )
            .filter(Pedido.estado != EstadoPedido.CANCELADO)
            .group_by(func.date_format(Pedido.fecha, text("'%Y-%m'")))
            .order_by(desc("mes"))
            .limit(12)
            .all()
        )

        total_ingresos = (
            db.session.query(func.sum(Pedido.total))
            .filter(Pedido.estado != EstadoPedido.CANCELADO)
            .scalar()
            or 0
        )

        total_pedidos = (
            db.session.query(func.count(Pedido.id))
            .scalar()
            or 0
        )

        pedido_promedio = round(total_ingresos / total_pedidos, 2) if total_pedidos else 0

        recomendaciones_ventas = generar_recomendaciones_ventas(
            ventas_diarias, ventas_mensuales, total_ingresos, total_pedidos, pedido_promedio
        )

        return self.render_template(
            "reportes/ventas.html",
            ventas_diarias=ventas_diarias,
            ventas_mensuales=ventas_mensuales,
            total_ingresos=total_ingresos,
            total_pedidos=total_pedidos,
            pedido_promedio=pedido_promedio,
            recomendaciones_ventas=recomendaciones_ventas,
        )

    @expose("/platos/")
    @has_access
    def platos(self):
        top_platos = (
            db.session.query(
                Plato.nombre.label("plato"),
                Categoria.nombre.label("categoria"),
                func.count(ItemPedido.id).label("veces_pedido"),
                func.sum(ItemPedido.cantidad).label("total_vendidos"),
                func.sum(ItemPedido.subtotal).label("ingreso_total"),
                Plato.precio,
            )
            .join(Plato, ItemPedido.plato_id == Plato.id)
            .join(Categoria, Plato.categoria_id == Categoria.id)
            .group_by(Plato.id)
            .order_by(desc("total_vendidos"))
            .limit(20)
            .all()
        )

        recomendaciones_platos = generar_recomendaciones_platos(top_platos)

        return self.render_template(
            "reportes/platos.html",
            top_platos=top_platos,
            recomendaciones_platos=recomendaciones_platos,
        )

    @expose("/clientes/")
    @has_access
    def clientes(self):
        top_clientes = (
            db.session.query(
                Cliente.id,
                Cliente.nombre,
                Cliente.apellido,
                Cliente.telefono,
                Cliente.email,
                func.count(Pedido.id).label("total_pedidos"),
                func.sum(Pedido.total).label("gasto_total"),
                func.avg(Resena.calificacion).label("calificacion_promedio"),
            )
            .join(Pedido, Pedido.cliente_id == Cliente.id)
            .outerjoin(Resena, Resena.cliente_id == Cliente.id)
            .group_by(Cliente.id)
            .order_by(desc("gasto_total"))
            .limit(20)
            .all()
        )

        recomendaciones_clientes = generar_recomendaciones_clientes(top_clientes)

        return self.render_template(
            "reportes/clientes.html",
            top_clientes=top_clientes,
            recomendaciones_clientes=recomendaciones_clientes,
        )


class GraficosView(BaseView):
    route_base = "/graficos"
    default_view = "ingresos"

    @expose("/ingresos/")
    @has_access
    def ingresos(self):
        hoy = datetime.utcnow().date()
        hace_30 = hoy - timedelta(days=30)

        data = (
            db.session.query(
                func.date(Pedido.fecha).label("dia"),
                func.sum(Pedido.total).label("total"),
            )
            .filter(
                Pedido.fecha >= hace_30,
                Pedido.estado != EstadoPedido.CANCELADO,
            )
            .group_by(func.date(Pedido.fecha))
            .order_by("dia")
            .all()
        )

        labels = [str(r.dia) for r in data]
        values = [float(r.total) for r in data]

        return self.render_template(
            "graficos/ingresos.html",
            labels=labels,
            values=values,
        )

    @expose("/estados/")
    @has_access
    def estados(self):
        data = (
            db.session.query(
                Pedido.estado,
                func.count(Pedido.id).label("cantidad"),
            )
            .group_by(Pedido.estado)
            .all()
        )

        labels = [str(r.estado.value).replace("_", " ").title() for r in data]
        values = [r.cantidad for r in data]

        colores = {
            "Pendiente": "#ffc107",
            "En Preparacion": "#0dcaf0",
            "Servido": "#198754",
            "Cancelado": "#dc3545",
            "Pagado": "#0d6efd",
        }
        bg = [colores.get(l, "#6c757d") for l in labels]

        return self.render_template(
            "graficos/estados.html",
            labels=labels,
            values=values,
            colores=bg,
        )

    @expose("/clientes/")
    @has_access
    def clientes_frecuentes(self):
        data = (
            db.session.query(
                Cliente.nombre,
                Cliente.apellido,
                func.count(Pedido.id).label("total_pedidos"),
                func.sum(Pedido.total).label("gasto_total"),
            )
            .join(Pedido, Pedido.cliente_id == Cliente.id)
            .group_by(Cliente.id)
            .order_by(desc("total_pedidos"))
            .limit(10)
            .all()
        )

        labels = [f"{r.nombre} {r.apellido or ''}" for r in data]
        valores_pedidos = [r.total_pedidos for r in data]
        valores_gasto = [float(r.gasto_total or 0) for r in data]

        return self.render_template(
            "graficos/clientes.html",
            labels=labels,
            valores_pedidos=valores_pedidos,
            valores_gasto=valores_gasto,
        )

    @expose("/categorias/")
    @has_access
    def categorias(self):
        data = (
            db.session.query(
                Categoria.nombre.label("categoria"),
                func.count(Plato.id).label("cantidad"),
            )
            .join(Plato, Plato.categoria_id == Categoria.id)
            .group_by(Categoria.id)
            .order_by(desc("cantidad"))
            .all()
        )

        labels = [r.categoria for r in data]
        values = [r.cantidad for r in data]

        return self.render_template(
            "graficos/categorias.html",
            labels=labels,
            values=values,
        )
