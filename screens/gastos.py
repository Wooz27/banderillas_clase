import streamlit as st

from components.pantalla_tabla import pantalla_tabla
from db import gastos as gastos_db
from db.models import TIPOS_GASTO
from utils.costos import (
    DIAS_POR_MES,
    HORAS_POR_DIA,
    UNIDADES,
    costo_mensual,
    por_unidad,
)

CLAVE_TABLA = "tabla_gastos"
CLAVE_VERSION = "gastos_version"
CLAVE_FIRMA = "gastos_firma_guardada"

DTYPES = {
    "nombre": "string",
    "tipo": "string",
    "monto": "float",
    "unidad": "string",
    "cantidad": "float",
}

CONFIG_COLUMNAS = {
    "nombre": st.column_config.TextColumn("Gasto", required=True),
    "tipo": st.column_config.SelectboxColumn(
        "Tipo", options=list(TIPOS_GASTO), default=TIPOS_GASTO[0], required=True
    ),
    "monto": st.column_config.NumberColumn(
        "Monto", min_value=0.0, step=1.0, format="$%.2f"
    ),
    "unidad": st.column_config.SelectboxColumn(
        "Unidad", options=list(UNIDADES), default=UNIDADES[-1], required=True
    ),
    "cantidad": st.column_config.NumberColumn(
        "Cantidad", min_value=0.0, step=1.0, format="%.2f"
    ),
    "costo_unitario": st.column_config.NumberColumn(
        "Costo por unidad", format="$%.2f"
    ),
    "costo_mensual": st.column_config.NumberColumn(
        "Costo mensual", format="$%.2f"
    ),
}


def _supuestos() -> tuple[float, float]:
    with st.expander("Supuestos", icon=":material/tune:"):
        dias = st.number_input(
            "Días por mes", min_value=1.0, step=1.0, value=DIAS_POR_MES, key="gastos_dias_mes"
        )
        horas = st.number_input(
            "Horas por día", min_value=1.0, step=1.0, value=HORAS_POR_DIA, key="gastos_horas_dia"
        )
    return dias, horas


def mostrar() -> None:
    st.title("Gastos", icon=":material/receipt_long:")
    dias, horas = _supuestos()

    pantalla_tabla(
        clave_tabla=CLAVE_TABLA,
        clave_version=CLAVE_VERSION,
        clave_firma=CLAVE_FIRMA,
        dtypes=DTYPES,
        config_columnas=CONFIG_COLUMNAS,
        columnas_calculo={
            "costo_unitario": lambda fila: por_unidad(fila["monto"], fila["cantidad"]),
            "costo_mensual": lambda fila: costo_mensual(
                fila["monto"], fila["unidad"], fila["cantidad"], dias, horas
            ),
        },
        listar=gastos_db.listar_gastos,
        guardar=gastos_db.guardar_gastos,
        etiqueta_agregar="Agregar gasto",
        icono_agregar=":material/add:",
    )
