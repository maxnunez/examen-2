"""
CRUD Configuraciones.
"""
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.views import ModelView
from app.models import Configuracion


class ConfiguracionModelView(ModelView):
    datamodel = SQLAInterface(Configuracion)
    list_columns = ["id", "clave", "valor", "descripcion"]
    add_columns = ["clave", "valor", "descripcion"]
    edit_columns = add_columns
    show_columns = add_columns
