import streamlit as st
import pandas as pd
import datetime
import os

# 1. Configuración de la página y Guardado de Datos (Local Storage simulado)
st.set_page_config(page_title="Gestor Finanzas", layout="wide", page_icon="💰")
FILE_NAME = "mis_finanzas.csv"

# Carga datos guardados previamente; si no existen, crea el historial inicial
if 'transactions' not in st.session_state:
    if os.path.exists(FILE_NAME):
        st.session_state.transactions = pd.read_csv(FILE_NAME, parse_dates=['Fecha'])
    else:
        initial_data = {
            'Fecha': [datetime.date(2026, 1, 1), datetime.date(2026, 1, 5)], 
            'Descripción': ['Mesada/Salario', 'Suscripciones'], 'Tipo': ['Ingreso', 'Gasto'], 'Monto': [3000.0, 1000.0]
        }
        st.session_state.transactions = pd.DataFrame(initial_data)

# Control de navegación para la pantalla de bienvenida
if 'pantalla' not in st.session_state:
    st.session_state.pantalla = "bienvenida"

# 2. PANTALLA DE BIENVENIDA (Mensaje convincente)
if st.session_state.pantalla == "bienvenida":
    st.title("🚀 Toma el Control de tu Futuro Financiero")
    
    st.markdown("""
    **¿Llegas a fin de mes preguntándote a dónde se fue tu dinero?**  
    Para un estudiante o joven profesional, la falta de orden financiero es el enemigo silencioso que sabotea tus metas, 
    acumula estrés y limita tu libertad. 
    
    Este **Gestor de Finanzas Personal** no es una planilla aburrida; es tu centro de comandos. Diseñado para ser 
    ultrarrápido, visual e interactivo, te ayudará a transformar el caos en claridad matemática. Deja de adivinar 
    y empieza a construir tu estabilidad desde hoy.
    """)
    
    # Botón grande para avanzar a la aplicación
    if st.button("🚀 Entrar al Gestor Financiero", use_container_width=True):
        st.session_state.pantalla = "dashboard"
        st.rerun()

# 3. PANTALLA PRINCIPAL DE LA APLICACIÓN
else:
    st.title("📊 Mi Dashboard Financiero")
    
    # Barra Lateral para añadir datos
    with st.sidebar:
        st.header("➕ Nueva Transacción")
        desc = st.text_input("Descripción", placeholder="Ej. Almuerzo")
        type_t = st.selectbox("Tipo", ["Ingreso", "Gasto"])
        amt = st.number_input("Monto ($)", min_value=0.0, format="%.2f")
        date_t = st.date_input("Fecha", datetime.date.today())
        
        if st.button("Guardar", use_container_width=True):
            if desc and amt > 0:
                new_t = pd.DataFrame([{'Fecha': date_t, 'Descripción': desc, 'Tipo': type_t, 'Monto': amt}])
                st.session_state.transactions = pd.concat([st.session_state.transactions, new_t], ignore_index=True)
                
                # FUNCIÓN CLAVE: Guarda los progresos automáticamente en el archivo físico .csv
                st.session_state.transactions.to_csv(FILE_NAME, index=False)
                st.success("¡Guardado!")
                st.rerun()
            else:
                st.warning("Completa los campos correctamente.")
        
        # Botón para regresar a la bienvenida si el usuario quiere leer el mensaje de nuevo
        if st.button("⬅️ Ver Bienvenida", use_container_width=True):
            st.session_state.pantalla = "bienvenida"
            st.rerun()

    # Operaciones de Datos
    df = st.session_state.transactions
    ingresos = df[df['Tipo'] == 'Ingreso']['Monto'].sum()
    gastos = df[df['Tipo'] == 'Gasto']['Monto'].sum()
    balance = ingresos - gastos

    # Pestañas visuales
    tab1, tab2 = st.tabs(["📈 Resumen y Gráficos", "📋 Historial"])

    with tab1:
        # Métricas principales
        c1, c2, c3 = st.columns(3)
        c1.metric("Balance Disponible", f"${balance:,.2f}", delta=f"${balance:,.2f}")
        c2.metric("Total Ingresos", f"${ingresos:,.2f}")
        c3.metric("Total Gastos", f"${gastos:,.2f}", delta=f"-${gastos:,.2f}", delta_color="inverse")
        
        st.markdown("---")
        
        # Gráficos paralelos sencillos
        cg1, cg2 = st.columns(2)
        with cg1:
            st.subheader("Ingresos vs Gastos")
            st.bar_chart(pd.DataFrame({'Monto': [ingresos, gastos]}, index=['Ingresos', 'Gastos']))
        with cg2:
            st.subheader("Flujo en el Tiempo")
            st.line_chart(df.groupby(['Fecha', 'Tipo'])['Monto'].sum().unstack(fill_value=0))

    with tab2:
        st.subheader("Registro Histórico")
        st.dataframe(df.sort_values(by='Fecha', ascending=False), use_container_width=True, hide_index=True)
        
        if st.button("Resetear Base de Datos"):
            if os.path.exists(FILE_NAME):
                os.remove(FILE_NAME) # Borra el archivo guardado
            st.session_state.transactions = pd.DataFrame(columns=['Fecha', 'Descripción', 'Tipo', 'Monto'])
            st.rerun()