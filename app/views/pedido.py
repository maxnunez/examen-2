"""
CRUD Pedidos e Items de Pedido.
"""
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.views import ModelView
from app.models import Pedido, ItemPedido


class PedidoModelView(ModelView):
    datamodel = SQLAInterface(Pedido)
    list_columns = [
        "id", "codigo", "estado", "cliente", "mesa",
        "total", "metodo_pago", "fecha",
    ]
    add_columns = [
        "codigo", "estado", "cliente", "mesa",
        "usuario_mesero", "subtotal", "impuesto", "descuento",
        "total", "metodo_pago", "notas_cocina",
    ]
    edit_columns = add_columns
    show_columns = add_columns + ["atendido_en", "pagado_en"]

    label_columns = {
        "cliente": "Cliente",
        "mesa": "Mesa",
        "usuario_mesero": "Mesero",
        "metodo_pago": "Método de Pago",
        "notas_cocina": "Notas Cocina",
    }


class ItemPedidoModelView(ModelView):
    datamodel = SQLAInterface(ItemPedido)
    list_columns = [
        "id", "pedido", "plato", "cantidad",
        "precio_unitario", "subtotal", "entregado",
    ]
    add_columns = [
        "pedido", "plato", "cantidad",
        "precio_unitario", "subtotal", "notas",
    ]
    edit_columns = add_columns
    show_columns = add_columns + ["entregado", "entregado_en"]
