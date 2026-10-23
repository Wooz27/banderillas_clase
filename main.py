import streamlit as st
from streamlit_option_menu import option_menu

from db.database import init_db
from screens import (
    analisis,
    gastos,
    herramientas,
    insumos,
    productos,
    punto_equilibrio,
    ventas,
)

init_db()

PANTALLAS = [
    ("Insumos", "box-seam", insumos.mostrar),
    ("Gastos", "receipt", gastos.mostrar),
    ("Productos", "tag", productos.mostrar),
    ("Herramientas", "tools", herramientas.mostrar),
    ("Ventas", "cart", ventas.mostrar),
    ("Análisis de ventas", "graph-up", analisis.mostrar),
    ("Punto de equilibrio", "clipboard-data", punto_equilibrio.mostrar),
]


def main() -> None:
    st.set_page_config(
        page_title="Control de Costos",
        page_icon=":material/payments:",
        layout="wide",
    )

    with st.sidebar:
        st.header("Control de Costos", icon=":material/payments:")
        seleccion = option_menu(
            menu_title=None,
            options=[nombre for nombre, _, _ in PANTALLAS],
            icons=[icono for _, icono, _ in PANTALLAS],
            default_index=0,
            key="menu_principal",
        )

    mostrar = next(mostrar for nombre, _, mostrar in PANTALLAS if nombre == seleccion)
    mostrar()


if __name__ == "__main__":
    main()
