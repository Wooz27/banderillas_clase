import streamlit as st
from sqlalchemy import delete, select

from db.database import SessionLocal
from db.models import Venta

CAMPOS = ("fecha", "sabor", "cantidad")


@st.cache_data
def listar_ventas() -> list[dict]:
    with SessionLocal() as session:
        ventas = session.scalars(select(Venta).order_by(Venta.fecha)).all()
    return [{campo: getattr(venta, campo) for campo in CAMPOS} for venta in ventas]


def guardar_ventas(filas: list[dict]) -> None:
    with SessionLocal() as session:
        session.execute(delete(Venta))
        for fila in filas:
            session.add(Venta(**fila))
        session.commit()
    listar_ventas.clear()
