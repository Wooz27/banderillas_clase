import streamlit as st
from sqlalchemy import delete, select

from db.database import SessionLocal
from db.models import Insumo

SEPARADOR = "|"


def _sabores(texto: str | None) -> list[str]:
    return [sabor for sabor in (texto or "").split(SEPARADOR) if sabor]


def _texto(sabores: list[str] | None) -> str:
    return SEPARADOR.join(sabores or [])


@st.cache_data
def listar_insumos() -> list[dict]:
    with SessionLocal() as session:
        insumos = session.scalars(select(Insumo).order_by(Insumo.nombre)).all()
    return [
        {
            "nombre": insumo.nombre,
            "tipo": insumo.tipo,
            "rinde": insumo.rinde,
            "mermas": insumo.mermas,
            "precio": insumo.precio,
            "sirve_para": _sabores(insumo.sirve_para),
        }
        for insumo in insumos
    ]


def guardar_insumos(filas: list[dict]) -> None:
    with SessionLocal() as session:
        session.execute(delete(Insumo))
        for fila in filas:
            session.add(Insumo(**{**fila, "sirve_para": _texto(fila.get("sirve_para"))}))
        session.commit()
    listar_insumos.clear()
