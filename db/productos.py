import streamlit as st
from sqlalchemy import delete, select

from db.database import SessionLocal
from db.models import Producto


@st.cache_data
def listar_productos() -> list[dict]:
    with SessionLocal() as session:
        productos = session.scalars(select(Producto).order_by(Producto.nombre)).all()
    return [
        {"nombre": producto.nombre, "precio": producto.precio or 0.0}
        for producto in productos
    ]


def guardar_productos(filas: list[dict]) -> None:
    with SessionLocal() as session:
        session.execute(delete(Producto))
        for fila in filas:
            session.add(Producto(**fila))
        session.commit()
    listar_productos.clear()
