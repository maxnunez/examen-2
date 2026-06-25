"""
CRUD Pagos.
"""
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.views import ModelView
from app.models import Pago


class PagoModelView(ModelView):
    datamodel = SQLAInterface(Pago)
    list_columns = ["id", "pedido", "monto", "metodo", "referencia", "fecha"]
    add_columns = ["pedido", "monto", "metodo", "referencia"]
    edit_columns = add_columns
    show_columns = add_columns + ["fecha"]
