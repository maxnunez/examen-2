"""
CRUD Mesas.
"""
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.views import ModelView
from app.models import Mesa


class MesaModelView(ModelView):
    datamodel = SQLAInterface(Mesa)
    list_columns = ["id", "numero", "capacidad", "ubicacion", "activa"]
    add_columns = ["numero", "capacidad", "ubicacion", "activa", "qr_code_url"]
    edit_columns = add_columns
    show_columns = add_columns
