import streamlit as st

# --- 1. CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Satcom Autómata v7.0", page_icon="🤖", layout="wide")

# --- 2. CEREBRO: TARIFAS 2025 & CATÁLOGOS ---
TARIFARIO = {
    "demanda": 200000, "bolsa_3h": 180000, "bolsa_5h": 172000,
    "bolsa_10h": 170000, "bolsa_20h": 140000, "reproceso": 6000,
    "hora_tecnica": 148200, "soporte_10h": 1700000, "soporte_20h": 2800000
}

CATALOGO_CAP = {
    "Recepción de Documentos": 4, "Cuadraturas POS-PMS": 4,
    "Manejo Docs No Autorizados": 4, "Operativa POS": 2, "Auditoría IT": 4
}

RANGOS_TRX = [
    (10000, 25.0, "Micro"), (25000, 18.0, "Pyme"),
    (50000, 10.0, "Corp"), (1000000, 8.5, "Enterprise")
]

# --- 3. FUNCIÓN EDUCATIVA (TARJETA) ---
def tarjeta(paso, pestana, accion, valor, explicacion, alerta=None):
    with st.expander(f"{paso} | Pestaña {pestana}", expanded=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**📍 {accion}**")
            st.code(valor, language="text")
            st.caption(f"💡 {explicacion}")
            if alerta: st.error(alerta)
        with col2: st.markdown("✅")

# --- 4. INTERFAZ INTELIGENTE ---
st.title("🤖 Satcom Autómata v7.0")
st.markdown("Cotizador Inteligente con asignación automática de descuentos según perfil.")

with st.sidebar:
    st.header("1. Perfil del Cliente")
    cliente = st.text_input("Nombre del Cliente:", placeholder="Ej: Hotel Estelar")
    
    # ---> CEREBRO DE DESCUENTOS (Aquí está la magia) <---
    clasificacion = st.selectbox("Clasificación (Según Excel):", [
        "Empresa Pequeña / Independiente",
        "Empresa Mediana",
        "Empresa Grande",
        "Major Account / Cadena (Grupo)",
        "Distribuidor / Partner"
    ])
    
    # Lógica de Auto-Asignación de Descuento Base
    dcto_sugerido = 0
    if "Pequeña" in clasificacion: dcto_sugerido = 0
    elif "Mediana" in clasificacion: dcto_sugerido = 5
    elif "Grande" in clasificacion: dcto_sugerido = 10
    elif "Major Account" in clasificacion: dcto_sugerido = 15 # Estándar Cadena
    elif "Distribuidor" in clasificacion: dcto_sugerido = 30  # Margen Canal
    
    st.info(f"🏷️ Política Detectada: Descuento Base {dcto_sugerido}%")
    
    # Slider que inicia en el sugerido pero permite ajuste manual
    descuento_pct = st.slider("Ajuste de Descuento Final (%):", 0, 50, dcto_sugerido)
    
    st.divider()
    
    # --- SELECTOR DE MODO ---
    modo = st.radio("¿Qué vas a cotizar?", ["A. Servicios Puntuales", "B. Proyecto Implementación"])
    
    # INPUTS DINÁMICOS
    if modo.startswith("A"):
        servicio = st.selectbox("Producto:", [
            "Paquete de Transacciones (Solo Datos)",
            "Bolsa de Horas (Consultoría)",
            "Paquete de Capacitación",
            "Contrato de Soporte",
            "Reproceso Documentos"
        ])
        
        cantidad = 0; lista_cap = []; volumen_trx = 0
        
        if "Transacciones" in servicio:
            volumen_trx = st.number_input("Volumen Anual:", 1000, 1000000, 24000)
        elif "Capacitación" in servicio:
            lista_cap = st.multiselect("Módulos:", list(CATALOGO_CAP.keys()))
            cantidad = sum([CATALOGO_CAP[k] for k in lista_cap])
            if cantidad > 0: st.caption(f"Total: {cantidad} Horas")
        elif "Reproceso" in servicio:
            cantidad = st.number_input("Nº Documentos:", 1, 10000, 100)
        elif "Contrato" in servicio:
            tipo_contrato = st.radio("Plan:", ["10h/Mes", "20h/Mes"])
            cantidad = 10 if "10" in tipo_contrato else 20
        else: # Bolsa
            cantidad = st.number_input("Horas:", 1, 100, 5)

    else: # Modo B
        es_modular = st.checkbox("🔀 Cotizar Modular (Tercerizado)", value=False)
        st.subheader("Infraestructura")
        pms = st.selectbox("PMS:", ["Ninguno", "Opera Cloud", "Opera V5", "Otro"])
        pos = st.selectbox("POS:", ["Ninguno", "Simphony Cloud", "Micros 3700"])
        tiendas = 1
        if pos != "Ninguno": tiendas = st.slider("Tiendas:", 1, 10, 1)
        trx = st.number_input("TRX Totales:", 0, 1000000, 12000)

# --- 5. MOTOR DE CÁLCULO ---
st.header("2. Guía de Ingeniería & Financiera")

valor_bruto = 0

# LÓGICA DE PRECIOS
if modo.startswith("A"):
    if "Transacciones" in servicio:
        p_unit = 25.0; r_nom = "Micro"
        for t, p, n in RANGOS_TRX:
            if volumen_trx <= t: p_unit = p; r_nom = n; break
        valor_bruto = volumen_trx * p_unit
        tarjeta("1️⃣", "DATOS", "Sección Transacciones", f"{volumen_trx:,} x ${p_unit}", f"Rango: {r_nom}")
        
    elif "Reproceso" in servicio:
        valor_bruto = cantidad * TARIFARIO["reproceso"]
        tarjeta("1️⃣", "COTIZ", "Fila Saneamiento", f"Cant: {cantidad} | Unit: ${TARIFARIO['reproceso']}", "Tarifa fija.")
        
    elif "Contrato" in servicio:
        valor_bruto = TARIFARIO["soporte_10h"] if cantidad == 10 else TARIFARIO["soporte_20h"]
        tarjeta("1️⃣", "COTIZ", f"Contrato {cantidad}h", f"${valor_bruto:,.0f} / mes", "Recurrente.")
        
    else: # Bolsa/Capacitación
        p_hora = TARIFARIO["demanda"]
        if 3 <= cantidad < 5: p_hora = TARIFARIO["bolsa_3h"]
        elif 5 <= cantidad < 10: p_hora = TARIFARIO["bolsa_5h"]
        elif 10 <= cantidad < 20: p_hora = TARIFARIO["bolsa_10h"]
        elif cantidad >= 20: p_hora = TARIFARIO["bolsa_20h"]
        valor_bruto = cantidad * p_hora
        tarjeta("1️⃣", "COTIZ", f"Servicios ({servicio})", f"{cantidad}h x ${p_hora:,.0f}", "Tarifa escalonada 2025.")

else: # MODO PROYECTO
    h_total = 0
    items = []
    # PMS
    if pms == "Opera Cloud": h_total += 8; items.append("Middleware + SIAT Cloud (8h)")
    elif pms == "Opera V5": h_total += 32; items.append("Conector Opera V5 (32h)")
    # POS
    if pos == "Simphony Cloud": 
        h = 24 + (8*(tiendas-1)); h_total += h
        items.append(f"Simphony ({tiendas} tiendas) ({h}h)")
    elif pos == "Micros 3700": 
        h_total += 32; items.append("Micros Legacy + Pruebas (32h)")
        st.warning("⚠️ Alerta: Micros 3700 requiere Soporte Post-Venta obligatorio.")

    valor_bruto = h_total * TARIFARIO["hora_tecnica"]
    
    # Desglose en Pantalla
    st.markdown("#### 🛠️ Ingeniería Requerida")
    for i in items: st.write(f"- [x] {i}")
    tarjeta("1️⃣", "TIEMPOS", "Cargar Horas Técnicas", f"Total: {h_total} Horas", "Suma de componentes detectados.")
    
    if es_modular: st.info("ℹ️ Recuerda separar las filas en el Excel si es cotización modular.")

# --- RESUMEN FINANCIERO (CON DESCUENTO AUTOMÁTICO) ---
monto_descuento = valor_bruto * (descuento_pct / 100)
valor_neto = valor_bruto - monto_descuento

st.divider()
st.markdown("### 💰 Cierre Financiero")

col1, col2, col3 = st.columns(3)
col1.metric("Valor Lista", f"${valor_bruto:,.0f}")
col2.metric("Descuento", f"-${monto_descuento:,.0f}", delta=f"-{descuento_pct}% ({clasificacion})", delta_color="inverse")
col3.metric("Valor Final", f"${valor_neto:,.0f}")

if descuento_pct > 0:
    tarjeta("💎", "COTIZ", "Fila 'Descuento Comercial'", f"{descuento_pct}%", 
            f"Aplicado por política de: {clasificacion}")
else:
    st.success("✅ Se vende a Tarifa Plena (Sin descuento).")
