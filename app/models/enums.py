"""
Enums compartidos entre modelos.
"""
import enum


class EstadoPedido(str, enum.Enum):
    PENDIENTE = "pendiente"
    EN_PREPARACION = "en_preparacion"
    SERVIDO = "servido"
    CANCELADO = "cancelado"
    PAGADO = "pagado"
