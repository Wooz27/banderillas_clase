import numpy as np
import pandas as pd
import streamlit as st

from components.editor_tabla import agregar_fila, editor_con_calculos


def _texto(valor) -> str:
    return str(valor).strip() if pd.notna(valor) else ""


def _numero(valor) -> float:
    return float(valor) if pd.notna(valor) else 0.0


def _valor(dtype: str, valor):
    if dtype == "string":
        return _texto(valor)
    if dtype == "object":
        return valor if isinstance(valor, list) else []
    if dtype.startswith("datetime"):
        return pd.Timestamp(valor).date() if pd.notna(valor) else None
    return _numero(valor)


def _crear_tabla(listar, dtypes: dict, filtro) -> pd.DataFrame:
    registros = listar()
    if filtro is not None:
        registros = [registro for registro in registros if filtro(registro)]
    return pd.DataFrame(registros).reindex(columns=list(dtypes)).astype(dtypes)


def _fila_vacia(dtypes: dict, valores_iniciales: dict | None = None) -> dict:
    fila = {
        columna: [] if dtype == "object" else np.nan
        for columna, dtype in dtypes.items()
    }
    fila.update(valores_iniciales or {})
    return fila


def _fila_guardable(
    fila: dict, dtypes: dict, campos_fijos: dict | None, columna_clave: str
) -> dict | None:
    if not _texto(fila[columna_clave]):
        return None
    datos = {columna: _valor(dtype, fila[columna]) for columna, dtype in dtypes.items()}
    datos.update(campos_fijos or {})
    return datos


def _filas_guardables(
    tabla: pd.DataFrame, dtypes: dict, campos_fijos, columna_clave: str
) -> list[dict]:
    filas = (
        _fila_guardable(fila, dtypes, campos_fijos, columna_clave)
        for fila in tabla.to_dict("records")
    )
    return [fila for fila in filas if fila is not None]


def _autoguardar(tabla, clave_firma, dtypes, campos_fijos, guardar, columna_clave) -> None:
    filas = _filas_guardables(tabla, dtypes, campos_fijos, columna_clave)
    firma = str(filas)
    if st.session_state.get(clave_firma) == firma:
        return
    guardar(filas)
    st.session_state[clave_firma] = firma


def pantalla_tabla(
    *,
    clave_tabla: str,
    clave_version: str,
    clave_firma: str,
    dtypes: dict,
    config_columnas: dict,
    columnas_calculo: dict,
    listar,
    guardar,
    etiqueta_agregar: str,
    icono_agregar: str,
    filtro=None,
    campos_fijos: dict | None = None,
    columna_clave: str = "nombre",
    valores_iniciales: dict | None = None,
) -> pd.DataFrame:
    tabla = editor_con_calculos(
        clave_tabla=clave_tabla,
        clave_version=clave_version,
        config_columnas=config_columnas,
        columnas_calculo=columnas_calculo,
        crear_tabla=lambda: _crear_tabla(listar, dtypes, filtro),
    )
    _autoguardar(tabla, clave_firma, dtypes, campos_fijos, guardar, columna_clave)

    if st.button(etiqueta_agregar, key=f"agregar_{clave_tabla}", icon=icono_agregar):
        agregar_fila(clave_tabla, dtypes, _fila_vacia(dtypes, valores_iniciales))
        st.rerun()
    return tabla
