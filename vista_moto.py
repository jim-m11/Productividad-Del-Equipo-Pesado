"""Motoniveladora (v3): asistente por pasos con resultados en vivo."""
import pandas as pd
import streamlit as st

import calculos
from formato import dec, fmt
from tablas import MODELOS_MOTO, VELOCIDADES, LONGITUD_EFECTIVA, TRACCION

OTRO = "Otro material (manual)"
PASOS = ["Productividad", "Tiempo de trabajo", "Fuerza de tracción",
         "Fuerza descendente", "Resumen final"]
ANGULOS = list(LONGITUD_EFECTIVA)
CLAVES = ["mn_modelo", "mn_trabajo", "mn_angulo", "mn_lo", "mn_E", "mn_at",
          "mn_LT", "mn_unidad", "mn_htd", "mn_np", "mn_material", "mn_wr",
          "mn_T", "mn_wb", "mn_ba", "mn_fw"]

# ------------------------------ EJEMPLOS ------------------------------
EJEMPLOS = {
    "Ejemplo 1 · Camino de acarreo": dict(
        modelo="14M", trabajo="Mantenimiento de caminos de acarreo", S=10.0,
        angulo=30, lo=0.6, E=80.0, at=8.0, LT=12.0, unidad="km", htd=8, np=3,
        material="Tierra firme", wr=14000.0, T=None, wb=6.5, ba=2.1, fw=5200.0),
    "Ejemplo 2 · Carretera": dict(
        modelo="16M", trabajo="Mantenimiento de carreteras", S=12.0,
        angulo=20, lo=0.5, E=75.0, at=9.0, LT=5.0, unidad="km", htd=10, np=4,
        material="Arena mojada", wr=17500.0, T=None, wb=7.0, ba=2.4, fw=6300.0),
}


def cargar_ejemplo(nombre):
    e, ss = EJEMPLOS[nombre], st.session_state
    for k in ("modelo", "trabajo", "angulo", "lo", "E", "at", "LT", "unidad",
              "htd", "np", "material", "wr", "T", "wb", "ba", "fw"):
        ss[f"mn_{k}"] = e[k]
    ss[f"mn_S_{e['trabajo']}"] = e["S"]
    ss["mn_paso"] = 1


def conservar():
    """Mantiene los datos de los pasos que no se están mostrando."""
    ss = st.session_state
    for k in list(ss.keys()):
        if k in CLAVES or k.startswith("mn_S_"):
            ss[k] = ss[k]


def ir(delta):
    st.session_state["mn_paso"] = max(1, min(5, st.session_state["mn_paso"] + delta))


# ------------------------------ CÁLCULOS EN VIVO ------------------------------
def calc1():
    ss = st.session_state
    modelo = ss.get("mn_modelo", "12M")
    trabajo = ss.get("mn_trabajo", list(VELOCIDADES)[0])
    vmax = float(VELOCIDADES[trabajo][1])
    S = dec(ss.get(f"mn_S_{trabajo}", vmax))
    angulo = ss.get("mn_angulo", 0)
    le = dec(LONGITUD_EFECTIVA[angulo][list(MODELOS_MOTO).index(modelo)])
    lo, ef = ss.get("mn_lo"), ss.get("mn_E")
    if lo is None or not ef:
        return None, "Ingresa el traslape Lo y la eficiencia E."
    if dec(lo) >= le:
        return None, f"Lo debe ser menor que Le ({le} m)."
    E = dec(ef) / 100
    ancho, A = calculos.productividad(S, le, lo, E)
    return dict(modelo=modelo, trabajo=trabajo, S=S, angulo=angulo, le=le,
                lo=dec(lo), E=E, ancho=ancho, A=A), None


def calc2(a1):
    ss = st.session_state
    at, lt, htd, npas = ss.get("mn_at"), ss.get("mn_LT"), ss.get("mn_htd"), ss.get("mn_np")
    if not a1:
        return None, "Completa primero el paso 1."
    if not (at and lt and htd and npas):
        return None, "Completa ancho, distancia, turno y pasadas."
    LT = dec(lt) * (1000 if ss.get("mn_unidad", "m") == "km" else 1)
    AT, NH, DT = calculos.tiempo_trabajo(at, LT, npas, a1["A"], htd)
    return dict(at=at, LT=LT, np=npas, htd=htd, AT=AT, NH=NH, DT=DT, A=a1["A"]), None


def calc3():
    ss = st.session_state
    material, wr = ss.get("mn_material", list(TRACCION)[0]), ss.get("mn_wr")
    T = ss.get("mn_T") if material == OTRO else TRACCION.get(material)
    if not wr or not T:
        return None, "Ingresa la masa Wr (y T si eliges otro material)."
    return dict(material=material, T=dec(T), wr=wr, TH=calculos.traccion(wr, T)), None


def calc4():
    ss = st.session_state
    wb, ba, fw = ss.get("mn_wb"), ss.get("mn_ba"), ss.get("mn_fw")
    if not (wb and fw) or ba is None:
        return None, "Completa WB, BA y FW."
    if ba >= wb:
        return None, "WB debe ser mayor que BA."
    dif, BD = calculos.fuerza_descendente(wb, ba, fw)
    return dict(wb=wb, ba=ba, fw=fw, dif=dif, BD=BD), None


def mostrar_resultado(res, error):
    if error:
        st.info(error)
        return False
    return True


# ------------------------------ PASOS ------------------------------
def paso1():
    izq, der = st.columns(2, gap="large")
    with izq:
        st.radio("Modelo de motoniveladora", list(MODELOS_MOTO), horizontal=True,
                 key="mn_modelo")
        trabajo = st.selectbox("Tipo de trabajo (pág. 146)", list(VELOCIDADES),
                               key="mn_trabajo")
        vmin, vmax = VELOCIDADES[trabajo]
        clave_s = f"mn_S_{trabajo}"
        st.session_state.setdefault(clave_s, float(vmax))
        st.slider("Velocidad S (km/h)", float(vmin), float(vmax), step=0.5, key=clave_s)
        st.select_slider("Ángulo de vertedera (pág. 148)", options=ANGULOS,
                         format_func=lambda x: f"{x}°", key="mn_angulo")
        c1, c2 = st.columns(2)
        c1.number_input("Traslape Lo (m)", min_value=0.0, value=None,
                        format="%.3f", key="mn_lo")
        c2.number_input("Eficiencia E (%)", min_value=0.0, max_value=100.0,
                        value=None, key="mn_E")
    with der:
        r, err = calc1()
        if mostrar_resultado(r, err):
            st.metric("Productividad A", f"{fmt(r['A'])} m²/h")
            with st.container(border=True):
                st.markdown("**Desarrollo**")
                st.write(f"{r['trabajo']} · Le = {r['le']} m a {r['angulo']}°")
                st.latex(r"A=S\cdot(Le-Lo)\cdot1000\cdot E")
                st.latex(rf"A={r['S']}\cdot({r['le']}-{r['lo']})\cdot1000\cdot{r['E']}")
                st.markdown(f"➜ **A = {fmt(r['A'])} m²/h**")


def paso2():
    a1, _ = calc1()
    izq, der = st.columns(2, gap="large")
    with izq:
        if a1:
            st.success(f"A del paso 1 = {fmt(a1['A'])} m²/h")
        else:
            st.warning("Primero completa el paso 1.")
        st.number_input("Ancho del terreno aT (m)", min_value=0.0, value=None, key="mn_at")
        c1, c2 = st.columns([2, 1])
        c1.number_input("Distancia a nivelar LT", min_value=0.0, value=None, key="mn_LT")
        c2.radio("Unidad", ["m", "km"], horizontal=True, key="mn_unidad")
        st.slider("Turno de trabajo (h/día)", 1, 24, key="mn_htd")
        st.number_input("Número de pasadas NP", min_value=1, value=None, step=1, key="mn_np")
    with der:
        r, err = calc2(a1)
        if mostrar_resultado(r, err):
            c1, c2, c3 = st.columns(3)
            c1.metric("Área", f"{fmt(r['AT'])} m²")
            c2.metric("Horas", fmt(r["NH"]))
            c3.metric("Días", r["DT"])
            with st.container(border=True):
                st.latex(rf"AT=aT\cdot LT\cdot NP={r['at']:g}\cdot{r['LT']}\cdot{r['np']}")
                st.latex(rf"NH=\frac{{AT}}{{A}}=\frac{{{fmt(r['AT'])}}}{{{fmt(r['A'])}}}")
                st.latex(rf"DT=\frac{{NH}}{{HTD}}=\frac{{{fmt(r['NH'])}}}{{{r['htd']}}}")
                st.markdown(f"➜ **{r['DT']} día(s)** (entero superior)")


def paso3():
    izq, der = st.columns(2, gap="large")
    with izq:
        material = st.selectbox("Material (pág. 1573)", list(TRACCION) + [OTRO],
                                key="mn_material")
        if material == OTRO:
            st.number_input("Factor de tracción T", min_value=0.0, value=None,
                            format="%.3f", key="mn_T")
        else:
            st.info(f"Factor de tracción T = {TRACCION[material]}")
        st.number_input("Masa sobre el eje trasero Wr (kg)", min_value=0.0,
                        value=None, key="mn_wr")
    with der:
        r, err = calc3()
        if mostrar_resultado(r, err):
            st.metric("Fuerza de tracción TH", f"{fmt(r['TH'])} kgf")
            with st.container(border=True):
                st.latex(r"TH=Wr\cdot T")
                st.latex(rf"TH={r['wr']:g}\cdot{r['T']}")
                st.markdown(f"➜ **TH = {fmt(r['TH'])} kgf**")


def paso4():
    izq, der = st.columns(2, gap="large")
    with izq:
        st.number_input("Distancia entre ejes WB (m)", min_value=0.0, value=None,
                        format="%.3f", key="mn_wb")
        st.number_input("Distancia hoja - eje delantero BA (m)", min_value=0.0,
                        value=None, format="%.3f", key="mn_ba")
        st.number_input("Peso sobre ruedas delanteras FW (kg)", min_value=0.0,
                        value=None, key="mn_fw")
    with der:
        r, err = calc4()
        if mostrar_resultado(r, err):
            st.metric("Fuerza descendente BD", f"{fmt(r['BD'])} kgf")
            with st.container(border=True):
                st.latex(r"BD=\frac{WB}{WB-BA}\cdot FW")
                st.latex(rf"BD=\frac{{{r['wb']:g}}}{{{r['dif']}}}\cdot{r['fw']:g}")
                st.markdown(f"➜ **BD = {fmt(r['BD'])} kgf**")


def paso5():
    a1, _ = calc1()
    a2, _ = calc2(a1)
    a3, _ = calc3()
    a4, _ = calc4()
    filas = []
    if a1: filas.append(("1", "A", "Productividad", fmt(a1["A"]), "m²/h"))
    if a2: filas += [("2", "AT", "Área total", fmt(a2["AT"]), "m²"),
                     ("2", "NH", "Horas", fmt(a2["NH"]), "h"),
                     ("2", "DT", "Días", str(a2["DT"]), "días")]
    if a3: filas.append(("3", "TH", "Fuerza de tracción", fmt(a3["TH"]), "kgf"))
    if a4: filas.append(("4", "BD", "Fuerza descendente", fmt(a4["BD"]), "kgf"))
    if not filas:
        st.info("Aún no hay resultados. Completa los pasos anteriores.")
        return
    st.markdown(
        f'<div class="respuesta"><small>RESUMEN</small><h2>{len(filas)} resultados calculados</h2>'
        f'<p>Revisa la tabla y descárgala si la necesitas.</p></div>',
        unsafe_allow_html=True)
    df = pd.DataFrame(filas, columns=["Paso", "Variable", "Descripción", "Resultado", "Unidad"])
    st.dataframe(df, hide_index=True)
    st.download_button("⬇️ Descargar CSV", df.to_csv(index=False).encode("utf-8-sig"),
                       "resumen_motoniveladora.csv", "text/csv")


# ------------------------------ PANTALLA ------------------------------
def mostrar():
    ss = st.session_state
    ss.setdefault("mn_paso", 1)
    ss.setdefault("mn_angulo", 0)
    ss.setdefault("mn_htd", 8)
    ss.setdefault("mn_unidad", "m")
    conservar()

    st.markdown("##### ¿Quieres probar con un ejercicio de ejemplo?")
    cols = st.columns(len(EJEMPLOS) + 1)
    for col, nombre in zip(cols, EJEMPLOS):
        col.button(nombre, on_click=cargar_ejemplo, args=(nombre,), key=f"mnbtn_{nombre}")

    paso = ss["mn_paso"]
    st.progress(paso / len(PASOS), text=f"PASO {paso} DE {len(PASOS)} · {PASOS[paso - 1].upper()}")
    {1: paso1, 2: paso2, 3: paso3, 4: paso4, 5: paso5}[paso]()

    st.write("")
    c1, c2, c3 = st.columns([1, 1, 4])
    c1.button("◀ Anterior", on_click=ir, args=(-1,), disabled=paso == 1, key="mn_prev")
    c2.button("Siguiente ▶", on_click=ir, args=(1,), disabled=paso == len(PASOS),
              type="primary", key="mn_next")
