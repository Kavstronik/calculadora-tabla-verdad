import streamlit as st

# Intentamos importar tu lógica
try:
    from truth_table import generar_y_descargar
except Exception as e:
    st.error(f"Error al importar el motor: {e}")

st.title("Calculadora de Kelvin")

# --- LÓGICA DE INTERCAMBIO DE MODO ---
if 'modo_entrada' not in st.session_state:
    st.session_state.modo_entrada = "teclado"

if 'texto_expresion' not in st.session_state:
    st.session_state.texto_expresion = ""

# Función para añadir símbolos desde botones
def insertar_simbolo(simbolo):
    st.session_state.texto_expresion += simbolo

col_btn1, col_btn2 = st.columns(2)
if col_btn1.button("⌨️ Modo Teclado"):
    st.session_state.modo_entrada = "teclado"
if col_btn2.button("🔘 Botonera Virtual"):
    st.session_state.modo_entrada = "botones"

# --- RENDERIZADO DE ENTRADA ---
if st.session_state.modo_entrada == "teclado":
    expresion = st.text_input("Escribe o pega tu ejercicio:", value=st.session_state.texto_expresion)
    st.session_state.texto_expresion = expresion
else:
    st.write("Selecciona los operadores y variables:")
    
    # Fila 1: Variables y Negación
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("P", on_click=insertar_simbolo, args=("p",), use_container_width=True)
    with c2: st.button("Q", on_click=insertar_simbolo, args=("q",), use_container_width=True)
    with c3: st.button("R", on_click=insertar_simbolo, args=("r",), use_container_width=True)
    with c4: st.button("NOT (~)", on_click=insertar_simbolo, args=("~",), use_container_width=True)
    
    # Fila 2: Operadores Básicos
    c5, c6, c7, c8 = st.columns(4)
    with c5: st.button("AND (^)", on_click=insertar_simbolo, args=("^",), use_container_width=True)
    with c6: st.button("OR (v)", on_click=insertar_simbolo, args=(" v ",), use_container_width=True)
    with c7: st.button("IF (->)", on_click=insertar_simbolo, args=(" -> ",), use_container_width=True)
    with c8: st.button("IFF (<->)", on_click=insertar_simbolo, args=(" <-> ",), use_container_width=True)

    # Fila 3: Operadores Especiales (XOR, NAND, NOR)
    c9, c10, c11, c12 = st.columns(4)
    with c9: st.button("XOR (⊕)", on_click=insertar_simbolo, args=(" xor ",), use_container_width=True)
    with c10: st.button("NAND (↑)", on_click=insertar_simbolo, args=(" nand ",), use_container_width=True)
    with c11: st.button("NOR (↓)", on_click=insertar_simbolo, args=(" nor ",), use_container_width=True)
    with c12: st.button("🧹 Borrar", on_click=lambda: st.session_state.update({"texto_expresion": ""}), use_container_width=True)

    # Fila 4: Agrupación
    c13, c14, c15, c16 = st.columns(4)
    with c13: st.button("(", on_click=insertar_simbolo, args=("(",), use_container_width=True)
    with c14: st.button(")", on_click=insertar_simbolo, args=(")",), use_container_width=True)
    with c15: st.button("[", on_click=insertar_simbolo, args=("[",), use_container_width=True)
    with c16: st.button("]", on_click=insertar_simbolo, args=("]",), use_container_width=True)

    # Mostramos lo que se va armando
    st.session_state.texto_expresion = st.text_area("Expresión armada:", value=st.session_state.texto_expresion)

# --- BOTÓN DE CÁLCULO ---
if st.button("Calcular", key="btn_principal"):
    # IMPORTANTE: Ahora recibimos 3 valores de tu motor corregido
    resultado_motor = generar_y_descargar(st.session_state.texto_expresion)
    
    # Manejo de seguridad por si el motor devuelve 2 o 3 valores
    if len(resultado_motor) == 3:
        df, error, tipo = resultado_motor
    else:
        df, error = resultado_motor
        tipo = None

    if error:
        st.error(error)
    else:
        st.success("Tabla generada con éxito")
        if tipo:
            st.info(f"Clasificación: **{tipo}**")
        st.table(df)
        
        try:
            with open("tabla_verdad.pdf", "rb") as f:
                st.download_button(
                    label="📄 Descargar Reporte PDF",
                    data=f,
                    file_name="Reporte_Tabla_Verdad.pdf",
                    mime="application/pdf"
                )
        except FileNotFoundError:
            st.error("No se encontró el PDF. El motor no generó el archivo.")
