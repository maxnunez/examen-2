"""
CRUD Categorías.
"""
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.views import ModelView
from app import appbuilder
from app.models import Categoria


class CategoriaModelView(ModelView):
    datamodel = SQLAInterface(Categoria)
    list_columns = ["id", "nombre", "activo", "orden"]
    add_columns = ["nombre", "descripcion", "icono", "activo", "orden"]
    edit_columns = ["nombre", "descripcion", "icono", "activo", "orden"]
    show_columns = add_columns

    label_columns = {"icono": "Icono Bootstrap"}
