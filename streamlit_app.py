
!pip install streamlit pandas plotly
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuración de la Página ---
# st.set_page_config debe ser el primer comando de Streamlit
st.set_page_config(
    page_title="Análisis Financiero | Consultora",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Funciones de Página ---

def mostrar_resumen():
    """Muestra un dashboard o resumen general."""
    st.title("Resumen General 📈")
    st.markdown("Bienvenido al panel de análisis financiero de [Nombre de tu Consultora].")

    # KPIs de ejemplo
    st.header("Indicadores Clave (KPIs)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Ingresos Totales (YTD)", "$1.2M", "12%")
    col2.metric("EBITDA", "$450K", "8.5%")
    col3.metric("Nuevos Clientes", "58", "-2%")

    # Gráfico de ejemplo
    st.subheader("Crecimiento de Ingresos (Ejemplo)")
    # Datos de ejemplo para el gráfico
    chart_data = pd.DataFrame(
        {
            "Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun"],
            "Ingresos": [180, 210, 220, 205, 240, 260]
        }
    )
    fig = px.line(chart_data, x="Mes", y="Ingresos", title="Ingresos Mensuales", markers=True)
    st.plotly_chart(fig, use_container_width=True)

def analizar_datos():
    """Página para cargar y analizar un conjunto de datos."""
    st.title("Análisis de Datos 📊")
    st.write("Carga un archivo CSV con tus datos financieros (ej. estado de resultados, balance, etc.)")

    # Carga de archivo
    uploaded_file = st.file_uploader("Elige tu archivo CSV", type=["csv"])

    if uploaded_file is not None:
        try:
            # Leer los datos
            data = pd.read_csv(uploaded_file)
            st.success("¡Archivo cargado exitosamente!")

            # Guardar en el estado de la sesión para usarlo en otras páginas
            st.session_state['data'] = data

            # Mostrar el dataframe
            st.header("Vista Previa de los Datos")
            st.dataframe(data.head())

            # Mostrar estadísticas descriptivas
            st.header("Estadísticas Descriptivas")
            st.write(data.describe())

            # Mostrar tipos de datos
            st.header("Información de Columnas")
            st.dataframe(data.info())

        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
    else:
        st.info("Esperando que se cargue un archivo CSV.")

def visualizar_datos():
    """Página para crear visualizaciones interactivas."""
    st.title("Visualización de Datos 📉")

    # Comprobar si los datos están en el estado de la sesión
    if 'data' not in st.session_state:
        st.warning("Por favor, carga un archivo CSV en la página 'Análisis de Datos' primero.")
        return

    data = st.session_state['data']
    all_columns = data.columns.tolist()

    st.header("Crear Gráfico Interactivo")

    # --- Selector de Tipo de Gráfico ---
    chart_type = st.selectbox("Elige el tipo de gráfico:", ["Gráfico de Línea", "Gráfico de Barras", "Gráfico de Dispersión"])

    if chart_type == "Gráfico de Línea":
        st.subheader("Gráfico de Línea")
        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox("Elige la columna para el Eje X (ej. Fecha, Año):", all_columns, key="line_x")
        with col2:
            y_axis = st.selectbox("Elige la columna para el Eje Y (ej. Ingresos, Costos):", all_columns, key="line_y")
        
        if x_axis and y_axis:
            fig = px.line(data, x=x_axis, y=y_axis, title=f"{y_axis} a lo largo de {x_axis}", markers=True)
            st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Gráfico de Barras":
        st.subheader("Gráfico de Barras")
        col1, col2 = st.columns(2)
        with col1:
            x_axis_bar = st.selectbox("Elige la columna categórica (Eje X):", all_columns, key="bar_x")
        with col2:
            y_axis_bar = st.selectbox("Elige la columna numérica (Eje Y):", all_columns, key="bar_y")

        if x_axis_bar and y_axis_bar:
            # Agrupar por la columna categórica y sumar la numérica (común para finanzas)
            grouped_data = data.groupby(x_axis_bar)[y_axis_bar].sum().reset_index()
            fig = px.bar(grouped_data, x=x_axis_bar, y=y_axis_bar, title=f"Total de {y_axis_bar} por {x_axis_bar}")
            st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Gráfico de Dispersión":
        st.subheader("Gráfico de Dispersión (Scatter Plot)")
        st.write("Útil para ver la relación entre dos variables numéricas.")
        col1, col2 = st.columns(2)
        with col1:
            x_axis_scatter = st.selectbox("Elige la variable del Eje X:", all_columns, key="scatter_x")
        with col2:
            y_axis_scatter = st.selectbox("Elige la variable del Eje Y:", all_columns, key="scatter_y")

        if x_axis_scatter and y_axis_scatter:
            fig = px.scatter(data, x=x_axis_scatter, y=y_axis_scatter, title=f"Relación entre {x_axis_scatter} y {y_axis_scatter}")
            st.plotly_chart(fig, use_container_width=True)

def simular_escenarios():
    """Página para un simulador financiero simple."""
    st.title("Simulación de Escenarios 🔮")
    st.header("Proyección de Ingresos Simple")

    col1, col2 = st.columns(2)
    
    with col1:
        current_revenue = st.number_input("Ingresos Actuales ($)", min_value=0.0, value=1000000.0, step=50000.0)
        growth_rate = st.slider("Tasa de Crecimiento Anual Esperada (%)", min_value=-10.0, max_value=50.0, value=5.0, step=0.5)
    
    with col2:
        years = st.number_input("Años a Proyectar", min_value=1, max_value=20, value=5, step=1)
        
    if st.button("Calcular Proyección"):
        projection = []
        projected_revenue = current_revenue
        
        for year in range(1, int(years) + 1):
            projected_revenue *= (1 + growth_rate / 100)
            projection.append({"Año": year, "Ingresos Proyectados": projected_revenue})
        
        proj_df = pd.DataFrame(projection)
        
        st.subheader("Resultados de la Proyección")
        st.dataframe(proj_df.style.format({"Ingresos Proyectados": "${:,.2f}"}))
        
        # Gráfico de la proyección
        fig_proj = px.line(proj_df, x="Año", y="Ingresos Proyectados", title="Proyección de Ingresos", markers=True)
        fig_proj.update_yaxes(tickprefix="$", tickformat=",.0f")
        st.plotly_chart(fig_proj, use_container_width=True)

def acerca_de():
    """Página con información de la consultora."""
    st.title("Acerca de [Nombre de tu Consultora]")
    st.image("https://placehold.co/800x200/004080/FFFFFF?text=Tu+Logo+Aquí", use_column_width=True)
    
    st.header("Nuestra Misión")
    st.write(
        """
        Ayudar a nuestros clientes a tomar decisiones financieras más inteligentes 
        a través del poder de los datos y el análisis avanzado.
        """
    )
    
    st.header("El Equipo")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Juan Pérez")
        st.write("Socio Fundador, CFA")
        st.write("Experto en valoración de empresas y M&A.")
    with col2:
        st.subheader("María Gómez")
        st.write("Directora de Análisis de Datos")
        st.write("Especialista en modelado predictivo y machine learning.")
        
    st.header("Contáctanos")
    st.write("📧 email@tuconsultora.com")
    st.write("🌐 www.tuconsultora.com")

# --- Barra Lateral de Navegación ---
st.sidebar.title("Navegación")
st.sidebar.write("Consultora Financiera")

# Opciones de página
paginas = {
    "Resumen General": mostrar_resumen,
    "Análisis de Datos": analizar_datos,
    "Visualización de Datos": visualizar_datos,
    "Simulación de Escenarios": simular_escenarios,
    "Acerca de": acerca_de
}

# Selector de página
seleccion = st.sidebar.radio("Ir a:", list(paginas.keys()))

# Ejecutar la función de la página seleccionada
paginas[seleccion]()
