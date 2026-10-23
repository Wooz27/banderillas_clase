import streamlit as st
from sqlalchemy import delete, select

from db.database import SessionLocal
from db.models import Herramienta

CAMPOS = ("nombre", "fecha_compra", "costo", "vida_util", "valor_rescate")


@st.cache_data
def listar_herramientas() -> list[dict]:
    with SessionLocal() as session:
        herramientas = session.scalars(
            select(Herramienta).order_by(Herramienta.nombre)
        ).all()
    return [
        {campo: getattr(herramienta, campo) for campo in CAMPOS}
        for herramienta in herramientas
    ]


def guardar_herramientas(filas: list[dict]) -> None:
    with SessionLocal() as session:
        session.execute(delete(Herramienta))
        for fila in filas:
            session.add(Herramienta(**fila))
        session.commit()
    listar_herramientas.clear()
