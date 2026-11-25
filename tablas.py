"""Datos del Manual de Rendimiento Caterpillar (edición 42)."""

# ---------------- CARGADOR FRONTAL ----------------
# Tiempo de ciclo base (min) - pág. 998 del PDF
TIEMPOS_CICLO = {
    "966H": 0.50, "972H": 0.50, "980H": 0.50, "988H": 0.55,
    "990H": 0.55, "992K": 0.60, "993K": 0.60, "994F": 0.60,
}
MODELOS_CARGADOR = list(TIEMPOS_CICLO.keys())

# Factores de corrección del tiempo de ciclo (min) - pág. 998
FACTORES = {
    "Máquina": {"Manipulador de materiales": -0.05},
    "Materiales": {
        "Materiales mezclados": 0.02, "Hasta 3 mm": 0.02,
        "De 3 a 20 mm": -0.02, "De 20 a 150 mm": 0.00,
        "Más de 150 mm": 0.03, "Banco o fracturado": 0.04,
    },
    "Pila": {
        "Apilado a más de 3 m": 0.00, "Apilado a menos de 3 m": 0.01,
        "Descargado por camión": 0.02,
    },
    "Varios": {
        "Mismo propietario de camiones y cargadores": -0.04,
        "Propietario independiente de camiones": 0.04,
        "Operación constante": -0.04, "Operación intermitente": 0.04,
        "Punto de carga pequeño": 0.04, "Punto de carga frágil": 0.05,
    },
}
# Lista plana: "Categoría · Nombre" -> valor
FACTORES_PLANOS = {
    f"{cat} · {nombre}": valor
    for cat, opciones in FACTORES.items()
    for nombre, valor in opciones.items()
}

# Capacidades colmadas de cucharones (m³) - págs. 938 a 961
CAPACIDADES = {
    "966H": [3.5, 6.4],
    "972H": [1.8, 3.8, 4.0, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.1, 6.4],
    "980H": [4.2, 4.3, 4.5, 4.6, 4.7, 4.9, 5.0, 5.3, 5.4, 5.6, 5.7, 6.0,
             6.1, 8.2, 10.5],
    "988H": [6.4, 6.9, 7.6, 7.7],
    "990H": [8.4, 8.6, 9.2],
    "992K": [10.7, 11.5, 12.3],
    "993K": [12.0, 12.8, 13.8, 14.5],
    "994F": [14.0, 15.0, 17.0, 19.0],
}
# Valores con inconsistencia en el manual (pendientes de verificar)
EXCLUIDAS = {"972H": [1.8]}

# Densidad suelta, densidad en banco (t/m³), factor de carga - pág. 1575
MATERIALES = {
    "Basalto": (1.960, 2.970, 0.67),
    "Bauxita, caolín": (1.420, 1.900, 0.75),
    "Caliche": (1.250, 2.260, 0.55),
    "Carnotita": (1.630, 2.200, 0.74),
    "Ceniza": (0.560, 0.860, 0.66),
    "Arcilla en su lecho natural": (1.660, 2.020, 0.82),
    "Arcilla seca": (1.480, 1.840, 0.81),
    "Arcilla mojada": (1.660, 2.080, 0.80),
    "Arcilla y grava secas": (1.420, 1.660, 0.85),
    "Arcilla y grava mojadas": (1.540, 1.840, 0.85),
    "Carbón antracita en bruto": (1.190, 1.600, 0.74),
    "Carbón bituminoso en bruto": (0.950, 1.280, 0.74),
    "75% roca y 25% tierra": (1.960, 2.790, 0.70),
    "50% roca y 50% tierra": (1.720, 2.280, 0.75),
    "25% roca y 75% tierra": (1.570, 1.960, 0.80),
    "Tierra apisonada y seca": (1.510, 1.900, 0.80),
    "Tierra excavada y mojada": (1.600, 2.020, 0.79),
    "Tierra limo": (1.250, 1.540, 0.81),
    "Granito fragmentado": (1.660, 2.730, 0.61),
    "Grava de cantera": (1.930, 2.170, 0.89),
    "Grava seca": (1.510, 1.690, 0.89),
    "Grava seca de 6 a 50 mm": (1.690, 1.900, 0.89),
    "Grava mojada de 6 a 50 mm": (2.020, 2.260, 0.89),
    "Yeso fragmentado": (1.810, 3.170, 0.57),
    "Yeso triturado": (1.600, 2.790, 0.57),
    "Piedra caliza fragmentada": (1.540, 2.610, 0.59),
    "Magnetita": (2.790, 3.260, 0.85),
    "Pirita": (2.580, 3.030, 0.85),
    "Arena seca y suelta": (1.420, 1.600, 0.89),
    "Arena húmeda": (1.690, 1.900, 0.89),
    "Arena mojada": (1.840, 2.080, 0.89),
    "Arena y arcilla suelta": (1.600, 2.020, 0.79),
    "Arena y grava seca": (1.720, 1.930, 0.89),
    "Arena y grava mojada": (2.020, 2.230, 0.91),
    "Arenisca": (1.510, 2.520, 0.60),
    "Pizarra bituminosa": (1.250, 1.660, 0.75),
    "Escorias fragmentadas": (1.750, 2.940, 0.60),
    "Piedra triturada": (1.600, 2.670, 0.60),
    "Tierra vegetal": (0.950, 1.370, 0.70),
    "Roca fragmentada": (1.750, 2.610, 0.67),
}

# ---------------- MOTONIVELADORA ----------------
# Longitud de vertedera (m) - pág. 148
MODELOS_MOTO = {"12M": 3.66, "14M": 4.27, "16M": 4.88, "24M": 7.32}

# Velocidades (km/h) - pág. 146
VELOCIDADES = {
    "Nivelación de acabado": (0, 4),
    "Trabajo pesado con la hoja": (0, 9),
    "Reparación de zanjas": (0, 5),
    "Desgarramiento": (0, 5),
    "Mantenimiento de carreteras": (5, 16),
    "Mantenimiento de caminos de acarreo": (5, 16),
    "Movimiento de nieve": (7, 21),
    "Limpieza de nieve": (15, 28),
}

# Longitud efectiva (m) por ángulo; orden: 12M, 14M, 16M, 24M - pág. 148
LONGITUD_EFECTIVA = {
    0: [3.66, 4.27, 4.88, 7.32], 5: [3.64, 4.25, 4.86, 7.29],
    10: [3.60, 4.20, 4.80, 7.21], 15: [3.53, 4.12, 4.71, 7.07],
    20: [3.44, 4.01, 4.58, 6.87], 25: [3.32, 3.87, 4.42, 6.63],
    30: [3.17, 3.69, 4.22, 6.33], 35: [3.00, 3.50, 4.00, 5.99],
    40: [2.80, 3.27, 3.74, 5.61], 45: [2.59, 3.02, 3.45, 5.17],
}

# Factor de tracción de neumáticos - pág. 1573
TRACCION = {
    "Hormigón": 0.90, "Marga arcillosa seca": 0.55,
    "Marga arcillosa mojada": 0.45, "Marga arcillosa con surcos": 0.40,
    "Arena seca": 0.20, "Arena mojada": 0.40, "Canteras": 0.65,
    "Camino de grava (suelta, no dura)": 0.36, "Nieve compacta": 0.20,
    "Hielo": 0.12, "Tierra firme": 0.55, "Tierra suelta": 0.45,
    "Carbón amontonado": 0.45,
}
