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
                # Guardamos la fecha como texto plano para evitar errores de compatibilidad
                new_t = pd.DataFrame([{'Fecha': str(date_t), 'Descripción': desc, 'Tipo': type_t, 'Monto': amt}])
                st.session_state.transactions = pd.concat([st.session_state.transactions, new_t], ignore_index=True)
                st.session_state.transactions.to_csv(FILE_NAME, index=False) # Guarda en el archivo
                st.success("¡Guardado!")
                st.rerun()
            else:
                st.warning("Completa los campos.")
        
        if st.button("⬅️ Ver Bienvenida", use_container_width=True):
            st.session_state.pantalla = "bienvenida"
            st.rerun()

    # Cálculos matemáticos de las métricas
    df = st.session_state.transactions
    ingresos = df[df['Tipo'] == 'Ingreso']['Monto'].sum()
    gastos = df[df['Tipo'] == 'Gasto']['Monto'].sum()
    balance = ingresos - gastos

    tab1, tab2 = st.tabs(["📈 Resumen y Gráficos", "📋 Historial e Interacción"])

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
        st.caption("💡 Para BORRAR: Haz clic en el cuadro al lado izquierdo de la fila y presiona la tecla 'Suprimir' (Delete) en tu teclado. Luego dale al botón Guardar Cambios.")
        
        # El truco: data_editor permite modificar la tabla directamente en pantalla
        edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
        
        # Si el usuario borró o editó algo, guardamos los cambios al presionar este botón
        if st.button("💾 Guardar Cambios en el Historial", type="primary"):
            st.session_state.transactions = edited_df
            st.session_state.transactions.to_csv(FILE_NAME, index=False)
            st.success("¡Historial actualizado correctamente!")
            st.rerun()
            
        if st.button("Resetear Todo"):
            if os.path.exists(FILE_NAME):
                os.remove(FILE_NAME)
            st.session_state.transactions = pd.DataFrame(columns=['Fecha', 'Descripción', 'Tipo', 'Monto'])
            st.rerun()
