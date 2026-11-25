"""Funciones auxiliares de redondeo y formato (usan Decimal para que
los resultados coincidan con los de un cálculo hecho a mano)."""
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING


def dec(valor):
    return Decimal(str(valor))


def red(valor):
    """Redondea a 2 decimales (mitad hacia arriba)."""
    return dec(valor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def techo(valor):
    """Aproxima al entero superior."""
    return int(dec(valor).to_integral_value(rounding=ROUND_CEILING))


def fmt(valor):
    """Formato con separador de miles y 2 decimales."""
    return f"{float(valor):,.2f}"
