import streamlit as st

from components.pantalla_tabla import pantalla_tabla
from db import insumos as insumos_db
from db import productos as productos_db
from db.models import TIPO_PRODUCCION
from utils.costos import MERMA_MAXIMA, costo_unitario, rinde_neto

CLAVE_TABLA = "tabla_produccion"
CLAVE_VERSION = "insumos_version"
CLAVE_FIRMA = "insumos_firma_guardada"

DTYPES = {
    "nombre": "string",
    "rinde": "float",
    "precio": "float",
    "mermas": "float",
    "sirve_para": "object",
}


def _config_columnas() -> dict:
    return {
        "nombre": st.column_config.TextColumn("Insumo", required=True),
        "rinde": st.column_config.NumberColumn("Rinde para", min_value=0.0, step=1.0),
        "precio": st.column_config.NumberColumn(
            "Precio", min_value=0.0, step=0.5, format="$%.2f"
        ),
        "mermas": st.column_config.NumberColumn(
            "Mermas (%)", min_value=0.0, max_value=MERMA_MAXIMA, step=1.0, format="%.1f%%"
        ),
        "sirve_para": st.column_config.MultiselectColumn(
            "Sirve para",
            options=[producto["nombre"] for producto in productos_db.listar_productos()],
        ),
        "rinde_real": st.column_config.NumberColumn("Rinde real", format="%.1f"),
        "costo_unitario": st.column_config.NumberColumn(
            "Costo por unidad", format="$%.2f"
        ),
    }


def _rinde_real(fila: dict) -> float:
    return rinde_neto(fila["rinde"], fila["mermas"])


def _costo_unitario(fila: dict) -> float:
    return costo_unitario(fila["precio"], fila["rinde"], fila["mermas"])


def mostrar() -> None:
    st.title("Insumos", icon=":material/inventory_2:")

    pantalla_tabla(
        clave_tabla=CLAVE_TABLA,
        clave_version=CLAVE_VERSION,
        clave_firma=CLAVE_FIRMA,
        dtypes=DTYPES,
        config_columnas=_config_columnas(),
        columnas_calculo={
            "rinde_real": _rinde_real,
            "costo_unitario": _costo_unitario,
        },
        listar=insumos_db.listar_insumos,
        guardar=insumos_db.guardar_insumos,
        etiqueta_agregar="Agregar insumo",
        icono_agregar=":material/add:",
        filtro=lambda registro: registro["tipo"] == TIPO_PRODUCCION,
        campos_fijos={"tipo": TIPO_PRODUCCION},
    )
