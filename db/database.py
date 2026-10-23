from pathlib import Path

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DB_PATH = Path(__file__).resolve().parent.parent / "costos.db"

engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def _agregar_columnas_faltantes() -> None:
    inspector = inspect(engine)
    tablas_existentes = set(inspector.get_table_names())
    for tabla in Base.metadata.sorted_tables:
        if tabla.name not in tablas_existentes:
            continue
        existentes = {columna["name"] for columna in inspector.get_columns(tabla.name)}
        for columna in tabla.columns:
            if columna.name in existentes:
                continue
            tipo = columna.type.compile(engine.dialect)
            with engine.begin() as conexion:
                conexion.execute(
                    text(f"ALTER TABLE {tabla.name} ADD COLUMN {columna.name} {tipo}")
                )


def init_db() -> None:
    from db import models

    Base.metadata.create_all(engine)
    _agregar_columnas_faltantes()
