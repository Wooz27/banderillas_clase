import streamlit as st

from components.tarjetas import estilo_metric_cards
from db import gastos as gastos_db
from db import herramientas as herramientas_db
from db import insumos as insumos_db
from db import productos as productos_db
from db import ventas as ventas_db
from db.models import TIPOS_GASTO
from utils.costos import (
    DIAS_POR_MES,
    HORAS_POR_DIA,
    costo_variable_sabor,
    depreciacion_total,
    gastos_mensuales,
)
from utils.ventas import comparacion, resumen_ventas

TIPO_FIJO = TIPOS_GASTO[0]
VENTANAS = (7, 30, 90)


def _precios() -> dict:
    return {producto["nombre"]: producto["precio"] for producto in productos_db.listar_productos()}


def _costos_variables() -> dict:
    insumos = insumos_db.listar_insumos()
    return {
        producto["nombre"]: costo_variable_sabor(insumos, producto["nombre"])
        for producto in productos_db.listar_productos()
    }


def _supuestos() -> tuple[float, float]:
    return (
        st.session_state.get("gastos_dias_mes", DIAS_POR_MES),
        st.session_state.get("gastos_horas_dia", HORAS_POR_DIA),
    )


def _fijos_mensuales(dias: float, horas: float) -> float:
    gastos = [gasto for gasto in gastos_db.listar_gastos() if gasto["tipo"] == TIPO_FIJO]
    return gastos_mensuales(gastos, dias, horas) + depreciacion_total(
        herramientas_db.listar_herramientas()
    )


def mostrar() -> None:
    st.title("Análisis de ventas", icon=":material/analytics:")
    estilo_metric_cards()

    dias = st.segmented_control(
        "Ventana de análisis",
        options=VENTANAS,
        default=30,
        format_func=lambda opcion: f"{opcion} días",
    )
    dias = dias or 30

    resumen = resumen_ventas(
        ventas_db.listar_ventas(), _precios(), _costos_variables(), dias
    )

    col_unidades, col_ingreso, col_margen, col_promedio = st.columns(4)
    col_unidades.metric(
        "Unidades", f"{resumen['unidades']:,.0f}", icon=":material/sell:"
    )
    col_ingreso.metric(
        "Ingresos", f"${resumen['ingreso']:,.2f}", icon=":material/attach_money:"
    )
    col_margen.metric(
        "Margen de contribución",
        f"${resumen['margen']:,.2f}",
        icon=":material/trending_up:",
    )
    col_promedio.metric(
        "Promedio diario", f"{resumen['promedio_diario']:,.1f}", icon=":material/today:"
    )

    fijos_periodo = _fijos_mensuales(*_supuestos()) * dias / DIAS_POR_MES
    comp = comparacion(resumen, fijos_periodo)

    st.subheader("Comparación con el punto de equilibrio", icon=":material/compare_arrows:")
    col_fijos, col_cobertura, col_resultado = st.columns(3)
    col_fijos.metric(
        "Costos fijos del periodo",
        f"${fijos_periodo:,.2f}",
        icon=":material/lock:",
        help=f"Costos fijos mensuales prorrateados a {dias} días.",
    )
    col_cobertura.metric(
        "Cobertura",
        f"{comp['cobertura'] * 100:,.1f}%",
        icon=":material/donut_small:",
        help="Margen de contribución real ÷ costos fijos del periodo.",
    )
    col_resultado.metric(
        "Resultado",
        f"${comp['resultado']:,.2f}",
        icon=":material/insights:",
        help="Margen real − costos fijos. Positivo = utilidad; negativo = faltante.",
    )

    if comp["cobertura"] >= 1:
        st.success(f"Estás por encima del equilibrio: excedente ${comp['resultado']:,.2f}.")
    else:
        st.warning(f"Faltan ${-comp['resultado']:,.2f} para cubrir los fijos del periodo.")
    if comp["equilibrio_unidades"] is not None:
        st.caption(
            f"Equilibrio ≈ {comp['equilibrio_unidades']:,.0f} unidades en {dias} días; "
            f"llevas {resumen['unidades']:,.0f} ({comp['diferencia_unidades']:+,.0f})."
        )

    if resumen["por_sabor"]:
        st.subheader("Por sabor", icon=":material/donut_small:")
        st.dataframe(
            [
                {
                    "Sabor": fila["sabor"],
                    "Unidades": fila["unidades"],
                    "Ingresos": fila["ingreso"],
                    "Margen": fila["margen"],
                }
                for fila in resumen["por_sabor"]
            ],
            hide_index=True,
            column_config={
                "Unidades": st.column_config.NumberColumn(format="%.0f"),
                "Ingresos": st.column_config.NumberColumn(format="$%.2f"),
                "Margen": st.column_config.NumberColumn(format="$%.2f"),
            },
        )
    else:
        st.caption(f"Sin ventas registradas en los últimos {dias} días.")
