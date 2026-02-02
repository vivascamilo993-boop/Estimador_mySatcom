import streamlit as st

# --- 1. CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Satcom Instructor v6.0", page_icon="🏢", layout="wide")

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

RANGOS_TRX = [
    (10000, 25.0, "Rango Micro (Start)"),
    (25000, 18.0, "Rango Pyme (Growth)"),
    (50000, 10.0, "Rango Corp (Scale)"),
    (1000000, 8.5, "Rango Enterprise (Volume)")
]

# --- 4. FUNCIÓN EDUCATIVA (LA TARJETA) ---
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
st.title("🏢 Satcom Instructor v6.0")
st.markdown("Herramienta unificada de Cotización, Ingeniería y Aprendizaje.")

with st.sidebar:
    st.header("1. Escenario")
    modo = st.radio("¿Qué vas a cotizar?", [
        "A. Servicios Puntuales (Bolsas/Capacitación)", 
        "B. Proyecto de Implementación (Software)"
    ])
    
    st.divider()
    
    # --- INPUTS MODO A (SERVICIOS) ---
    if modo.startswith("A"):
        servicio = st.selectbox("Tipo de Servicio:", [
            "Bolsa de Horas (Consultoría)",
            "Paquete de Capacitación",
            "Contrato de Soporte (Recurrente)",
            "Reproceso Documentos (Saneamiento)"
        ])
        
        cantidad = 0
        lista_cap = []
        
        if servicio == "Paquete de Capacitación":
            lista_cap = st.multiselect("Temas:", list(CATALOGO_CAP.keys()))
            cantidad = sum([CATALOGO_CAP[k] for k in lista_cap])
            if cantidad > 0: st.info(f"Total Horas Académicas: {cantidad}")
            
        elif "Reproceso" in servicio:
            cantidad = st.number_input("Nº Documentos con Error:", 1, 10000, 100)
        
        elif "Contrato" in servicio:
            tipo_contrato = st.radio("Nivel:", ["10 Horas/Mes", "20 Horas/Mes"])
            cantidad = 10 if "10" in tipo_contrato else 20
            
        else: # Bolsa
            cantidad = st.number_input("Horas (Según Consultor):", 1, 100, 5)

    # --- INPUTS MODO B (PROYECTO) ---
    else: 
        cliente = st.text_input("Cliente:", placeholder="Ej: Hotel Ibis")
        # LA CLAVE DEL ÉXITO: COTIZACIÓN MODULAR
        es_modular = st.checkbox("🔀 Cotizar Modular (Separar PMS de POS)", value=False, help="Activar si el cliente va a tercerizar el restaurante.")
        
        st.subheader("Infraestructura")
        pms = st.selectbox("PMS (Hotel):", ["Ninguno", "Opera Cloud", "Opera V5", "Otro"])
        pos = st.selectbox("POS (A&B):", ["Ninguno", "Simphony Cloud", "Micros 3700"])
        
        tiendas = 1
        if pos != "Ninguno": tiendas = st.slider("Nº Tiendas:", 1, 10, 1)
        
        st.subheader("Volumen")
        trx = st.number_input("TRX Anuales Totales:", 0, 1000000, 12000)

# --- 6. LOGICA Y SALIDA ---
st.header("2. Guía de Llenado (El Instructor)")

# ==========================================
# MODO A: SERVICIOS PUNTUALES
# ==========================================
if modo.startswith("A"):
    precio_u = 0
    total = 0
    
    if "Reproceso" in servicio:
        precio_u = TARIFARIO["reproceso"]
        total = cantidad * precio_u
        tarjeta("1️⃣", "COTIZ", "Fila 'Saneamiento de Documentos'", f"Cant: {cantidad} | Unit: ${precio_u:,.0f}", 
                "Cobro por documento fallido (Tarifa 2025).")
    
    elif "Contrato" in servicio:
        total = TARIFARIO["soporte_10h"] if cantidad == 10 else TARIFARIO["soporte_20h"]
        tarjeta("1️⃣", "COTIZ", f"Sección 'Recurrentes' > Contrato {cantidad}h", f"Valor Mensual: ${total:,.0f}", 
                "Mantenimiento preventivo y correctivo. Facturación mensual.")
        
    else: # Bolsa y Capacitación
        # Cálculo de Tarifa por Volumen de Horas
        nombre_tarifa = ""
        if cantidad < 3: precio_u = TARIFARIO["demanda"]; nombre_tarifa = "Plena"
        elif 3 <= cantidad < 5: precio_u = TARIFARIO["bolsa_3h"]; nombre_tarifa = "Bolsa 3h"
        elif 5 <= cantidad < 10: precio_u = TARIFARIO["bolsa_5h"]; nombre_tarifa = "Bolsa 5h"
        elif 10 <= cantidad < 20: precio_u = TARIFARIO["bolsa_10h"]; nombre_tarifa = "Bolsa 10h"
        else: precio_u = TARIFARIO["bolsa_20h"]; nombre_tarifa = "Mayorista"
        
        total = cantidad * precio_u
        
        if servicio == "Paquete de Capacitación":
            st.success(f"🎓 Plan de Formación ({cantidad} Horas)")
            for tema in lista_cap:
                h_tema = CATALOGO_CAP[tema]
                tarjeta("🔹", "TIEMPOS", f"Fila '{tema}'", f"Cant: {h_tema}", 
                        f"Módulo estándar. Se cobrará a tarifa '{nombre_tarifa}' (${precio_u:,.0f}/h).")
            st.metric("Total Inversión", f"${total:,.0f} COP")
            
        else: # Bolsa Consultoría
            tarjeta("1️⃣", "COTIZ", "Fila 'Bolsa de Horas Consultoría'", f"Cant: {cantidad} | Unit: ${precio_u:,.0f}", 
                    f"Tarifa aplicada: {nombre_tarifa} (Según tabla oficial 2025).")
            st.success(f"💰 Total Bolsa: ${total:,.0f} COP")

# ==========================================
# MODO B: PROYECTO (CON LÓGICA MODULAR)
# ==========================================
else:
    # Función auxiliar para calcular horas por módulo
    def calcular_horas_modulo(tipo, sistema, n_tiendas=1):
        items = []
        horas = 0
        if tipo == "PMS":
            if sistema == "Opera Cloud":
                items.append(("Middleware + SIAT Cloud", 8, "Mandatorio Cloud")); horas += 8
            elif sistema == "Opera V5":
                items.append(("Conector Opera On-Premise", 32, "Estándar V5")); horas += 32
        elif tipo == "POS":
            if sistema == "Simphony Cloud":
                h = 24 + (8 * (n_tiendas - 1))
                items.append((f"Simphony ({n_tiendas} tiendas)", h, "24h Base + 8h/Adicional")); horas += h
            elif sistema == "Micros 3700":
                items.append(("Reinstalación Micros Legacy", 32, "Incluye 8h pruebas críticas")); horas += 32
        return items, horas

    # Lógica de Precios TRX
    p_trx = 25.0
    for t, p, n in RANGOS_TRX:
        if trx <= t: p_trx = p; break

    # --- RENDERIZADO MODULAR ---
    if es_modular:
        st.warning("🔀 MODO MODULAR: Se presentan dos presupuestos independientes.")
        col_hotel, col_ab = st.columns(2)
        
        with col_hotel:
            st.markdown("### 🏨 Cotización Hotel (PMS)")
            items_pms, h_pms = calcular_horas_modulo("PMS", pms)
            if pms == "Ninguno": st.caption("No aplica.")
            else:
                for i, h, j in items_pms: st.write(f"- [x] {i}: **{h}h**")
                st.info(f"Total Ingeniería: {h_pms} Horas")
                st.write(f"Fee TRX: ${p_trx} (Si asume volumen total)")

        with col_ab:
            st.markdown("### 🍽️ Cotización A&B (POS)")
            items_pos, h_pos = calcular_horas_modulo("POS", pos, tiendas)
            if pos == "Ninguno": st.caption("No aplica.")
            else:
                for i, h, j in items_pos: st.write(f"- [x] {i}: **{h}h**")
                st.info(f"Total Ingeniería: {h_pos} Horas")
                if trx < 5000: st.error("⚠️ Alerta: Volumen bajo. Sugerir Fee Fijo.")

    # --- RENDERIZADO UNIFICADO ---
    else:
        st.success("✅ MODO UNIFICADO: Economía de escala aplicada.")
        items_pms, h_pms = calcular_horas_modulo("PMS", pms)
        items_pos, h_pos = calcular_horas_modulo("POS", pos, tiendas)
        
        # Instructor paso a paso
        step = 1
        if pms != "Ninguno":
            st.markdown("#### 🏨 Infraestructura Hotelera")
            for i, h, j in items_pms:
                tarjeta(f"{step}", "TIEMPOS", f"Fila '{i}'", f"Cant: 1 (={h}h)", j)
                step += 1
                
        if pos != "Ninguno":
            st.markdown("#### 🍽️ Infraestructura Alimentos y Bebidas")
            for i, h, j in items_pos:
                alerta = "⚠️ Requiere Bolsa Soporte" if "Micros" in i else None
                tarjeta(f"{step}", "TIEMPOS", f"Fila '{i}'", f"Cant: 1 (={h}h)", j, alerta)
                step += 1
        
        st.markdown("#### 📊 Transaccionalidad")
        tarjeta(f"{step}", "DATOS", "Valor Unitario TRX", f"${p_trx} COP", f"Basado en volumen de {trx:,} docs/año.")
