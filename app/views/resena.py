"""
CRUD Reseñas.
"""
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.views import ModelView
from app.models import Resena


class ResenaModelView(ModelView):
    datamodel = SQLAInterface(Resena)
    list_columns = ["id", "pedido", "cliente",
                     "calificacion", "comentario", "fecha"]
    add_columns = ["pedido", "cliente", "calificacion", "comentario"]
    edit_columns = add_columns
    show_columns = add_columns + ["fecha"]
