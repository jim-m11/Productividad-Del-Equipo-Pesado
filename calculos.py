"""Toda la matemática del proyecto (sin elementos de pantalla)."""
from formato import dec, red, techo
from tablas import (TIEMPOS_CICLO, CAPACIDADES, EXCLUIDAS)


# ------------------------- CARGADOR FRONTAL -------------------------
def leer_tp(texto):
    """'5; 0.04' -> (lista de valores, suma redondeada)."""
    valores = [dec(x.strip().replace(",", ".")) for x in texto.split(";") if x.strip()]
    if not valores or any((not v.is_finite()) or v < 0 for v in valores):
        raise ValueError("Tiempo perdido inválido")
    return valores, red(sum(valores))


def cargador(prd, hd, modelos, fact, tp, d, fc):
    prd, hd, d, fc = dec(prd), dec(hd), dec(d), dec(fc)
    prh = red(prd / hd)
    ef = red((60 - tp) / 60)
    filas = []
    for modelo in modelos:
        tcb = dec(TIEMPOS_CICLO[modelo])
        tc = red(tcb + fact)
        if tc <= 0:
            raise ValueError(f"Tiempo de ciclo inválido para {modelo}")
        ctr = techo((60 - tp) / tc)
        cuc = red(prh / ctr)
        scu = red((cuc / d) / fc)
        for cap in CAPACIDADES[modelo]:
            if cap in EXCLUIDAS.get(modelo, []):
                continue
            cap = dec(cap)
            pr = red(cap * ctr * ef * fc * hd * d)
            if pr <= 0:
                continue
            n = techo(prd / pr)
            total = red(pr * n)
            filas.append(dict(Modelo=modelo, Tcb=tcb, TC=tc, Ctr=ctr, CUC=cuc,
                              SCU=scu, Cchr=cap, PrdReal=pr, N=n, Total=total,
                              Exceso=red(total - prd)))
    if not filas:
        raise ValueError("No hay alternativas válidas")
    return dict(prd=prd, hd=hd, prh=prh, ef=ef, tp=tp, d=d, fc=fc, fact=fact,
                filas=filas, mejor=min(filas, key=lambda r: r["Exceso"]))


# ------------------------- MOTONIVELADORA -------------------------
def productividad(S, le, lo, E):
    ancho = red(dec(le) - dec(lo))
    return ancho, red(dec(S) * ancho * 1000 * dec(E))


def tiempo_trabajo(at, LT, npas, A, htd):
    AT = red(dec(at) * dec(LT) * dec(npas))
    NH = red(AT / A)
    return AT, NH, techo(NH / dec(htd))


def traccion(wr, T):
    return red(dec(wr) * dec(T))


def fuerza_descendente(wb, ba, fw):
    dif = dec(wb) - dec(ba)
    return dif, red(dec(wb) / dif * dec(fw))
