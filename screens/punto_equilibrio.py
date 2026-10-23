import streamlit as st

from components.tarjetas import estilo_metric_cards
from db import gastos as gastos_db
from db import herramientas as herramientas_db
from db import insumos as insumos_db
from db import productos as productos_db
from db.models import TIPOS_GASTO
from utils.costos import (
    DIAS_POR_MES,
    HORAS_POR_DIA,
    costo_variable_sabor,
    depreciacion_total,
    gastos_mensuales,
    punto_equilibrio,
)

TIPO_FIJO, TIPO_VARIABLE = TIPOS_GASTO


def _supuestos() -> tuple[float, float]:
    return (
        st.session_state.get("gastos_dias_mes", DIAS_POR_MES),
        st.session_state.get("gastos_horas_dia", HORAS_POR_DIA),
    )


def _gastos_por_tipo(gastos: list[dict], tipo: str, dias: float, horas: float) -> float:
    return gastos_mensuales(
        [gasto for gasto in gastos if gasto["tipo"] == tipo], dias, horas
    )


def mostrar() -> None:
    st.title("Punto de equilibrio", icon=":material/scale:")
    estilo_metric_cards()

    dias, horas = _supuestos()
    gastos = gastos_db.listar_gastos()
    fijos_gastos = _gastos_por_tipo(gastos, TIPO_FIJO, dias, horas)
    variables = _gastos_por_tipo(gastos, TIPO_VARIABLE, dias, horas)
    depreciacion = depreciacion_total(herramientas_db.listar_herramientas())
    fijos_totales = fijos_gastos + depreciacion

    st.subheader("Costos mensuales", icon=":material/calendar_month:")
    col_fijos, col_depreciacion, col_total = st.columns(3)
    col_fijos.metric(
        "Costos fijos (gastos)",
        f"${fijos_gastos:,.2f}",
        icon=":material/lock:",
        help="Gastos tipo Fijo, normalizados al mes.",
    )
    col_depreciacion.metric(
        "Depreciación",
        f"${depreciacion:,.2f}",
        icon=":material/handyman:",
        help="Depreciación mensual de herramientas, solo mientras están dentro de su vida útil.",
    )
    col_total.metric(
        "Costos fijos totales",
        f"${fijos_totales:,.2f}",
        icon=":material/functions:",
        help="Gastos fijos + depreciación. Es lo que entra al punto de equilibrio.",
    )
    st.subheader("Producto", icon=":material/tag:")
    productos = productos_db.listar_productos()
    if not productos:
        st.warning("Da de alta al menos un sabor en la pantalla Productos.")
        return

    nombre = st.selectbox("Sabor", [producto["nombre"] for producto in productos])
    precio = next(
        producto["precio"] for producto in productos if producto["nombre"] == nombre
    )
    costo_variable = costo_variable_sabor(insumos_db.listar_insumos(), nombre)
    if not costo_variable:
        st.warning(f"Ningún insumo está marcado para «{nombre}» en Insumos.")
    if not precio:
        st.warning(f"El sabor «{nombre}» no tiene precio. Ponlo en Productos.")

    col_precio, col_costo, col_margen = st.columns(3)
    col_precio.metric("Precio de venta", f"${precio:,.2f}", icon=":material/sell:")
    col_costo.metric(
        "Costo variable unitario",
        f"${costo_variable:,.2f}",
        icon=":material/inventory_2:",
    )
    col_margen.metric(
        "Margen de contribución",
        f"${precio - costo_variable:,.2f}",
        icon=":material/trending_up:",
    )

    equilibrio = punto_equilibrio(precio, costo_variable, fijos_totales)
    if equilibrio is None:
        st.warning(
            "El margen de contribución debe ser mayor que cero para calcular "
            "el punto de equilibrio."
        )
        return

    st.subheader("Resultado", icon=":material/insights:")
    col_unidades, col_ventas = st.columns(2)
    col_unidades.metric(
        "Punto de equilibrio",
        f"{equilibrio:,.0f} unidades",
        icon=":material/balance:",
    )
    col_ventas.metric(
        "Ventas de equilibrio",
        f"${equilibrio * precio:,.2f}",
        icon=":material/attach_money:",
    )
