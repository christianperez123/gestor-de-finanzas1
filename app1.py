import streamlit as st
import pandas as pd
import datetime
import os

# 1. Configuración de la página y Archivo de Datos
st.set_page_config(page_title="Gestor Finanzas", layout="wide", page_icon="💰")
FILE_NAME = "mis_finanzas.csv"

if 'transactions' not in st.session_state:
    if os.path.exists(FILE_NAME):
        st.session_state.transactions = pd.read_csv(FILE_NAME)
    else:
        initial_data = {
            'Fecha': ['2026-01-01', '2026-01-05'], 
            'Descripción': ['Mesada/Salario', 'Suscripciones'], 'Tipo': ['Ingreso', 'Gasto'], 'Monto': [3000.0, 1000.0]
        }
        st.session_state.transactions = pd.DataFrame(initial_data)

if 'pantalla' not in st.session_state:
    st.session_state.pantalla = "bienvenida"

# 2. PANTALLA DE BIENVENIDA
if st.session_state.pantalla == "bienvenida":
    st.title("🚀 Toma el Control de tu Futuro Financiero")
    st.markdown("""
    **¿Llegas a fin de mes preguntándote a dónde se fue tu dinero?** Para un estudiante, la falta de orden financiero es el enemigo silencioso que sabotea metas y acumula estrés. 
    Este **Gestor de Finanzas** interactivo transformará tu caos en claridad matemática. ¡Empieza hoy!
    """)
    if st.button("🚀 Entrar al Gestor Financiero", use_container_width=True):
        st.session_state.pantalla = "dashboard"
        st.rerun()

# 3. PANTALLA PRINCIPAL
else:
    st.title("📊 Mi Gestor Financiero")
    
    with st.sidebar:
        st.header("➕ Nueva Transacción")
        desc = st.text_input("Descripción", placeholder="Ej. Almuerzo")
        type_t = st.selectbox("Tipo", ["Ingreso", "Gasto"])
        amt = st.number_input("Monto ($)", min_value=0.0, format="%.2f")
        date_t = st.date_input("Fecha", datetime.date.today())
        
        if st.button("Guardar", use_container_width=True):
            if desc and amt > 0:
                new_t = pd.DataFrame([{'Fecha': str(date_t), 'Descripción': desc, 'Tipo': type_t, 'Monto': amt}])
                st.session_state.transactions = pd.concat([st.session_state.transactions, new_t], ignore_index=True)
                st.session_state.transactions.to_csv(FILE_NAME, index=False)
                st.success("¡Guardado!")
                st.rerun()
            else:
                st.warning("Completa los campos.")
        
        if st.button("⬅️ Ver Bienvenida", use_container_width=True):
            st.session_state.pantalla = "bienvenida"
            st.rerun()

    # Operaciones Matemáticas
    df = st.session_state.transactions
    ingresos = df[df['Tipo'] == 'Ingreso']['Monto'].sum()
    gastos = df[df['Tipo'] == 'Gasto']['Monto'].sum()
    balance = ingresos - gastos

    tab1, tab2 = st.tabs(["📈 Resumen y Gráficos", "📋 Historial y Opciones"])

    with tab1:
        c1, c2, c3 = st.columns(3)
        c1.metric("Balance Disponible", f"${balance:,.2f}", delta=f"${balance:,.2f}")
        c2.metric("Total Ingresos", f"${ingresos:,.2f}")
        c3.metric("Total Gastos", f"${gastos:,.2f}", delta=f"-${gastos:,.2f}", delta_color="inverse")
        
        st.markdown("---")
        
        cg1, cg2 = st.columns(2)
        with cg1:
            st.subheader("Ingresos vs Gastos")
            st.bar_chart(pd.DataFrame({'Monto': [ingresos, gastos]}, index=['Ingresos', 'Gastos']))
        with cg2:
            st.subheader("Flujo en el Tiempo")
            if not df.empty:
                st.line_chart(df.groupby(['Fecha', 'Tipo'])['Monto'].sum().unstack(fill_value=0))

    with tab2:
        st.subheader("Registro Histórico")
        
        if not df.empty:
            # Mostramos la tabla normal (añadiendo el índice visual para que el usuario sepa qué número es cada fila)
            st.dataframe(df, use_container_width=True)
            
            st.markdown("---")
            st.subheader("🗑️ Eliminar una Transacción")
            
            # Creamos una lista de opciones legibles para el menú desplegable (Ej: "0 - Salario ($3000)")
            opciones = [f"{idx} - {row['Descripción']} (${row['Monto']})" for idx, row in df.iterrows()]
            seleccion = st.selectbox("Selecciona la transacción que deseas eliminar:", opciones)
            
            # Al hacer clic en el botón, extraemos el número (ID) de la opción y lo borramos
            if st.button("❌ Eliminar Transacción Seleccionada", type="primary"):
                fila_id = int(seleccion.split(" - ")[0]) # Obtiene el número de fila
                st.session_state.transactions = df.drop(fila_id).reset_index(drop=True) # Lo borra y reordena
                st.session_state.transactions.to_csv(FILE_NAME, index=False) # Guarda en el archivo
                st.success("¡Transacción eliminada!")
                st.rerun()
        else:
            st.info("El historial está vacío.")
            
        if st.button("Resetear Todo"):
            if os.path.exists(FILE_NAME):
                os.remove(FILE_NAME)
            st.session_state.transactions = pd.DataFrame(columns=['Fecha', 'Descripción', 'Tipo', 'Monto'])
            st.rerun()
