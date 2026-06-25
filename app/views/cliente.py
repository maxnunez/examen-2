"""
CRUD Clientes.
"""
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.views import ModelView
from app.models import Cliente


class ClienteModelView(ModelView):
    datamodel = SQLAInterface(Cliente)
    list_columns = [
        "id", "nombre_completo", "telefono", "email",
        "cliente_vip", "total_pedidos",
    ]
    add_columns = [
        "nombre", "apellido", "telefono", "email", "direccion",
        "notas", "fecha_nacimiento", "cliente_vip",
    ]
    edit_columns = add_columns
    show_columns = add_columns

    label_columns = {
        "nombre_completo": "Nombre",
        "cliente_vip": "VIP",
    }
