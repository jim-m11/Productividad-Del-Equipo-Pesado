"""Cargador frontal (v3): datos en pestañas, interruptores, sliders y tabla
editable; la solución se muestra como una hoja de resolución paso a paso."""
import pandas as pd
import plotly.express as px
import streamlit as st

import calculos
import estado
from formato import dec, red, fmt
from tablas import MODELOS_CARGADOR, FACTORES, FACTORES_PLANOS, MATERIALES

CLAVE = "cf_res"

# ------------------------------ EJEMPLOS ------------------------------
EJEMPLOS = {
    "Ejemplo 1 · Arena húmeda": dict(
        prd=85000.0, hd=16, modelos=("966H", "988H"),
        factores=["Pila · Descargado por camión", "Varios · Operación intermitente"],
        tp=[("Espera de camiones", 3.0), ("Cambio de operador", 1.5)],
        modo="Tabla del manual", material="Arena húmeda", estado="Suelto",
        d=None, fc=None),
    "Ejemplo 2 · Datos manuales": dict(
        prd=48000.0, hd=12, modelos=("980H", "993K"),
        factores=[],
        tp=[("Mantenimiento menor", 2.0)],
        modo="Ingresar manualmente", material="Grava seca", estado="Suelto",
        d=1.85, fc=0.85),
}


def cargar_ejemplo(nombre):
    e, ss = EJEMPLOS[nombre], st.session_state
    ss["cf_prd"], ss["cf_hd"], ss["cf_modelos_def"] = e["prd"], e["hd"], e["modelos"]
    for k in FACTORES_PLANOS:
        ss[f"cf_t_{k}"] = k in e["factores"]
    ss["cf_extra"] = 0.0
    ss["cf_tp_base"] = pd.DataFrame(e["tp"], columns=["Concepto", "Min/h"])
    ss["cf_tp_ver"] = ss.get("cf_tp_ver", 0) + 1
    ss["cf_modo"], ss["cf_material"], ss["cf_estado"] = e["modo"], e["material"], e["estado"]
    ss["cf_d"], ss["cf_fc"] = e["d"], e["fc"]
    ss.pop(CLAVE, None)


def iniciar():
    ss = st.session_state
    ss.setdefault("cf_hd", 20)
    ss.setdefault("cf_modelos_def", (MODELOS_CARGADOR[0], MODELOS_CARGADOR[-1]))
    ss.setdefault("cf_extra", 0.0)
    ss.setdefault("cf_tp_ver", 0)
    ss.setdefault("cf_tp_base", pd.DataFrame({"Concepto": ["Tiempo perdido"],
                                              "Min/h": [0.0]}))
    ss.setdefault("cf_modo", "Tabla del manual")
    ss.setdefault("cf_estado", "Suelto")


# ------------------------------ ENTRADA ------------------------------
def panel_datos():
    ss = st.session_state
    st.markdown("##### ¿Quieres probar con un ejercicio de ejemplo?")
    cols = st.columns(len(EJEMPLOS) + 1)
    for col, nombre in zip(cols, EJEMPLOS):
        col.button(nombre, on_click=cargar_ejemplo, args=(nombre,),
                   key=f"btn_{nombre}")

    t1, t2, t3 = st.tabs(["① PRODUCCIÓN Y EQUIPOS", "② CICLO Y PÉRDIDAS", "③ MATERIAL"])

    with t1:
        c1, c2 = st.columns(2)
        prd = c1.number_input("Producción requerida (t/día)", min_value=0.0,
                              value=None, placeholder="Ej. 85000", key="cf_prd")
        hd = c2.slider("Horas de trabajo al día", 1, 24, key="cf_hd")
        rango = st.select_slider("Cargadores disponibles (rango de modelos)",
                                 options=MODELOS_CARGADOR,
                                 value=ss["cf_modelos_def"],
                                 key=f"cf_modelos_{ss['cf_tp_ver']}")

    with t2:
        izq, der = st.columns(2, gap="large")
        with izq:
            st.markdown("**Factores de corrección del ciclo** (pág. 998)")
            seleccion = []
            for categoria, opciones in FACTORES.items():
                st.caption(categoria.upper())
                for nombre in opciones:
                    clave = f"{categoria} · {nombre}"
                    if st.toggle(f"{nombre}  ({opciones[nombre]:+.2f} min)",
                                 key=f"cf_t_{clave}"):
                        seleccion.append(clave)
            extra = st.number_input("Corrección adicional (min)", step=0.01,
                                    format="%.2f", key="cf_extra",
                                    help="Si el enunciado da un valor distinto al manual.")
        with der:
            st.markdown("**Tiempo perdido** (min por hora)")
            st.caption("Agrega una fila por cada pérdida; se suman solas.")
            tabla = st.data_editor(
                ss["cf_tp_base"], num_rows="dynamic", hide_index=True,
                key=f"cf_tp_ed_{ss['cf_tp_ver']}",
                column_config={"Min/h": st.column_config.NumberColumn(
                    "Min/h", min_value=0.0, format="%.2f")})

    with t3:
        modo = st.radio("Origen de la densidad y el factor de carga",
                        ["Tabla del manual", "Ingresar manualmente"],
                        horizontal=True, key="cf_modo")
        if modo == "Tabla del manual":
            c1, c2 = st.columns([2, 1])
            material = c1.selectbox("Material (pág. 1575)", list(MATERIALES),
                                    key="cf_material")
            est = c2.radio("Estado", ["Suelto", "En banco"], horizontal=True,
                           key="cf_estado")
            ds, db, fc = MATERIALES[material]
            d = ds if est == "Suelto" else db
            st.info(f"Densidad D = {d} t/m³   ·   Factor de carga Fc = {fc}")
        else:
            c1, c2 = st.columns(2)
            d = c1.number_input("Densidad D (t/m³)", min_value=0.0, value=None,
                                format="%.3f", key="cf_d")
            fc = c2.number_input("Factor de carga Fc", min_value=0.0, value=None,
                                 format="%.3f", key="cf_fc",
                                 help="Si es 80 %, escribe 0.80")

    st.write("")
    if st.button("▶  RESOLVER EJERCICIO", type="primary"):
        resolver(prd, hd, rango, seleccion, extra, tabla, d, fc)


def resolver(prd, hd, rango, seleccion, extra, tabla, d, fc):
    ss = st.session_state
    try:
        vals = [dec(v) for v in tabla["Min/h"].dropna()]
        if any(v < 0 for v in vals):
            raise ValueError
        tp = red(sum(vals, dec(0)))
    except Exception:
        st.error("Revisa la tabla de tiempo perdido.")
        return
    if not prd:
        st.error("Ingresa la producción requerida.")
        return
    if not d or not fc:
        st.error("Falta la densidad o el factor de carga.")
        return
    if tp >= 60:
        st.error("El tiempo perdido debe ser menor a 60 min/h.")
        return
    i, j = (MODELOS_CARGADOR.index(m) for m in rango)
    fact = red(sum((dec(FACTORES_PLANOS[k]) for k in seleccion), dec(0)) + dec(extra))
    try:
        res = calculos.cargador(prd, hd, MODELOS_CARGADOR[i:j + 1], fact, tp, d, fc)
    except ValueError as e:
        st.error(str(e))
        return
    res["seleccion"] = seleccion
    res["tp_vals"] = vals
    ss[CLAVE] = res
    m = res["mejor"]
    estado.agregar(f"Cargador {m['Modelo']} × {m['N']} · {fmt(prd)} t/día")


# ------------------------------ SALIDA ------------------------------
def paso(n, titulo, formulas, resultado):
    with st.container(border=True):
        st.markdown(f"**PASO {n} · {titulo}**")
        for f in formulas:
            st.latex(f)
        st.markdown(f"➜ **{resultado}**")


def hoja(res):
    m = res["mejor"]
    st.markdown(
        f'<div class="respuesta"><small>RESPUESTA</small>'
        f'<h2>{m["N"]} cargador(es) CAT {m["Modelo"]}</h2>'
        f'<p>Cucharón de {m["Cchr"]} m³ · producción total {fmt(m["Total"])} t/día '
        f'· exceso {fmt(m["Exceso"])} t/día</p></div>', unsafe_allow_html=True)

    st.markdown("### HOJA DE RESOLUCIÓN")
    paso(1, "Producción requerida por hora",
         [rf"Prh=\frac{{Prd}}{{Hd}}=\frac{{{res['prd']}}}{{{res['hd']}}}"],
         f"Prh = {res['prh']} t/h")

    lista = " ".join(f"({FACTORES_PLANOS[k]:+.2f})" for k in res["seleccion"]) or "0"
    paso(2, "Tiempo de ciclo",
         [rf"Fact={lista.replace(') (', ')+(')}={res['fact']}",
          rf"TC=Tcb+Fact={m['Tcb']}+({res['fact']})"],
         f"TC = {m['TC']} min")

    suma = " + ".join(str(v) for v in res["tp_vals"]) or "0"
    paso(3, "Tiempo perdido y ciclos por hora",
         [rf"Tp={suma}={res['tp']}\ min/h",
          rf"Ctr=\frac{{60-Tp}}{{TC}}=\frac{{60-{res['tp']}}}{{{m['TC']}}}"],
         f"Ctr = {m['Ctr']} ciclos/h (entero superior)")

    paso(4, "Carga útil por ciclo",
         [rf"CUC=\frac{{Prh}}{{Ctr}}=\frac{{{res['prh']}}}{{{m['Ctr']}}}"],
         f"CUC = {m['CUC']} t/ciclo")

    paso(5, "Cucharón requerido",
         [rf"SCU=\frac{{CUC/D}}{{Fc}}=\frac{{{m['CUC']}/{res['d']}}}{{{res['fc']}}}"],
         f"SCU = {m['SCU']} m³")

    paso(6, "Producción real de un cargador",
         [rf"Ef=\frac{{60-Tp}}{{60}}={res['ef']}",
          rf"Prd_{{real}}=Cchr\cdot Ctr\cdot Ef\cdot Fc\cdot Hd\cdot D",
          rf"Prd_{{real}}={m['Cchr']}\cdot{m['Ctr']}\cdot{res['ef']}\cdot{res['fc']}"
          rf"\cdot{res['hd']}\cdot{res['d']}"],
         f"Prd real = {fmt(m['PrdReal'])} t/día")

    paso(7, "Cantidad de cargadores",
         [rf"N=\left\lceil\frac{{Prd}}{{Prd_{{real}}}}\right\rceil="
          rf"\left\lceil\frac{{{res['prd']}}}{{{m['PrdReal']}}}\right\rceil",
          rf"Total=N\cdot Prd_{{real}}={m['N']}\cdot{m['PrdReal']}",
          rf"Exceso=Total-Prd={m['Total']}-{res['prd']}"],
         f"N = {m['N']} · Total = {fmt(m['Total'])} t/día · Exceso = {fmt(m['Exceso'])} t/día")

    df = pd.DataFrame([{
        "Alternativa": f"{r['Modelo']} · {r['Cchr']} m³", "Modelo": r["Modelo"],
        "Cucharón (m³)": float(r["Cchr"]), "TC (min)": float(r["TC"]),
        "Ciclos/h": r["Ctr"], "SCU (m³)": float(r["SCU"]),
        "Prod. real (t/día)": float(r["PrdReal"]), "Cargadores": r["N"],
        "Total (t/día)": float(r["Total"]), "Exceso (t/día)": float(r["Exceso"]),
    } for r in res["filas"]])

    st.markdown("### COMPARACIÓN DE ALTERNATIVAS")
    fig = px.scatter(df, x="Alternativa", y="Total (t/día)", color="Modelo",
                     size="Cargadores", hover_data=["Exceso (t/día)"],
                     title="Producción total de cada alternativa vs. la requerida")
    fig.add_hline(y=float(res["prd"]), line_dash="dash", line_color="#FFC400",
                  annotation_text="Requerida", annotation_font_color="#FFC400")
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", height=420,
                      margin=dict(l=0, r=0, t=50, b=0), xaxis_tickangle=-45)
    st.plotly_chart(fig)
    with st.expander("📋 Tabla completa"):
        st.dataframe(df.drop(columns=["Alternativa"]), hide_index=True)
        st.download_button("⬇️ Descargar CSV",
                           df.to_csv(index=False).encode("utf-8-sig"),
                           "alternativas_cargador.csv", "text/csv")


def mostrar():
    iniciar()
    panel_datos()
    res = st.session_state.get(CLAVE)
    if res:
        st.divider()
        hoja(res)
