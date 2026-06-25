import os
import sys
import random
from datetime import datetime, timedelta
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import (
    Categoria, Plato, Cliente, Mesa,
    Pedido, ItemPedido, Pago, Resena, EstadoPedido,
)
from app import db
from flask_appbuilder.security.sqla.models import User

app = create_app()

with app.app_context():
    user = db.session.query(User).first()
    if not user:
        user = User(first_name="Seed", last_name="Bot", username="seedbot", email="seed@example.com", active=True, roles=[])
        user.set_password("seedbot")
        db.session.add(user)
        db.session.commit()

    db.session.query(ItemPedido).delete()
    db.session.query(Pago).delete()
    db.session.query(Resena).delete()
    db.session.query(Pedido).delete()
    db.session.query(Plato).delete()
    db.session.query(Cliente).delete()
    db.session.query(Mesa).delete()
    db.session.query(Categoria).delete()
    db.session.commit()

    cats = [
        ("Entradas", "Aperitivos y entrantes", "bi-basket"),
        ("Platos Fuertes", "Platos principales de la casa", "bi-fire"),
        ("Bebidas", "Bebidas frías y calientes", "bi-cup-straw"),
        ("Postres", "Dulces para cerrar la experiencia", "bi-cake"),
        ("Ensaladas", "Opciones frescas y saludables", "bi-leaf"),
    ]
    categorias = []
    for nombre, desc, icono in cats:
        c = Categoria(nombre=nombre, descripcion=desc, icono=icono, activo=True, orden=len(categorias)+1)
        c.created_by_fk = user.id
        c.changed_by_fk = user.id
        db.session.add(c)
        categorias.append(c)
    db.session.commit()

    platos_data = [
        ("Tequeños", "Queso envuelto en masa", 25, 8, 0, True, False, 10, 350, False, False, False, 0),
        ("Empanadas de carne", "Empanadas al horno", 20, 6, 0, True, False, 15, 400, False, False, False, 0),
        ("Sopa del día", "Sopa casera de temporada", 18, 5, 0, True, False, 12, 120, False, False, True, 0),
        ("Brusquetas caprese", "Pan tostado con tomate y albahaca", 22, 7, 0, True, True, 8, 220, False, True, False, 0),
        ("Parrilla mixta", "Corte de carne con papas fritas", 120, 45, 0, True, False, 25, 750, False, False, False, 0),
        ("Pasta carbonara", "Pasta con salsa cremosa", 65, 22, 0, True, False, 20, 620, False, False, True, 0),
        ("Pollo a la brasa", "Pollo entero con guarnición", 90, 32, 0, True, False, 30, 580, False, False, False, 0),
        ("Pescado a la plancha", "Filete con vegetales", 85, 30, 0, True, False, 22, 420, False, False, True, 0),
        ("Hamburguesa clásica", "Carne, queso y vegetales", 45, 15, 0, True, False, 15, 550, False, False, False, 0),
        ("Churrasco con ensalada", "Corte fino con vegetales frescos", 95, 35, 0, True, True, 18, 480, False, False, True, 0),
        ("Jugo natural", "Fruta de temporada", 15, 4, 0, True, False, 5, 80, False, True, True, 0),
        ("Refresco", "Bebida gaseosa 500ml", 12, 3, 0, True, False, 2, 120, False, False, False, 0),
        ("Agua mineral", "Botella 500ml", 8, 2, 0, True, False, 2, 0, False, False, False, 0),
        ("Vino tinto", "Copa de vino de la casa", 35, 12, 0, True, False, 5, 150, False, False, False, 0),
        ("Cerveza artesanal", "Pinta de la casa", 28, 10, 0, True, False, 5, 180, False, False, False, 0),
        ("Torta de chocolate", "Porción generosa", 28, 10, 0, True, False, 10, 450, False, False, False, 0),
        ("Helado artesanal", "2 bolas a elección", 20, 6, 0, True, False, 5, 220, False, True, False, 0),
        ("Flan casero", "Con caramelo", 18, 5, 0, True, False, 8, 260, False, False, False, 0),
        ("Brownie con helado", "Brownie tibio", 32, 12, 0, True, False, 12, 480, False, False, False, 0),
        ("Ensalada César", "Lechuga, pollo, crutones", 45, 14, 0, True, True, 10, 320, False, False, False, 0),
        ("Ensalada Mediterránea", "Mix de hojas, aceitunas, feta", 40, 13, 0, True, True, 10, 280, False, True, False, 0),
    ]
    platos = []
    for idx, data in enumerate(platos_data):
        nombre, desc, precio, costo, img_url, disponible, destacado, tiempo, calorias, veg, vegano, gluten, orden = data
        p = Plato(
            nombre=nombre,
            descripcion=desc,
            imagen_url=img_url or None,
            precio=Decimal(str(precio)),
            costo=Decimal(str(costo)),
            categoria_id=categorias[idx % len(categorias)].id,
            disponible=disponible,
            destacado=destacado,
            tiempo_preparacion_min=tiempo,
            calorias=calorias,
            es_vegetariano=veg,
            es_vegano=vegano,
            sin_gluten=gluten,
        )
        p.created_by_fk = user.id
        p.changed_by_fk = user.id
        db.session.add(p)
        platos.append(p)
    db.session.commit()

    with db.session.no_autoflush:
        clientes_data = [
            ("María", "López", "71234567", "maria@example.com", "Calle 1"),
            ("Juan", "Pérez", "72345678", "juan@example.com", "Calle 2"),
            ("Ana", "González", "73456789", "ana@example.com", "Calle 3"),
            ("Carlos", "Ramírez", "74567890", "carlos@example.com", "Calle 4"),
            ("Laura", "Martínez", "75678901", "laura@example.com", "Calle 5"),
            ("Diego", "Fernández", "76789012", "diego@example.com", "Calle 6"),
            ("Sofía", "Torres", "77890123", "sofia@example.com", "Calle 7"),
            ("Andrés", "Díaz", "78901234", "andres@example.com", "Calle 8"),
            ("Valentina", "Ruiz", "79012345", "valentina@example.com", "Calle 9"),
            ("Mateo", "Hernández", "70123456", "mateo@example.com", "Calle 10"),
            ("Lucía", "Morales", "71234568", "lucia@example.com", "Calle 11"),
            ("Sebastián", "Jiménez", "72345679", "sebastian@example.com", "Calle 12"),
            ("Camila", "Álvarez", "73456780", "camila@example.com", "Calle 13"),
            ("Nicolás", "Rojas", "74567891", "nicolas@example.com", "Calle 14"),
            ("Gabriela", "Mendoza", "75678902", "gabriela@example.com", "Calle 15"),
            ("Daniel", "Silva", "76789013", "daniel@example.com", "Calle 16"),
            ("Isabella", "Castillo", "77890124", "isabella@example.com", "Calle 17"),
            ("Samuel", "Vargas", "78901235", "samuel@example.com", "Calle 18"),
            ("Emilia", "Romero", "79012346", "emilia@example.com", "Calle 19"),
            ("Tomás", "Gutiérrez", "70123457", "tomas@example.com", "Calle 20"),
        ]
        clientes = []
        for nombre, apellido, telefono, email, direccion in clientes_data:
            cli = Cliente(
                nombre=nombre,
                apellido=apellido,
                telefono=telefono,
                email=email,
                direccion=direccion,
                notas="",
                fecha_nacimiento=None,
                total_pedidos=0,
                cliente_vip=False,
            )
            cli.created_by_fk = user.id
            cli.changed_by_fk = user.id
            db.session.add(cli)
            clientes.append(cli)
        db.session.commit()

        mesas = []
        for i in range(1, 13):
            m = Mesa(numero=i, capacidad=random.choice([2, 4, 6]), ubicacion=random.choice(["Interior", "Terraza", "VIP", "Barra"]), activa=True)
            m.created_by_fk = user.id
            m.changed_by_fk = user.id
            db.session.add(m)
            mesas.append(m)
        db.session.commit()

        estados = [EstadoPedido.PENDIENTE, EstadoPedido.EN_PREPARACION, EstadoPedido.SERVIDO, EstadoPedido.PAGADO, EstadoPedido.CANCELADO]
        metodo_pagos = ["efectivo", "tarjeta", "qr"]

        base_fecha = datetime.utcnow() - timedelta(days=90)
        pedidos = []
        for i in range(120):
            fecha = base_fecha + timedelta(days=random.randint(0, 90), hours=random.randint(10, 22), minutes=random.randint(0, 59))
            estado = random.choices(estados, weights=[5, 8, 15, 65, 7])[0]
            cliente = random.choice(clientes) if random.random() > 0.15 else None
            mesa = random.choice(mesas)

            n_items = random.randint(1, 4)
            platos_disponibles = random.sample(platos, min(n_items, len(platos)))
            subtotal = Decimal("0")
            for plato in platos_disponibles:
                cantidad = random.randint(1, 3)
                precio_unitario = Decimal(str(plato.precio))
                subtotal += precio_unitario * cantidad

            subtotal = subtotal.quantize(Decimal("0.01"))
            impuesto = (subtotal * Decimal("0.13")).quantize(Decimal("0.01"))
            descuento = Decimal("0")
            if random.random() > 0.8:
                descuento = (subtotal * Decimal("0.05")).quantize(Decimal("0.01"))
            total = (subtotal + impuesto - descuento).quantize(Decimal("0.01"))

            pedido = Pedido(
                codigo=f"PED-{i+1:04d}",
                estado=estado,
                cliente_id=cliente.id if cliente else None,
                mesa_id=mesa.id,
                usuario_mesero_id=None,
                subtotal=subtotal,
                impuesto=impuesto,
                descuento=descuento,
                total=total,
                metodo_pago=random.choice(metodo_pagos) if estado in [EstadoPedido.SERVIDO, EstadoPedido.PAGADO] else None,
                notas_cocina=random.choice(["", "", "", "Sin cebolla", "Poca sal", ""]),
                atendido_en=fecha + timedelta(minutes=random.randint(5, 15)) if estado != EstadoPedido.PENDIENTE else None,
                pagado_en=fecha + timedelta(minutes=random.randint(20, 60)) if estado == EstadoPedido.PAGADO else None,
                fecha=fecha,
            )
            pedido.created_by_fk = user.id
            pedido.changed_by_fk = user.id
            db.session.add(pedido)
            db.session.flush()

            for plato in platos_disponibles:
                cantidad = random.randint(1, 3)
                precio_unitario = Decimal(str(plato.precio))
                item_subtotal = (precio_unitario * cantidad).quantize(Decimal("0.01"))
                item = ItemPedido(
                    pedido_id=pedido.id,
                    plato_id=plato.id,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    subtotal=item_subtotal,
                    notas="" if random.random() > 0.2 else random.choice(["Salsas aparte", "Sin hielo"]),
                    entregado=random.random() > 0.5,
                    entregado_en=fecha + timedelta(minutes=random.randint(10, 30)) if random.random() > 0.5 else None,
                )
                item.created_by_fk = user.id
                item.changed_by_fk = user.id
                db.session.add(item)

            if estado == EstadoPedido.PAGADO:
                pago = Pago(
                    pedido_id=pedido.id,
                    monto=total,
                    metodo=pedido.metodo_pago,
                    referencia=f"REF-{i+1:06d}",
                    fecha=pedido.pagado_en or fecha + timedelta(minutes=30),
                )
                pago.created_by_fk = user.id
                pago.changed_by_fk = user.id
                db.session.add(pago)

            pedidos.append(pedido)
        db.session.commit()

    pedidos_pagados = [p for p in pedidos if p.estado and p.estado.upper() == EstadoPedido.PAGADO.name and p.cliente_id is not None]
    random.shuffle(pedidos_pagados)
    reseñados = pedidos_pagados[:50]
    print('pedidos_pagados:', len(pedidos_pagados), 'reseñados:', len(reseñados))
    for pedido in reseñados:
        cliente = next(c for c in clientes if c.id == pedido.cliente_id)
        calificacion = random.choices([1, 2, 3, 4, 5], weights=[5, 8, 15, 35, 37])[0]
        comentarios = [
            "Excelente atención y comida deliciosa.",
            "Muy buena experiencia, volveré.",
            "El servicio fue un poco lento.",
            "La comida estuvo fría, esperaba más.",
            "Increíble sabor y presentación.",
            "Buena relación calidad-precio.",
            "No me gustó la preparación del plato.",
            "El mesero muy amable.",
            "Ambiente agradable y acogedor.",
            "Pedí para llevar y llegó perfecto.",
            "Los platos principales son los mejores.",
            "Muy recomendado para familias.",
            "Postres espectaculares.",
            "Bebidas frescas y bien atendidas.",
            "El estacionamiento es cómodo.",
            "Buena música y ambientación.",
            "Una experiencia memorable.",
            "Regular, esperaba más por el precio.",
            "Rápido y delicioso.",
            "La ensalada estaba fresca.",
        ]
        comentario = random.choice(comentarios)
        reseña = Resena(
            pedido_id=pedido.id,
            cliente_id=cliente.id,
            calificacion=calificacion,
            comentario=comentario,
            fecha=pedido.pagado_en or pedido.fecha + timedelta(minutes=40),
        )
        reseña.created_by_fk = user.id
        reseña.changed_by_fk = user.id
        db.session.add(reseña)

    db.session.commit()
    print("Seed completado exitosamente.")
    print(f"Categorías: {len(categorias)}")
    print(f"Platos: {len(platos)}")
    print(f"Clientes: {len(clientes)}")
    print(f"Mesas: {len(mesas)}")
    print(f"Pedidos: {len(pedidos)}")
