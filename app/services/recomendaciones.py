from decimal import Decimal
import json
import os

import requests

"""
Servicio de recomendaciones con IA (Groq) + fallback a sistema experto.

Genera recomendaciones accionables a partir de los datos de reportes
del restaurante, analizando patrones en ventas, platos y clientes.
"""

# ---------------------------------------------------------------------------
# Configuración de Groq
# ---------------------------------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")  # verifica tu modelo en la consola Groq
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


# ---------------------------------------------------------------------------
# Helpers de Groq
# ---------------------------------------------------------------------------
def _llamar_groq(prompt: str, contexto: dict) -> list:
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Eres un analista experto de restaurantes. "
                        "Devuelve recomendaciones accionables breves basadas en los datos. "
                        "Responde SOLO JSON válido con esta estructura: "
                        '{"recomendaciones": [{"icono": "bi-...", "titulo": "...", "texto": "...", "tipo": "success|info|warning|danger|secondary|primary"}]}'
                    ),
                },
                {
                    "role": "user",
                    "content": f"Datos del sistema:\n{json.dumps(contexto, ensure_ascii=False, default=str)}\n\n{prompt}",
                },
            ],
            "temperature": 0.3,
            "max_tokens": 600,
        }
        resp = requests.post(
            GROQ_URL,
            headers=headers,
            json=payload,
            timeout=15,
        )
        if resp.status_code != 200:
            return []
        content = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        data = json.loads(content)
        recs = data.get("recomendaciones", [])
        if not isinstance(recs, list):
            return []
        # Normalizar campos mínimos
        normalizadas = []
        for r in recs:
            normalizadas.append({
                "icono": r.get("icono", "bi-lightbulb"),
                "titulo": r.get("titulo", "Recomendación"),
                "texto": r.get("texto", ""),
                "tipo": r.get("tipo", "info"),
            })
        return normalizadas
    except Exception:
        return []




def _generar_recomendaciones_ventas_experto(
    ventas_diarias, ventas_mensuales, total_ingresos, total_pedidos, pedido_promedio
):
    recomendaciones = []

    if total_pedidos == 0:
        recomendaciones.append({
            "icono": "bi-exclamation-triangle",
            "titulo": "Sin actividad reciente",
            "texto": "No se registran pedidos en los últimos 7 días. Considera lanzar una promoción o revisar la disponibilidad del menú.",
            "tipo": "warning",
        })
        return recomendaciones

    total_pedidos_7dias = sum((r.cantidad for r in ventas_diarias), 0)
    promedio_diario = round(total_pedidos_7dias / 7, 2)

    if total_pedidos_7dias == 0:
        recomendaciones.append({
            "icono": "bi-calendar-x",
            "titulo": "Sin ventas recientes",
            "texto": "No hay ventas registradas en los últimos 7 días. Revisa si hay problemas con el flujo de pedidos o la demanda.",
            "tipo": "danger",
        })
    elif promedio_diario < 3:
        recomendaciones.append({
            "icono": "bi-graph-down-arrow",
            "titulo": "Baja afluencia diaria",
            "texto": f"El promedio diario es {promedio_diario:.1f} pedidos/día. Considera implementar descuentos por horario bajo o promociones digitales.",
            "tipo": "info",
        })

    if len(ventas_diarias) < 7:
        dias_sin = 7 - len(ventas_diarias)
        recomendaciones.append({
            "icono": "bi-calendar-week",
            "titulo": "Días sin actividad",
            "texto": f"Hay {dias_sin} día(s) sin ventas en la última semana. Evalúa si es un patrón recurrente por día de la semana.",
            "tipo": "secondary",
        })

    if len(ventas_mensuales) >= 2:
        primer_mes = ventas_mensuales[-1]
        ultimo_mes = ventas_mensuales[0]
        variacion = (
            ((ultimo_mes.total - primer_mes.total) / primer_mes.total * 100)
            if primer_mes.total
            else 0
        )
        if variacion > 15:
            recomendaciones.append({
                "icono": "bi-arrow-up-right",
                "titulo": "Crecimiento mensual destacado",
                "texto": f"Las ventas subieron un {variacion:.1f}% entre {primer_mes.mes} y {ultimo_mes.mes}. Aprovecha el impulso y amplía la oferta.",
                "tipo": "success",
            })
        elif variacion < -15:
            recomendaciones.append({
                "icono": "bi-arrow-down-right",
                "titulo": "Caída mensual preocupante",
                "texto": f"Las ventas bajaron un {abs(variacion):.1f}% entre {primer_mes.mes} y {ultimo_mes.mes}. Revisa precios, menú y competencia.",
                "tipo": "danger",
            })

    if pedido_promedio > 0 and pedido_promedio < 50:
        recomendaciones.append({
            "icono": "bi-receipt",
            "titulo": "Ticket promedio bajo",
            "texto": f"El ticket promedio (Bs {pedido_promedio:.2f}) está por debajo del rango saludable. Sugiere combos o upsell en las mesas.",
            "tipo": "info",
        })
    elif pedido_promedio >= 100:
        recomendaciones.append({
            "icono": "bi-receipt",
            "titulo": "Ticket promedio alto",
            "texto": f"El ticket promedio es Bs {pedido_promedio:.2f}. El cliente valora calidad. Mantén la excelencia y captura reseñas.",
            "tipo": "success",
        })

    if not recomendaciones:
        recomendaciones.append({
            "icono": "bi-check-circle",
            "titulo": "Ventas estables",
            "texto": "Los indicadores de ventas se mantienen equilibrados. Continúa monitoreando para detectar cambios tempranos.",
            "tipo": "success",
        })

    return recomendaciones


def _generar_recomendaciones_platos_experto(top_platos):
    recomendaciones = []

    if not top_platos:
        recomendaciones.append({
            "icono": "bi-egg-fried",
            "titulo": "Sin datos de platos",
            "texto": "No hay datos de platos vendidos. Verifica que los pedidos tengan items asociados correctamente.",
            "tipo": "warning",
        })
        return recomendaciones

    total_vendidos_global = sum((p.total_vendidos or 0) for p in top_platos)
    categorias = {}
    for p in top_platos:
        cat = p.categoria or "Sin categoría"
        categorias[cat] = categorias.get(cat, 0) + (p.total_vendidos or 0)

    if categorias:
        categoria_top = max(categorias, key=categorias.get)
        recomendaciones.append({
            "icono": "bi-trophy",
            "titulo": "Categoría líder",
            "texto": f"La categoría más vendida es '{categoria_top}'. Considera ampliar variedad o crear combos especiales de esa sección.",
            "tipo": "success",
        })

    plato_top = top_platos[0]
    if plato_top.total_vendidos and total_vendidos_global > 0:
        participacion = (plato_top.total_vendidos / total_vendidos_global) * 100
        if participacion > 30:
            recomendaciones.append({
                "icono": "bi-star",
                "titulo": "Súper ventas concentradas",
                "texto": f"'{plato_top.plato}' concentra el {participacion:.1f}% de las ventas. Asegura stock suficiente y promociónalo para maximizar márgenes.",
                "tipo": "info",
            })

    platos_baja = [p for p in top_platos if (p.total_vendidos or 0) < 5]
    if platos_baja:
        nombres = ", ".join(f"'{p.plato}'" for p in platos_baja[:3])
        recomendaciones.append({
            "icono": "bi-archive",
            "titulo": "Platos con baja rotación",
            "texto": f"Los siguientes platos tienen menos de 5 unidades vendidas: {nombres}. Evalúa retirarlos del menú o relanzarlos con una receta mejorada.",
            "tipo": "secondary",
        })

    if len(top_platos) >= 5:
        recomendaciones.append({
            "icono": "bi-lightbulb",
            "titulo": "Sugerencia de combo",
            "texto": (
                f"Crea un combo que combine el top 1 '{plato_top.plato}' con otras categorías "
                "para aumentar el ticket promedio."
            ),
            "tipo": "primary",
        })

    return recomendaciones


def _generar_recomendaciones_clientes_experto(top_clientes):
    recomendaciones = []

    if not top_clientes:
        recomendaciones.append({
            "icono": "bi-people",
            "titulo": "Sin clientes registrados",
            "texto": "No hay suficientes datos de clientes. Incentiva el registro al momento del pago para ofrecer beneficios.",
            "tipo": "warning",
        })
        return recomendaciones

    clientes_top = [c for c in top_clientes if (c.calificacion_promedio or 0) >= 4.5]
    if clientes_top:
        clientes_top.sort(key=lambda c: c.calificacion_promedio, reverse=True)
        nombres = ", ".join(
            f"{c.nombre} {c.apellido or ''}" for c in clientes_top[:3]
        )
        recomendaciones.append({
            "icono": "bi-star-fill",
            "titulo": "Clientes leales",
            "texto": f"Los siguientes clientes tienen calificaciones excelentes (≥4.5): {nombres}. Considera ofrecerles un programa de fidelidad o descuentos exclusivos.",
            "tipo": "success",
        })

    clientes_alto_gasto = [
        c
        for c in top_clientes
        if (c.gasto_total or Decimal(0)) > 0 and (c.calificacion_promedio or 5) < 3
    ]
    if clientes_alto_gasto:
        nombres = ", ".join(
            f"{c.nombre} {c.apellido or ''}" for c in clientes_alto_gasto[:3]
        )
        recomendaciones.append({
            "icono": "bi-chat-left-text",
            "titulo": "Clientes de alto valor insatisfechos",
            "texto": f"Los siguientes clientes gastan mucho pero tienen calificación baja: {nombres}. Contactalos y resuelve sus inconformidades para evitar su pérdida.",
            "tipo": "danger",
        })

    if top_clientes:
        promedio_gasto = sum((c.gasto_total or Decimal(0)) for c in top_clientes) / len(top_clientes)
        clientes_debajo = [
            c
            for c in top_clientes
            if (c.gasto_total or Decimal(0)) < promedio_gasto * Decimal("0.5")
        ]
        if clientes_debajo:
            recomendaciones.append({
                "icono": "bi-gift",
                "titulo": "Clientes con bajo gasto",
                "texto": (
                    f"{len(clientes_debajo)} de los top {len(top_clientes)} clientes gastan menos de la mitad del promedio. "
                    "Ofréceles ofertas personalizadas o combos familiares para reactivarlos."
                ),
                "tipo": "info",
            })

    if not recomendaciones:
        recomendaciones.append({
            "icono": "bi-check-circle-fill",
            "titulo": "Clientes en equilibrio",
            "texto": "Los indicadores de clientes frecuentes se mantienen estables. Continúa con la atención personalizada para retenerlos.",
            "tipo": "success",
        })

    return recomendaciones


# ---------------------------------------------------------------------------
# Helpers de serialización
# ---------------------------------------------------------------------------
def _serializar_ventas(ventas_diarias, ventas_mensuales, total_ingresos, total_pedidos, pedido_promedio):
    return {
        "total_ingresos": float(total_ingresos),
        "total_pedidos": int(total_pedidos),
        "pedido_promedio": float(pedido_promedio),
        "ventas_diarias": [
            {
                "dia": str(r.dia),
                "total": float(r.total),
                "cantidad": int(r.cantidad),
            }
            for r in ventas_diarias
        ],
        "ventas_mensuales": [
            {
                "mes": r.mes,
                "total": float(r.total),
                "cantidad": int(r.cantidad),
            }
            for r in ventas_mensuales
        ],
    }


def _serializar_platos(top_platos):
    return {
        "top_platos": [
            {
                "plato": p.plato,
                "categoria": p.categoria,
                "veces_pedido": int(p.veces_pedido or 0),
                "total_vendidos": int(p.total_vendidos or 0),
                "ingreso_total": float(p.ingreso_total or 0),
                "precio": float(p.precio or 0),
            }
            for p in top_platos
        ]
    }


def _serializar_clientes(top_clientes):
    return {
        "top_clientes": [
            {
                "nombre": c.nombre,
                "apellido": c.apellido or "",
                "total_pedidos": int(c.total_pedidos or 0),
                "gasto_total": float(c.gasto_total or 0),
                "calificacion_promedio": float(c.calificacion_promedio or 0),
            }
            for c in top_clientes
        ]
    }


# ---------------------------------------------------------------------------
# API pública (usada por las vistas)
# ---------------------------------------------------------------------------
def generar_recomendaciones_ventas(
    ventas_diarias, ventas_mensuales, total_ingresos, total_pedidos, pedido_promedio
):
    contexto = _serializar_ventas(ventas_diarias, ventas_mensuales, total_ingresos, total_pedidos, pedido_promedio)
    prompt = (
        "Genera 2 a 4 recomendaciones accionables para mejorar las ventas de este restaurante, "
        "basándote en los datos JSON. Considera tendencias, días sin ventas, ticket promedio y crecimiento mensual. "
        "Sugiere acciones concretas (promos, combos, horarios, etc.)."
    )
    recs = _llamar_groq(prompt, contexto)
    if recs:
        return recs
    return _generar_recomendaciones_ventas_experto(
        ventas_diarias, ventas_mensuales, total_ingresos, total_pedidos, pedido_promedio
    )


def generar_recomendaciones_platos(top_platos):
    contexto = _serializar_platos(top_platos)
    prompt = (
        "Genera 2 a 4 recomendaciones accionables sobre el menú y los platos más vendidos. "
        "Sugiere combos, retiros, promociones o ajustes de carta basándote en rotación, categorías líderes y concentración de ventas."
    )
    recs = _llamar_groq(prompt, contexto)
    if recs:
        return recs
    return _generar_recomendaciones_platos_experto(top_platos)


def generar_recomendaciones_clientes(top_clientes):
    contexto = _serializar_clientes(top_clientes)
    prompt = (
        "Genera 2 a 4 recomendaciones accionables sobre fidelización y experiencia de clientes. "
        "Identifica clientes leales, insatisfechos o con bajo gasto, y sugiere campañas, beneficios o seguimiento concreto."
    )
    recs = _llamar_groq(prompt, contexto)
    if recs:
        return recs
    return _generar_recomendaciones_clientes_experto(top_clientes)

