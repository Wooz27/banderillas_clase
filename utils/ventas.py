from datetime import date, timedelta

from utils.costos import numero


def ventas_periodo(
    ventas: list[dict], dias: int, hoy: date | None = None
) -> list[dict]:
    corte = (hoy or date.today()) - timedelta(days=max(int(dias) - 1, 0))
    return [venta for venta in ventas if venta["fecha"] and venta["fecha"] >= corte]


def _importe(ventas: list[dict], sabor: str, precios: dict) -> float:
    return sum(
        numero(venta["cantidad"]) for venta in ventas if venta["sabor"] == sabor
    ) * numero(precios.get(sabor))


def _margen(ventas: list[dict], sabor: str, precios: dict, costos: dict) -> float:
    return sum(
        numero(venta["cantidad"]) for venta in ventas if venta["sabor"] == sabor
    ) * (numero(precios.get(sabor)) - numero(costos.get(sabor)))


def _unidades(ventas: list[dict], sabor: str) -> float:
    return sum(numero(venta["cantidad"]) for venta in ventas if venta["sabor"] == sabor)


def resumen_ventas(
    ventas: list[dict],
    precios: dict,
    costos: dict,
    dias: int = 30,
    hoy: date | None = None,
) -> dict:
    periodo = ventas_periodo(ventas, dias, hoy)
    unidades = sum(numero(venta["cantidad"]) for venta in periodo)
    ingreso = sum(
        numero(venta["cantidad"]) * numero(precios.get(venta["sabor"]))
        for venta in periodo
    )
    costo_variable = sum(
        numero(venta["cantidad"]) * numero(costos.get(venta["sabor"]))
        for venta in periodo
    )
    margen = ingreso - costo_variable
    return {
        "dias": dias,
        "unidades": unidades,
        "ingreso": ingreso,
        "costo_variable": costo_variable,
        "margen": margen,
        "promedio_diario": unidades / dias if dias else 0.0,
        "margen_unitario": margen / unidades if unidades else 0.0,
        "por_sabor": [
            {
                "sabor": sabor,
                "unidades": _unidades(periodo, sabor),
                "ingreso": _importe(periodo, sabor, precios),
                "margen": _margen(periodo, sabor, precios, costos),
            }
            for sabor in sorted({venta["sabor"] for venta in periodo})
        ],
    }


def comparacion(resumen: dict, costos_fijos: float) -> dict:
    margen = resumen["margen"]
    margen_unitario = resumen["margen_unitario"]
    equilibrio = costos_fijos / margen_unitario if margen_unitario > 0 else None
    return {
        "cobertura": margen / costos_fijos if costos_fijos else 0.0,
        "resultado": margen - costos_fijos,
        "equilibrio_unidades": equilibrio,
        "diferencia_unidades": resumen["unidades"] - equilibrio
        if equilibrio is not None
        else None,
    }
