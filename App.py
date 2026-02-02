import streamlit as st

# --- 1. CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Satcom Negociador v6.2", page_icon="💼", layout="wide")

# --- 2. CEREBRO: TARIFAS OFICIALES 2025 (COLOMBIA) ---
TARIFARIO = {
    "demanda": 200000,      # < 3 horas
    "bolsa_3h": 180000,     # 3-4 horas
    "bolsa_5h": 172000,     # 5-9 horas
    "bolsa_10h": 170000,    # 10-19 horas
    "bolsa_20h": 140000,    # >= 20 horas
    "reproceso": 6000,      # Por documento
    "hora_tecnica": 148200, # Base Implementación
    "soporte_10h": 1700000, # Contrato Base Mensual
    "soporte_20h": 2800000  # Contrato Pro Mensual
}

# --- 3. CATÁLOGOS ---
CATALOGO_CAP = {
    "Recepción de Documentos (Proveedores)": 4,
    "Cuadraturas POS-PMS vs DIAN": 4,
    "Manejo de Documentos No Autorizados": 4,
    "Operativa Básica POS (Cajeros)": 2,
    "Administración y Auditoría (IT)": 4
}

# Curva Logarítmica de Transacciones (Base de Datos)
RANGOS_TRX = [
    (10000, 25.0, "Rango Micro (Start)"),
    (25000, 18.0, "Rango Pyme (Growth)"),
    (50000, 10.0, "Rango Corp (Scale)"),
    (1000000, 8.5, "Rango Enterprise (Volume)")
]

# --- 4. FUNCIÓN VISUAL (TARJETA) ---
def tarjeta(paso, pestana, accion, valor, explicacion, alerta=None):
    with st.expander(f"{paso} | Pestaña {pestana}", expanded=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**📍 Acción:** {accion}")
            st.markdown(f"**✍️ Valor:** `{valor}`")
            st.caption(f"💡 **Criterio:** {explicacion}")
            if alerta: st.error(alerta)
        with col2:
            st.markdown("✅")

# --- 5. INTERFAZ PRINCIPAL ---
st.title("💼 Satcom Instructor v6.2")
st.markdown("**Novedad:** Control manual de descuentos y Paquetes de Transacciones independientes.")

with st.sidebar:
    st.header("1. Configuración")
    
    # ---> AQUÍ ESTÁ EL PODER DE ELEGIR EL DESCUENTO <---
    st.subheader("💰 Estrategia Comercial")
    descuento_pct = st.slider("Descuento a Aplicar (%)", min_value=0, max_value=50, value=0, step=1, 
                              help="Ajusta según negociación. Major Accounts suelen tener 15-20%. Transacciones masivas hasta 40%.")
    
    st.divider()
    
    modo = st.radio("¿Qué vas a cotizar?", [
        "A. Servicios / Paquetes Independientes", 
        "B. Proyecto Completo (Implementación)"
    ])
    
    # --- INPUTS MODO A ---
    if modo.startswith("A"):
        servicio = st.selectbox("Seleccione Producto:", [
            "Paquete de Transacciones (Solo Datos)", # <--- NUEVO
            "Bolsa de Horas (Consultoría)",
            "Paquete de Capacitación",
            "Contrato de Soporte (Recurrente)",
            "Reproceso Documentos (Saneamiento)"
        ])
        
        cantidad = 0
        lista_cap = []
        volumen_trx = 0
        
        if servicio == "Paquete de Transacciones (Solo Datos)":
            volumen_trx = st.number_input("Volumen Anual de Documentos:", 1000, 1000000, 24000)
            
        elif servicio == "Paquete de Capacitación":
            lista_cap = st.multiselect("Temas:", list(CATALOGO_CAP.keys()))
            cantidad = sum([CATALOGO_CAP[k] for k in lista_cap])
            if cantidad > 0: st.info(f"Total Horas: {cantidad}")
            
        elif "Reproceso" in servicio:
            cantidad = st.number_input("Nº Documentos con Error:", 1, 10000, 100)
        
        elif "Contrato" in servicio:
            tipo_contrato = st.radio("Nivel:", ["10 Horas/Mes", "20 Horas/Mes"])
            cantidad = 10 if "10" in tipo_contrato else 20
            
        else: # Bolsa
            cantidad = st.number_input("Horas (Según Consultor):", 1, 100, 5)

    # --- INPUTS MODO B ---
    else: 
        cliente = st.text_input("Cliente:", placeholder="Ej: Hotel Dann")
        es_modular = st.checkbox("🔀 Cotizar Modular (Separar PMS de POS)", value=False)
        
        st.subheader("Infraestructura")
        pms = st.selectbox("PMS:", ["Ninguno", "Opera Cloud", "Opera V5", "Otro"])
        pos = st.selectbox("POS:", ["Ninguno", "Simphony Cloud", "Micros 3700"])
        tiendas = 1
        if pos != "Ninguno": tiendas = st.slider("Nº Tiendas:", 1, 10, 1)
        
        st.subheader("Datos")
        trx = st.number_input("TRX Anuales Totales:", 0, 1000000, 12000)

# --- 6. MOTOR DE CÁLCULO ---
st.header("2. Resumen Financiero & Guía")

valor_bruto = 0
items_detalle = [] # Para guardar qué estamos cobrando

# ==========================================
# CÁLCULOS MODO A
# ==========================================
if modo.startswith("A"):
    if servicio == "Paquete de Transacciones (Solo Datos)":
        # Lógica Logarítmica para TRX
        p_unit = 25.0
        r_nom = "Micro"
        for t, p, n in RANGOS_TRX:
            if volumen_trx <= t: p_unit = p; r_nom = n; break
        
        valor_bruto = volumen_trx * p_unit
        tarjeta("1️⃣", "DATOS", "Sección Transacciones", f"Volumen: {volumen_trx} | Unitario: ${p_unit}", 
                f"Rango detectado: {r_nom}")
        
    elif "Reproceso" in servicio:
        valor_bruto = cantidad * TARIFARIO["reproceso"]
        tarjeta("1️⃣", "COTIZ", "Fila Saneamiento", f"Cant: {cantidad} | Unit: ${TARIFARIO['reproceso']}", "Tarifa fija por doc.")
        
    elif "Contrato" in servicio:
        valor_bruto = TARIFARIO["soporte_10h"] if cantidad == 10 else TARIFARIO["soporte_20h"]
        tarjeta("1️⃣", "COTIZ", f"Contrato {cantidad}h", f"Mensual: ${valor_bruto:,.0f}", "Mantenimiento recurrente.")
        
    else: # Bolsa y Capacitación
        # Lógica de precio por hora escalonado
        p_hora = TARIFARIO["demanda"]
        if 3 <= cantidad < 5: p_hora = TARIFARIO["bolsa_3h"]
        elif 5 <= cantidad < 10: p_hora = TARIFARIO["bolsa_5h"]
        elif 10 <= cantidad < 20: p_hora = TARIFARIO["bolsa_10h"]
        elif cantidad >= 20: p_hora = TARIFARIO["bolsa_20h"]
        
        valor_bruto = cantidad * p_hora
        tarjeta("1️⃣", "COTIZ", f"Servicios Profesionales ({servicio})", 
                f"Cant: {cantidad}h | Unit: ${p_hora:,.0f}", 
                "Tarifa escalonada por volumen de horas.")

# ==========================================
# CÁLCULOS MODO B
# ==========================================
else:
    # (Lógica simplificada para el ejemplo)
    h_total = 0
    if pms == "Opera Cloud": h_total += 8
    elif pms == "Opera V5": h_total += 32
    if pos == "Simphony Cloud": h_total += 24 + (8*(tiendas-1))
    elif pos == "Micros 3700": h_total += 32
    
    valor_servicios = h_total * TARIFARIO["hora_tecnica"]
    
    # Precio TRX
    p_trx = 25.0
    for t, p, n in RANGOS_TRX:
        if trx <= t: p_trx = p; break
    valor_trx_anual = trx * p_trx
    
    valor_bruto = valor_servicios # Nos enfocamos en el One-Time fee para el descuento
    
    st.info(f"Ingeniería: {h_total} Horas | Transacciones: ${p_trx}/doc")
    tarjeta("1️⃣", "TIEMPOS", "Llenar items técnicos", f"Total Horas: {h_total}", "Ver detalle en lógica anterior.")

# ==========================================
# APLICACIÓN DEL DESCUENTO (EL FINAL)
# ==========================================
monto_descuento = valor_bruto * (descuento_pct / 100)
valor_neto = valor_bruto - monto_descuento

st.divider()
st.markdown("### 📊 Resultado de la Negociación")

col_a, col_b, col_c = st.columns(3)
col_a.metric("Valor de Lista (Bruto)", f"${valor_bruto:,.0f} COP")
col_b.metric("Descuento Aplicado", f"-${monto_descuento:,.0f} COP", delta=f"-{descuento_pct}%", delta_color="inverse")
col_c.metric("Valor Final a Cotizar", f"${valor_neto:,.0f} COP")

if descuento_pct > 0:
    tarjeta("💎", "COTIZ", "Columna 'Descuento' o Fila 'Dcto Comercial'", 
            f"{descuento_pct}% o valor ${monto_descuento:,.0f}", 
            "Ajuste estratégico seleccionado manualmente.")
else:
    st.caption("No se aplicaron descuentos. Se vende a Tarifa Plena.")
