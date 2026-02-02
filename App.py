import streamlit as st

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Satcom Instructor 2025", page_icon="👨‍🏫", layout="centered")

# --- CEREBRO: TARIFAS OFICIALES 2025 (COLOMBIA) ---
TARIFARIO = {
    "demanda": 200000,      # < 3 horas
    "bolsa_3h": 180000,     # 3-4 horas
    "bolsa_5h": 172000,     # 5-9 horas
    "bolsa_10h": 170000,    # 10-19 horas
    "bolsa_20h": 140000,    # >= 20 horas
    "reproceso": 6000,      # Por documento
    "hora_tecnica": 148200  # Base Implementación
}

# --- CEREBRO: RANGOS TRX (Curva Logarítmica) ---
# Formato: (Techo de Transacciones, Precio Unitario, Nombre del Rango)
RANGOS_TRX = [
    (10000, 25.0, "Rango Micro (Start)"),
    (25000, 18.0, "Rango Pyme (Growth)"),
    (50000, 10.0, "Rango Corp (Scale)"),
    (1000000, 8.5, "Rango Enterprise (Volume)")
]

# --- ENCABEZADO ---
st.title("👨‍🏫 Satcom Instructor")
st.markdown("### Guía interactiva para el llenado del Excel Comercial")
st.info("💡 **Objetivo:** Te indicaré exactamente qué celdas modificar en el archivo 'mySatcom.xlsx' y el criterio técnico detrás.")

# --- BARRA LATERAL: RELEVAMIENTO DE DATOS ---
with st.sidebar:
    st.header("1. Datos del Caso")
    modo = st.radio("¿Qué estamos cotizando?", ["A. Servicios Puntuales (Bolsas/Soporte)", "B. Proyecto de Implementación"])
    
    st.divider()
    
    if modo.startswith("A"):
        servicio = st.selectbox("Producto:", [
            "Bolsa de Horas (Consultoría)",
            "Contrato de Soporte (Recurrente)",
            "Reproceso Documentos"
        ])
        if "Reproceso" in servicio:
            cantidad = st.number_input("Cantidad de Documentos:", 1, 10000, 100)
        else:
            cantidad = st.number_input("Horas Estimadas (Ingeniería):", 1, 100, 5)
            
    else: # Modo Proyecto
        cliente = st.text_input("Nombre del Cliente:")
        pms = st.selectbox("Sistema PMS (Hotel):", ["Opera Cloud", "Opera V5", "Otro"])
        pos = st.selectbox("Sistema POS (Restaurante):", ["Simphony", "Micros 3700", "Ninguno"])
        
        tiendas = 1
        if pos != "Ninguno":
            tiendas = st.slider("Nº Puntos de Venta / Tiendas:", 1, 10, 1)
            
        trx = st.number_input("Volumen TRX Anuales (Estimado):", 0, 1000000, 12000)

# --- PANEL CENTRAL: EL INSTRUCTOR ---
st.header("2. Instrucciones de Llenado")
st.caption("Abre tu archivo Excel y sigue estos pasos:")

# Función para generar las tarjetas de instrucción
def tarjeta_instruccion(paso, pestana, celda, valor, explicacion, alerta=None):
    # Usamos un expander para organizar visualmente cada paso
    with st.expander(f"{paso} | Ir a Pestaña: {pestana}", expanded=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**📍 Ubicación (Celda/Fila):** {celda}")
            st.markdown(f"**✍️ Valor a Ingresar:** `{valor}`")
            st.markdown(f"🧠 **Criterio Técnico:** {explicacion}")
            if alerta:
                st.warning(f"⚠️ {alerta}")
        with col2:
            st.markdown("# ✅")

# ==========================================
# LÓGICA MODO A: SERVICIOS PUNTUALES
# ==========================================
if modo.startswith("A"):
    precio_u = 0
    total = 0
    razon_precio = ""
    
    # 1. CÁLCULO TARIFARIO AUTOMÁTICO
    if "Reproceso" in servicio:
        precio_u = TARIFARIO["reproceso"]
        razon_precio = "Tarifa fija Saneamiento (Data Entry)"
        total = cantidad * precio_u
    else:
        # Algoritmo de escalado de precios
        if cantidad < 3:
            precio_u = TARIFARIO["demanda"]
            razon_precio = "Tarifa Plena (Demanda < 3h)"
        elif 3 <= cantidad < 5:
            precio_u = TARIFARIO["bolsa_3h"]
            razon_precio = "Tarifa Bolsa 3h"
        elif 5 <= cantidad < 10:
            precio_u = TARIFARIO["bolsa_5h"]
            razon_precio = "Tarifa Bolsa 5h"
        elif 10 <= cantidad < 20:
            precio_u = TARIFARIO["bolsa_10h"]
            razon_precio = "Tarifa Bolsa 10h"
        else:
            precio_u = TARIFARIO["bolsa_20h"]
            razon_precio = "Tarifa Mayorista (>20h)"
        total = cantidad * precio_u

    # 2. GENERACIÓN DE TARJETAS
    tarjeta_instruccion(
        paso="Paso 1",
        pestana="COTIZACIÓN",
        celda=f"Sección '{servicio}' > Columna Cantidad",
        valor=cantidad,
        explicacion="Ingresa la cantidad exacta solicitada por el cliente o estimada por ingeniería."
    )
    
    tarjeta_instruccion(
        paso="Paso 2",
        pestana="COTIZACIÓN",
        celda="Columna 'Valor Unitario'",
        valor=f"${precio_u:,.0f}",
        explicacion=f"El sistema seleccionó automáticamente: **{razon_precio}**.",
        alerta="Si modificas la cantidad de horas en el Excel, recuerda actualizar manualmente este precio unitario."
    )
    
    st.metric(label="Total Esperado de la Cotización", value=f"${total:,.0f} COP")

# ==========================================
# LÓGICA MODO B: PROYECTO
# ==========================================
else:
    st.subheader(f"Configuración para: {cliente}")
    
    # 1. LÓGICA PMS (Gestión Hotelera)
    if pms == "Opera Cloud":
        tarjeta_instruccion("Paso PMS", "TIEMPOS / RECURSOS", "Fila 'Middleware Config'", "1 Unidad", 
            "Opera Cloud es SaaS. Requiere configuración obligatoria de túneles VPN/OIG.")
        tarjeta_instruccion("Paso PMS", "TIEMPOS / RECURSOS", "Fila 'Honorarios SIAT Cloud'", "1 Unidad", 
            "La integración fiscal (SIAT) en nube tiene una complejidad distinta a la local.")
    elif pms == "Opera V5":
        tarjeta_instruccion("Paso PMS", "TIEMPOS / RECURSOS", "Fila 'Instalación Conector Opera'", "1 Unidad", 
            "Instalación On-Premise. Equivale a ~32 horas estándar de ingeniería.")

    # 2. LÓGICA POS (Puntos de Venta)
    if pos == "Simphony":
        tarjeta_instruccion("Paso POS", "TIEMPOS / RECURSOS", "Fila 'Instalación Simphony Base'", "1 Unidad", 
            "Cubre la configuración del servidor de aplicaciones y la primera tienda (24h).")
        if tiendas > 1:
            tarjeta_instruccion("Paso POS", "TIEMPOS / RECURSOS", "Fila 'Tiendas Adicionales'", str(tiendas-1), 
                f"Configuración de {tiendas-1} tiendas extra. Se cobra como réplica (menor esfuerzo).")
    elif pos == "Micros 3700":
        tarjeta_instruccion("Paso POS", "TIEMPOS / RECURSOS", "Fila 'Reinstalación Micros Legacy'", "1 Unidad", 
            "Sistema Legacy (Antiguo). Se cobra como intervención crítica.", 
            alerta="Recomendación: Agregar una Bolsa de Soporte de 10h por posible inestabilidad del sistema antiguo.")

    # 3. LÓGICA TRX (Transacciones)
    precio_trx_final = 25.0
    nombre_rango = "Micro"
    
    # Buscamos en qué rango cae el volumen
    for techo, precio, nombre in RANGOS_TRX:
        if trx <= techo:
            precio_trx_final = precio
            nombre_rango = nombre
            break
            
    tarjeta_instruccion("Paso TRX", "DATOS FINANCIEROS", f"Fila 'Costo por TRX' (Rango {nombre_rango})", f"${precio_trx_final}", 
        f"Para un volumen de {trx} docs/año aplica el precio de {nombre_rango}. Economía de escala.")

    st.success("✅ **VALIDACIÓN:** Si seguiste los pasos, verifica que el margen del proyecto en el Excel sea positivo.")
