import streamlit as st
from sqlalchemy import delete, select

from db.database import SessionLocal
from db.models import Gasto

CAMPOS = ("nombre", "tipo", "monto", "unidad", "cantidad")


@st.cache_data
def listar_gastos() -> list[dict]:
    with SessionLocal() as session:
        gastos = session.scalars(select(Gasto).order_by(Gasto.nombre)).all()
    return [{campo: getattr(gasto, campo) for campo in CAMPOS} for gasto in gastos]


def guardar_gastos(filas: list[dict]) -> None:
    with SessionLocal() as session:
        session.execute(delete(Gasto))
        for fila in filas:
            session.add(Gasto(**fila))
        session.commit()
    listar_gastos.clear()
