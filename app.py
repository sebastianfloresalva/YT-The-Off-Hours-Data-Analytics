import streamlit as st
from google import genai
from google.genai import types
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. CONFIGURACIÓN INICIAL DE LA APLICACIÓN
st.set_page_config(
    page_title="YouTube Statistical WarRoom (Music Edition)",
    page_icon="🎧",
    layout="wide"
)

st.markdown("""
    <style>
    .stMetric { background-color: #161618; padding: 15px; border-radius: 8px; border: 1px solid #2d2d30; }
    </style>
""", unsafe_allow_html=True)

# 2. BARRA LATERAL Y SEGURIDAD DE IA
st.sidebar.title("🎧 WarRoom Control Center")
api_key_input = st.sidebar.text_input("Google AI Studio API Key", type="password")
api_key = api_key_input if api_key_input else st.secrets.get("GEMINI_API_KEY", "")

client = None
if api_key:
    try:
        client = genai.Client(api_key=api_key)
        st.sidebar.success("🔥 GenAI Conectado (Thinking High)")
    except Exception as e:
        st.sidebar.error(f"Error de inicialización IA: {e}")
else:
    st.sidebar.warning("⚠️ Ingresa tu API Key para habilitar al Consultor IA.")

# Filtro Temporal Global (Cohortes de ciclo de vida)
st.sidebar.markdown("---")
st.sidebar.subheader("⏱️ Filtro Temporal (Ciclo de Vida)")
ventana_tiempo = st.sidebar.selectbox(
    "Selecciona ventana de análisis:",
    ["Primeras 24 Horas", "Ventana de 5 Días", "Ventana de 7 Días", "Ventana de 15 Días", "Ventana de 30 Días (Maduración)"]
)

st.title("🎧 YouTube Music WarRoom: Master Edition")
st.markdown(f"*Analítica avanzada, visualización por cuadrantes estadísticos y consultoría de IA para música de larga duración ({ventana_tiempo}).*")

# 3. BASE DE DATOS MAESTRA (SIMULADA / API READY)
if "df_warroom" not in st.session_state:
    st.session_state.df_warroom = pd.DataFrame({
        "Mix_Video": ["2 AM Study Lofi (1h)", "Deep Focus Ambient (2h)", "Sleep & Relax Beats (3h)", "Cyberpunk Synthwave (1.5h)"],
        "Duracion_Horas": [1.0, 2.0, 3.0, 1.5],
        "Visualizaciones": [2400, 8100, 15300, 4100],
        "Impresiones": [50000, 95000, 160000, 60000],
        "CTR (%)": [4.8, 8.5, 9.6, 6.8],
        "Retencion_Media (%)": [39.0, 46.5, 69.0, 42.5],
        "Guardados_Playlists": [130, 480, 1020, 225],
        "Oyentes_Recurrentes_Pct": [45.0, 60.0, 75.0, 50.0],
        "Likes": [210, 750, 1400, 380],
        "Comentarios": [15, 42, 85, 20],
        "Compartidos": [30, 110, 250, 45],
        "Trafico_Home_Browse_Pct": [65.0, 72.0, 80.0, 55.0]
    })

df = st.session_state.df_warroom
df["Engagement_Rate (%)"] = ((df["Likes"] + df["Comentarios"] + df["Compartidos"]) / df["Visualizaciones"]) * 100

# 4. ESTADÍSTICOS BASE (MEDIAS Y MEDIANAS)
mean_ctr, median_ctr = df["CTR (%)"].mean(), df["CTR (%)"].median()
mean_ret, median_ret = df["Retencion_Media (%)"].mean(), df["Retencion_Media (%)"].median()
mean_eng, median_eng = df["Engagement_Rate (%)"].mean(), df["Engagement_Rate (%)"].median()

# 5. PESTAÑAS PRINCIPALES
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Panel Jerárquico de Métricas", 
    "🗺️ Cuadrantes Estadísticos & Outliers", 
    "🧪 Laboratorio A/B Testing Estético", 
    "🤖 Consultor IA Avanzado"
])

with tab1:
    st.subheader("🥇 Nivel 1: El Núcleo de Crecimiento (Gatillos del Algoritmo)")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Visualizaciones Totales", f"{df['Visualizaciones'].sum():,}", "Macro Canal")
    c2.metric("CTR Promedio", f"{df['CTR (%)'].mean():.2f}%", f"Media: {mean_ctr:.2f}%")
    c3.metric("Retención Media (APV)", f"{df['Retencion_Media (%)'].mean():.2f}%", f"Media: {mean_ret:.1f}%")
    c4.metric("Impresiones Totales", f"{df['Impresiones'].sum():,}", "Alcance Global")

    st.markdown("---")
    st.subheader("🥈 Nivel 2: Métricas de Hábito y Audio (Música Larga)")
    mc1, mc2, mc3 = st.columns(3)
    mc1.metric("Total Guardados (Playlists)", f"{df['Guardados_Playlists'].sum():,}", "Señal de Hábito Extrema")
    mc2.metric("Engagement Rate Medio", f"{df['Engagement_Rate (%)'].mean():.2f}%", f"Mediana: {median_eng:.2f}%")
    mc3.metric("Oyentes Recurrentes", f"{df['Oyentes_Recurrentes_Pct'].mean():.1f}%", "Fidelización")

    st.markdown("---")
    st.subheader("📋 Tabla Maestra de Rendimiento por Mix")
    st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("🗺️ Mapa de Dispersión (CTR vs. Retención)")
    st.markdown("Líneas de corte dinámicas: **Media de CTR (Rojo Neón)** y **Media de Retención (Azul Eléctrico)**.")

    fig_scatter = px.scatter(
        df, x="CTR (%)", y="Retencion_Media (%)", size="Guardados_Playlists", color="Mix_Video",
        hover_name="Mix_Video", title=f"Análisis de Cuadrantes ({ventana_tiempo})",
        template="plotly_dark"
    )

    fig_scatter.add_vline(x=mean_ctr, line_dash="dash", line_color="#FF073A", line_width=2, annotation_text=f"Media CTR: {mean_ctr:.2f}%")
    fig_scatter.add_hline(y=mean_ret, line_dash="dash", line_color="#00F0FF", line_width=2, annotation_text=f"Media Retención: {mean_ret:.1f}%")

    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("### 📂 Distribución de Guardados en Listas de Reproducción")
    fig_pl = px.bar(df, x="Mix_Video", y="Guardados_Playlists", color="Guardados_Playlists", template="plotly_dark")
    median_pl = df["Guardados_Playlists"].median()
    fig_pl.add_hline(y=median_pl, line_dash="dot", line_color="#FF00FF", annotation_text=f"Mediana Pls: {median_pl}")
    st.plotly_chart(fig_pl, use_container_width=True)

with tab3:
    st.subheader("🧪 A/B Testing para Arte Visual (*Faceless*)")
    st.markdown("Compara conceptos estéticos para optimizar el CTR inicial.")

    with st.form("ab_music_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Variante A**")
            t_a = st.text_input("Título A", value="Lofi Hip Hop Beats - Live to Study")
            v_a = st.text_input("Visual A", value="Ilustración lluvia ventana azulada")
            ctr_a = st.number_input("CTR A (%)", value=4.5)
        with col_b:
            st.markdown("**Variante B**")
            t_b = st.text_input("Título B", value="Late Night Lofi Session 🌙")
            v_b = st.text_input("Visual B", value="Animación 3D retro VHS tonos cálidos")
            ctr_b = st.number_input("CTR B (%)", value=7.2)
            
        run_ab = st.form_submit_button("Analizar Experimento Visual con IA")

    if run_ab:
        if client:
            with st.spinner("Analizando psicología visual con Thinking High..."):
                prompt_ab = f"""
                Analiza este test A/B de empaque visual para música de larga duración:
                - Variante A: Título="{t_a}" | Visual="{v_a}" | CTR={ctr_a}%
                - Variante B: Título="{t_b}" | Visual="{v_b}" | CTR={ctr_b}%
                Explica por qué una funcionó mejor en el CTR sin repetir datos crudos.
                """
                res_ab = client.models.generate_content(
                    model='gemini-2.5-pro',
                    contents=prompt_ab,
                    config=types.GenerateContentConfig(thinking_config=types.ThinkingConfig(thinking_budget=2048))
                )
                st.success("Resultado del Análisis Estético:")
                st.write(res_ab.text)
        else:
            st.error("Conecta tu API Key.")

with tab4:
    st.subheader("🤖 Consultor Estratégico (Nivel de Pensamiento: High)")
    st.markdown("La IA analiza los datos comparativamente frente a las líneas base del canal.")

    scope = st.radio("Selecciona el alcance de la auditoría:", ["Canal Completo (General)", "Mix / Video Específico"])
    target_mix = st.selectbox("Selecciona el mix a auditar:", df["Mix_Video"].tolist()) if scope == "Mix / Video Específico" else ""

    user_query = st.text_area(
        "¿Qué desafío creativo o estadístico quieres resolver?",
        placeholder="Ej: ¿Por qué este mix tiene un rendimiento atípico en comparación con la media del canal?"
    )

    if st.button("Ejecutar Auditoría Táctica con IA"):
        if client:
            with st.spinner("Procesando auditoría profunda (Thinking High)..."):
                baselines_texto = f"""
                LÍNEAS BASE DEL CANAL (BENCHMARK INTERNO):
                - Media de CTR del canal: {mean_ctr:.2f}% (Mediana: {median_ctr:.2f}%)
                - Media de Retención del canal: {mean_ret:.2f}% (Mediana: {median_ret:.2f}%)
                - Media de Engagement Rate: {mean_eng:.2f}%
                """
                
                datos_completos = df.to_string()
                
                prompt_maestro = f"""
                Eres un científico de datos y consultor senior de canales de música de larga duración en YouTube.
                {baselines_texto}
                DATOS DE LOS VIDEOS:
                {datos_completos}
                ALCANCE DE LA CONSULTA: {scope} {f'(Mix seleccionado: {target_mix})' if scope == 'Mix / Video Específico' else ''}
                PREGUNTA DEL CREADOR: {user_query}
                
                INSTRUCCIONES ESTRICTAS:
                - NO recites tablas de datos ni repites números uno por uno.
                - Utiliza los números SOLAMENTE como evidencia analítica matemática para calcular deltas o comparaciones frente a las líneas base del canal.
                - Estructura tu respuesta obligatoriamente en:
                  1. 📌 Resumen Ejecutivo (Puntos Clave)
                  2. 🧠 Diagnóstico Estadístico y Psicológico
                  3. 🚀 Plan de Acción Táctico
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-pro',
                    contents=prompt_maestro,
                    config=types.GenerateContentConfig(
                        thinking_config=types.ThinkingConfig(thinking_budget=4096),
                        temperature=0.3
                    )
                )
                
                st.success("Auditoría Finalizada:")
                st.write(response.text)
        else:
            st.error("Falta la API Key en la barra lateral.")

st.markdown("---")
st.caption(f"🎧 YouTube Statistical WarRoom | Modo activo: {ventana_tiempo} | Zero-Cost Free Tier Optimized.")
