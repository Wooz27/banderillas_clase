import math
from datetime import date

MERMA_MAXIMA = 100.0
UNIDADES = ("Hora", "Día", "Mes")
DIAS_POR_MES = 30.0
HORAS_POR_DIA = 8.0
MESES_POR_ANIO = 12


def numero(valor) -> float:
    if valor is None:
        return 0.0
    try:
        resultado = float(valor)
    except (TypeError, ValueError):
        return 0.0
    return 0.0 if math.isnan(resultado) else resultado


def rinde_neto(rinde: float, merma_porcentaje: float = 0.0) -> float:
    porcentaje = min(max(numero(merma_porcentaje), 0.0), MERMA_MAXIMA)
    return numero(rinde) * (1 - porcentaje / 100)


def costo_unitario(precio: float, rinde: float, merma_porcentaje: float = 0.0) -> float:
    neto = rinde_neto(rinde, merma_porcentaje)
    if not neto:
        return 0.0
    return numero(precio) / neto


def costo_variable_sabor(insumos: list[dict], sabor: str) -> float:
    return sum(
        costo_unitario(insumo["precio"], insumo["rinde"], insumo["mermas"])
        for insumo in insumos
        if sabor in (insumo["sirve_para"] or [])
    )


def por_unidad(monto: float, cantidad: float = 1.0) -> float:
    cantidad = numero(cantidad)
    return numero(monto) / cantidad if cantidad else 0.0


def costo_mensual(
    monto: float,
    unidad: str,
    cantidad: float = 1.0,
    dias_mes: float = DIAS_POR_MES,
    horas_dia: float = HORAS_POR_DIA,
) -> float:
    dias = numero(dias_mes)
    factor_por_unidad = dict(zip(UNIDADES, (dias * numero(horas_dia), dias, 1.0)))
    return por_unidad(monto, cantidad) * factor_por_unidad.get(unidad, 1.0)


def gastos_mensuales(
    gastos: list[dict],
    dias_mes: float = DIAS_POR_MES,
    horas_dia: float = HORAS_POR_DIA,
) -> float:
    return sum(
        costo_mensual(
            gasto["monto"], gasto["unidad"], gasto["cantidad"], dias_mes, horas_dia
        )
        for gasto in gastos
    )


def depreciacion_mensual(
    costo: float, vida_util: float, valor_rescate: float = 0.0
) -> float:
    meses = numero(vida_util) * MESES_POR_ANIO
    if not meses:
        return 0.0
    return max(numero(costo) - numero(valor_rescate), 0.0) / meses


def _meses_depreciados(
    vida_util: float, fecha_compra: date | None, hoy: date | None = None
) -> float:
    if fecha_compra is None:
        return 0.0
    hoy = hoy or date.today()
    transcurridos = (hoy.year - fecha_compra.year) * MESES_POR_ANIO
    transcurridos += hoy.month - fecha_compra.month
    if hoy.day < fecha_compra.day:
        transcurridos -= 1
    return min(max(transcurridos, 0), numero(vida_util) * MESES_POR_ANIO)


def depreciacion_vigente(
    costo: float,
    vida_util: float,
    valor_rescate: float = 0.0,
    fecha_compra: date | None = None,
    hoy: date | None = None,
) -> float:
    vida_meses = numero(vida_util) * MESES_POR_ANIO
    if fecha_compra is not None:
        if _meses_depreciados(vida_util, fecha_compra, hoy) >= vida_meses:
            return 0.0
    return depreciacion_mensual(costo, vida_util, valor_rescate)


def depreciacion_total(herramientas: list[dict]) -> float:
    return sum(
        depreciacion_vigente(
            herramienta["costo"],
            herramienta["vida_util"],
            herramienta["valor_rescate"],
            herramienta["fecha_compra"],
        )
        for herramienta in herramientas
    )


def valor_en_libros(
    costo: float,
    vida_util: float,
    valor_rescate: float = 0.0,
    fecha_compra: date | None = None,
    hoy: date | None = None,
) -> float:
    depreciado = depreciacion_mensual(costo, vida_util, valor_rescate)
    depreciado *= _meses_depreciados(vida_util, fecha_compra, hoy)
    return max(numero(costo) - depreciado, 0.0)


def punto_equilibrio(
    precio: float, costo_variable: float, costos_fijos: float
) -> float | None:
    margen = numero(precio) - numero(costo_variable)
    if margen <= 0:
        return None
    return numero(costos_fijos) / margen
