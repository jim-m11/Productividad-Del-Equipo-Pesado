"""Historial de cálculos de la sesión (se muestra en el menú lateral)."""
import streamlit as st


def agregar(texto):
    historial = st.session_state.setdefault("historial", [])
    historial.insert(0, texto)
    del historial[8:]          # solo se guardan los últimos 8


def obtener():
    return st.session_state.get("historial", [])


def borrar():
    st.session_state["historial"] = []
