import streamlit as st
import pandas as pd
from truth_table import generar_tabla

st.title("calc-lógica: Generador de Tablas de Verdad")
st.write("Ingresa una expresión usando AND, OR, NOT, XOR y variables en mayúsculas (A, B...).")

expresion = st.text_input("Expresión Lógica:", value="A AND B")

if st.button("Generar Tabla"):
    if expresion:
        vars_nombres, datos = generar_tabla(expresion)
        
        if vars_nombres:
            # Crear el encabezado de la tabla
            columnas = vars_nombres + ["Resultado"]
            df = pd.DataFrame(datos, columns=columnas)
            
            # Mostrar la tabla en formato 0/1
            st.table(df)
        else:
            st.error(f"Error en la expresión: {datos}")
    else:
        st.warning("Por favor, ingresa una expresión.")

