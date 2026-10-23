import streamlit as st

from components.pantalla_tabla import pantalla_tabla
from db import productos as productos_db

CLAVE_TABLA = "tabla_productos"
CLAVE_VERSION = "productos_version"
CLAVE_FIRMA = "productos_firma_guardada"

DTYPES = {"nombre": "string", "precio": "float"}

CONFIG_COLUMNAS = {
    "nombre": st.column_config.TextColumn("Sabor", required=True),
    "precio": st.column_config.NumberColumn(
        "Precio", min_value=0.0, step=0.5, format="$%.2f"
    ),
}


def mostrar() -> None:
    st.title("Productos", icon=":material/tag:")

    pantalla_tabla(
        clave_tabla=CLAVE_TABLA,
        clave_version=CLAVE_VERSION,
        clave_firma=CLAVE_FIRMA,
        dtypes=DTYPES,
        config_columnas=CONFIG_COLUMNAS,
        columnas_calculo={},
        listar=productos_db.listar_productos,
        guardar=productos_db.guardar_productos,
        etiqueta_agregar="Agregar sabor",
        icono_agregar=":material/add:",
    )
