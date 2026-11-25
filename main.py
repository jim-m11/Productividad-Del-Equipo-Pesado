"""Ejecutar con:  streamlit run main.py"""
import streamlit as st

import estado
import tema
import vista_cargador
import vista_moto

st.set_page_config(page_title="Productividad | Equipo pesado", page_icon="🟨",
                   layout="wide")
tema.aplicar()
tema.cabecera("PRODUCTIVIDAD DE EQUIPO PESADO",
              "Resolución paso a paso · Manual Caterpillar, edición 42")

with st.sidebar:
    st.markdown('<div class="marca">▰ CÓMO USAR</div>', unsafe_allow_html=True)
    st.markdown("1. Elige el equipo en las pestañas.\n"
                "2. Llena los datos (o carga un **ejemplo**).\n"
                "3. Cargador: presiona **RESOLVER**.\n"
                "4. Motoniveladora: avanza con **Siguiente**.")
    st.divider()
    st.markdown("**Cargadores resueltos**")
    if estado.obtener():
        for linea in estado.obtener():
            st.caption("▸ " + linea)
        st.button("Borrar historial", on_click=estado.borrar)
    else:
        st.caption("Aún no hay ejercicios resueltos.")
    st.divider()
    st.caption("Proyecto académico · Gestión y Mantenimiento de Maquinaria Pesada")

tab_cargador, tab_moto = st.tabs(["🚜 CARGADOR FRONTAL", "⚙️ MOTONIVELADORA"])
with tab_cargador:
    vista_cargador.mostrar()
with tab_moto:
    vista_moto.mostrar()
