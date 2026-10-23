import pandas as pd
import streamlit as st

COLUMNA_ELIMINAR = "eliminar"


def _version(clave_version: str) -> int:
    return st.session_state.get(clave_version, 0)


def _con_ediciones_pendientes(tabla: pd.DataFrame, key: str) -> pd.DataFrame:
    estado = st.session_state.get(key)
    if not estado:
        return tabla
    tabla = tabla.copy()
    for indice, cambios in (estado.get("edited_rows") or {}).items():
        if indice >= len(tabla):
            continue
        for columna, valor in cambios.items():
            if columna in tabla.columns:
                tabla.iat[int(indice), tabla.columns.get_loc(columna)] = valor
    return tabla


def _eliminar_fila(clave_tabla: str, key_boton: str) -> None:
    click = st.session_state.get(key_boton)
    tabla = st.session_state.get(clave_tabla)
    if click is None or tabla is None or len(tabla) <= int(click.row):
        return
    tabla.drop(index=int(click.row), inplace=True)
    tabla.reset_index(drop=True, inplace=True)


def editor_con_calculos(
    clave_tabla: str,
    clave_version: str,
    config_columnas: dict,
    columnas_calculo: dict,
    crear_tabla,
) -> pd.DataFrame:
    key = f"editor_{clave_tabla}_{_version(clave_version)}"
    key_eliminar = f"eliminar_{clave_tabla}"

    tabla = st.session_state.get(clave_tabla)
    if tabla is None:
        tabla = crear_tabla()

    tabla = tabla.copy()
    tabla = _con_ediciones_pendientes(tabla, key)
    for columna, calcular in columnas_calculo.items():
        tabla[columna] = [calcular(fila) for fila in tabla.to_dict("records")]
    tabla[COLUMNA_ELIMINAR] = ":material/delete:"

    orden = [
        *[c for c in tabla.columns if c not in columnas_calculo and c != COLUMNA_ELIMINAR],
        *columnas_calculo,
        COLUMNA_ELIMINAR,
    ]

    editada = st.data_editor(
        tabla[orden],
        key=key,
        num_rows="fixed",
        width="stretch",
        hide_index=True,
        disabled=list(columnas_calculo),
        column_config={
            **config_columnas,
            COLUMNA_ELIMINAR: st.column_config.ButtonColumn(
                " ",
                key=key_eliminar,
                on_click=_eliminar_fila,
                args=(clave_tabla, key_eliminar),
            ),
        },
    )

    columnas_internas = [COLUMNA_ELIMINAR, *columnas_calculo]
    limpia = editada.drop(columns=columnas_internas)
    st.session_state[clave_tabla] = limpia
    return limpia


def agregar_fila(clave_tabla: str, dtypes: dict, fila: dict) -> None:
    tabla = st.session_state.get(clave_tabla)
    if tabla is None:
        return
    nueva = pd.DataFrame([fila])
    st.session_state[clave_tabla] = (
        pd.concat([tabla, nueva.reindex(columns=tabla.columns)], ignore_index=True)
        .astype(dtypes)
    )
