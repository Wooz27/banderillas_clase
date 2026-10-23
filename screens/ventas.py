from datetime import date

import streamlit as st

from components.pantalla_tabla import pantalla_tabla
from db import productos as productos_db
from db import ventas as ventas_db
from utils.costos import numero

CLAVE_TABLA = "tabla_ventas"
CLAVE_VERSION = "ventas_version"
CLAVE_FIRMA = "ventas_firma_guardada"

DTYPES = {"fecha": "datetime64[ns]", "sabor": "string", "cantidad": "float"}


def _config_columnas() -> dict:
    return {
        "fecha": st.column_config.DateColumn("Fecha", format="DD/MM/YYYY", required=True),
        "sabor": st.column_config.SelectboxColumn(
            "Sabor",
            options=[producto["nombre"] for producto in productos_db.listar_productos()],
            required=True,
        ),
        "cantidad": st.column_config.NumberColumn(
            "Cantidad", min_value=0.0, step=1.0, format="%.0f"
        ),
        "importe": st.column_config.NumberColumn("Importe", format="$%.2f"),
    }


def _importe(fila: dict, precios: dict) -> float:
    return numero(fila["cantidad"]) * numero(precios.get(fila["sabor"]))


def mostrar() -> None:
    st.title("Ventas", icon=":material/shopping_cart:")

    precios = {producto["nombre"]: producto["precio"] for producto in productos_db.listar_productos()}

    pantalla_tabla(
        clave_tabla=CLAVE_TABLA,
        clave_version=CLAVE_VERSION,
        clave_firma=CLAVE_FIRMA,
        dtypes=DTYPES,
        config_columnas=_config_columnas(),
        columnas_calculo={"importe": lambda fila: _importe(fila, precios)},
        listar=ventas_db.listar_ventas,
        guardar=ventas_db.guardar_ventas,
        etiqueta_agregar="Agregar venta",
        icono_agregar=":material/add:",
        columna_clave="sabor",
        valores_iniciales={"fecha": date.today()},
    )
