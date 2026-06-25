"""
CRUD Platos.
"""
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.views import ModelView
from app.models import Plato


class PlatoModelView(ModelView):
    datamodel = SQLAInterface(Plato)
    list_columns = [
        "id", "nombre", "precio", "categoria", "disponible",
        "destacado", "tiempo_preparacion_min",
    ]
    add_columns = [
        "nombre", "descripcion", "imagen_url", "precio", "costo",
        "categoria", "disponible", "destacado", "tiempo_preparacion_min",
        "calorias", "es_vegetariano", "es_vegano", "sin_gluten",
    ]
    edit_columns = add_columns
    show_columns = add_columns

    label_columns = {
        "categoria": "Categoría",
        "precio": "Precio (Bs)",
        "tiempo_preparacion_min": "Tiempo (min)",
    }
    search_columns = ["nombre", "descripcion"]
    show_title = "Detalle del Plato"
    add_title = "Nuevo Plato"
    edit_title = "Editar Plato"
