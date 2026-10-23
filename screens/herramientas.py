import pandas as pd
import streamlit as st

from components.pantalla_tabla import pantalla_tabla
from db import herramientas as herramientas_db
from utils.costos import depreciacion_vigente, valor_en_libros

CLAVE_TABLA = "tabla_herramientas"
CLAVE_VERSION = "herramientas_version"
CLAVE_FIRMA = "herramientas_firma_guardada"

DTYPES = {
    "nombre": "string",
    "fecha_compra": "datetime64[ns]",
    "costo": "float",
    "vida_util": "float",
    "valor_rescate": "float",
}

CONFIG_COLUMNAS = {
    "nombre": st.column_config.TextColumn("Herramienta", required=True),
    "fecha_compra": st.column_config.DateColumn("Fecha de compra", format="DD/MM/YYYY"),
    "costo": st.column_config.NumberColumn(
        "Costo", min_value=0.0, step=1.0, format="$%.2f"
    ),
    "vida_util": st.column_config.NumberColumn(
        "Vida útil (años)", min_value=0.0, step=1.0, format="%.1f"
    ),
    "valor_rescate": st.column_config.NumberColumn(
        "Valor de rescate", min_value=0.0, step=1.0, format="$%.2f"
    ),
    "depreciacion": st.column_config.NumberColumn("Depreciación/mes", format="$%.2f"),
    "valor_libros": st.column_config.NumberColumn("Valor en libros", format="$%.2f"),
}


def _fecha(valor):
    return pd.Timestamp(valor).date() if pd.notna(valor) else None


def _depreciacion(fila: dict) -> float:
    return depreciacion_vigente(
        fila["costo"],
        fila["vida_util"],
        fila["valor_rescate"],
        _fecha(fila["fecha_compra"]),
    )


def _valor_libros(fila: dict) -> float:
    return valor_en_libros(
        fila["costo"],
        fila["vida_util"],
        fila["valor_rescate"],
        _fecha(fila["fecha_compra"]),
    )


def mostrar() -> None:
    st.title("Herramientas", icon=":material/handyman:")

    pantalla_tabla(
        clave_tabla=CLAVE_TABLA,
        clave_version=CLAVE_VERSION,
        clave_firma=CLAVE_FIRMA,
        dtypes=DTYPES,
        config_columnas=CONFIG_COLUMNAS,
        columnas_calculo={
            "depreciacion": _depreciacion,
            "valor_libros": _valor_libros,
        },
        listar=herramientas_db.listar_herramientas,
        guardar=herramientas_db.guardar_herramientas,
        etiqueta_agregar="Agregar herramienta",
        icono_agregar=":material/add:",
    )
