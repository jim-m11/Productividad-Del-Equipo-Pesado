"""Estilos: amarillo, negro y gris."""
import streamlit as st

CSS = """
<style>
.stApp {background:#0B0B0B;}
.block-container {max-width: 1250px; padding-top: 0.5rem;}
header[data-testid="stHeader"] {background: transparent;}

/* Franja de advertencia superior */
.franja {height: 14px; margin: 0 -4rem 14px -4rem;
  background: repeating-linear-gradient(45deg,#FFC400 0 18px,#0B0B0B 18px 36px);}
.cabecera {background:#FFC400; color:#0B0B0B; padding:18px 26px;
  border-radius:4px; margin-bottom:22px;}
.cabecera h1 {color:#0B0B0B !important; margin:0; font-size:1.9rem;
  letter-spacing:2px; font-weight:900;}
.cabecera p {margin:2px 0 0 0; color:#2B2B2B; font-weight:600;}

/* Tarjeta de resultado */
.resultado {background:#1C1C1C; border:2px solid #FFC400; border-radius:6px;
  padding:22px; text-align:center; margin-bottom:14px;}
.resultado small {color:#FFC400; letter-spacing:3px; font-weight:700;}
.resultado h2 {color:#FFFFFF; font-size:2.6rem; margin:6px 0; font-weight:900;}
.resultado p {color:#B5B5B5; margin:0; font-size:1.05rem;}
.vacio {background:#1C1C1C; border:2px dashed #4A4A4A; border-radius:6px;
  padding:50px 20px; text-align:center; color:#8A8A8A;}

/* Métricas */
div[data-testid="stMetric"] {background:#1C1C1C; border:1px solid #333;
  border-bottom:4px solid #FFC400; border-radius:4px; padding:12px 16px;}
div[data-testid="stMetricLabel"] p {color:#9A9A9A !important;}
div[data-testid="stMetricValue"] {color:#FFFFFF;}

/* Botones */
button[kind^="primary"], [data-testid^="stBaseButton-primary"] {
  background:#FFC400 !important; color:#0B0B0B !important;
  border:none !important; font-weight:800 !important; border-radius:4px !important;}
[data-testid^="stBaseButton-primary"] p {color:#0B0B0B !important; font-weight:800;}
button[kind^="primary"]:hover, [data-testid^="stBaseButton-primary"]:hover {
  background:#E6B000 !important;}

/* Expanders y menú lateral */
div[data-testid="stExpander"] {background:#161616; border:1px solid #333;
  border-radius:4px;}
section[data-testid="stSidebar"] {background:#141414; border-right:3px solid #FFC400;}
.marca {color:#FFC400; font-weight:900; font-size:1.4rem; letter-spacing:2px;}
.marca-sub {color:#8A8A8A; font-size:0.8rem; margin-bottom:10px;}
h2, h3, h4 {color:#FFFFFF !important;}

/* v3: bloques de la hoja de resolución */
div[data-testid="stVerticalBlockBorderWrapper"] {border-color:#3A3A3A !important;
  border-left:5px solid #FFC400 !important; border-radius:4px !important;}
button[data-baseweb="tab"] {font-weight:800; letter-spacing:1px;}
.respuesta {background:#FFC400; color:#0B0B0B; border-radius:6px; padding:22px;
  margin:14px 0;}
.respuesta small {letter-spacing:3px; font-weight:800;}
.respuesta h2 {color:#0B0B0B !important; margin:4px 0; font-weight:900;}
.respuesta p {margin:0; font-weight:600; color:#2B2B2B;}
</style>
"""


def aplicar():
    st.markdown(CSS, unsafe_allow_html=True)


def cabecera(titulo, subtitulo):
    st.markdown(
        f'<div class="franja"></div>'
        f'<div class="cabecera"><h1>{titulo}</h1><p>{subtitulo}</p></div>',
        unsafe_allow_html=True)
