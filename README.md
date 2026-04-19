# 📊 Calculadora de Tablas de Verdad - Proyecto UG

Este proyecto es una herramienta interactiva desarrollada en Python utilizando **Streamlit**. Permite evaluar expresiones de lógica proposicional de forma dinámica, generando tablas de verdad binarias (0 y 1) y permitiendo la exportación de los resultados a un reporte profesional en PDF.

## 🚀 Características
- **Interfaz Dual:** Entrada mediante teclado o botonera virtual interactiva.
- **Motor Lógico Robusto:** Soporta variables `p`, `q`, `r` y operadores complejos.
- **Clasificación Automática:** Determina si la expresión es una **Tautología**, **Contradicción** o **Contingencia**.
- **Reporte PDF:** Descarga los resultados con limpieza automática de caracteres especiales.

​"Se implementó un motor de detección de sub-expresiones mediante expresiones regulares para desglosar la tabla de verdad paso a paso, mejorando la trazabilidad del resultado final."

## 🛠️ Operadores Soportados
| Operador | Símbolo |
| :--- | :--- |
| Negación | `~` o `not` |
| Conjunción (AND) | `^` o `and` |
| Disyunción (OR) | `v` o `or` |
| Condicional (IF) | `->` |
| Bicondicional (IFF) | `<->` |
| XOR | `xor` |
| NAND / NOR | `nand` / `nor` |

## 📦 Instalación y Uso Local

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Kavstronik/calculadora-tabla-verdad
   cd Hola_Mundo


## 📦 Instalación y Uso Local

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt

Ejecutar la Aplicación
​Una vez instaladas las dependencias, inicia el servidor de Streamlit con el siguiente comando:
streamlit run app.py


Reflexión Técnica
​Durante el desarrollo, el principal desafío fue la exportación a PDF. La librería fpdf no reconoce caracteres Unicode (como las flechas -> o el símbolo ¬). Para solucionarlo, implementé una función de limpieza en truth_table.py que traduce estos símbolos a formato ASCII antes de generar el documento, evitando que la aplicación colapse.


​🎓 Autor
​Nombre: Steeven Almeida Velasco (Kavs)
​Institución: Universidad de Guayaquil
​Materia: Ingeniería de Software