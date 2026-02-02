import streamlit as st

# --- CONFIGURACIÓN E INTERFAZ ---
st.set_page_config(page_title="Cotizador Satcom v3.5", page_icon="🛠️")

# Estilo para ocultar menús internos y que se vea como una web limpia
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- DATOS MAESTROS (TARIFARIO 2025) ---
TARIFARIO = {
    "demanda": 200000,
    "bolsa_3h": 180000,
    "bolsa_5h": 172000,
    "bolsa_10h": 170000,
    "bolsa_20h": 140000,
    "reproceso": 6000
}

def obtener_tarifa(horas):
    if horas < 3: return TARIFARIO["demanda"]
    if horas < 5: return TARIFARIO["bolsa_3h"]
    if horas < 10: return TARIFARIO["bolsa_5h"]
    if horas < 20: return TARIFARIO["bolsa_10h"]
    return TARIFARIO["bolsa_20h"]

# --- CONTENIDO PRINCIPAL ---
st.title("🛠️ Cotizador de Servicios Profesionales")
st.write("Bienvenido. Seleccione los parámetros de su requerimiento para obtener una estimación inmediata.")

menu = st.segmented_control(
    "Seleccione el tipo de servicio:",
    ["Bolsa de Horas", "Proyecto Integral", "Capacitación", "Reprocesos"],
    default="Bolsa de Horas"
)

st.divider()

if menu == "Bolsa de Horas":
    st.subheader("🩹 Consultoría por Horas")
    horas = st.number_input("Cantidad de horas estimadas:", min_value=1, value=5)
    t = obtener_tarifa(horas)
    st.metric("Total Estimado", f"${(horas * t):,.0f} COP", f"Tarifa: ${t:,.0f}/h")

elif menu == "Proyecto Integral":
    st.subheader("🏗️ Wizard de Implementación")
    col1, col2 = st.columns(2)
    with col1:
        puntos = st.number_input("Puntos de Venta (POS):", 1, 50, 1)
        infra = st.selectbox("Infraestructura:", ["Nube (Cloud)", "Servidor Local"])
    with col2:
        migracion = st.checkbox("¿Requiere migración de datos?")
        soporte = st.checkbox("Soporte presencial (Semana 1)")

    # Lógica de ingeniería (HH)
    total_h = 10 + (puntos * 2) + (6 if infra == "Servidor Local" else 0) + (8 if migracion else 0) + (4 if soporte else 0)
    tarifa_proy = obtener_tarifa(total_h)
    
    st.success(f"### Inversión Estimada: ${(total_h * tarifa_proy):,.0f} COP")
    st.info(f"Esfuerzo técnico calculado: {total_h} horas hombre.")

elif menu == "Capacitación":
    st.subheader("🎓 Paquetes de Formación")
    modulos = st.multiselect("Módulos requeridos:", ["Operativo", "Administrativo", "Auditoría", "Inventarios"])
    total_h_cap = len(modulos) * 4
    if total_h_cap > 0:
        t_cap = obtener_tarifa(total_h_cap)
        st.metric("Costo Formación", f"${(total_h_cap * t_cap):,.0f} COP")

elif menu == "Reprocesos":
    st.subheader("🔄 Saneamiento de Documentos")
    docs = st.number_input("Número de documentos:", min_value=1, value=100)
    st.metric("Total Proyecto", f"${(docs * TARIFARIO['reproceso']):,.0f} COP")

st.divider()
st.caption("Esta herramienta es de uso libre y no genera compromisos contractuales automáticos.")
