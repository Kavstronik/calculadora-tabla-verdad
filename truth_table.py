import itertools
import re

def generar_tabla(expresion):
    """
    Lógica para extraer variables, generar combinaciones 2^n y evaluar
    la expresión devolviendo resultados en formato 0 y 1.
    """
    # 1. [span_1](start_span)Extraer variables (A, B, C...) automáticamente[span_1](end_span)
    variables = sorted(list(set(re.findall(r'\b[A-Z]\b', expresion))))
    
    if not variables:
        return None, "No se detectaron variables (usa letras mayúsculas como A, B...)"

    # 2. [span_2](start_span)Generar todas las combinaciones posibles (2^n)[span_2](end_span)
    n = len(variables)
    combinaciones = list(itertools.product([0, 1], repeat=n))
    
    tabla_resultados = []
    
    # 3. [span_3](start_span)Evaluar la expresión de forma segura[span_3](end_span)
    for combo in combinaciones:
        # Mapeamos cada variable a su valor actual (0 o 1)
        valores = dict(zip(variables, combo))
        
        # Ajustamos la expresión para que Python la entienda (AND -> and, etc.)
        exp_python = expresion.upper()
        exp_python = exp_python.replace('AND', ' and ')
        exp_python = exp_python.replace('OR', ' or ')
        exp_python = exp_python.replace('NOT', ' not ')
        exp_python = exp_python.replace('XOR', ' ^ ')
        
        try:
            # [span_4](start_span)Evaluación segura restringiendo el acceso a funciones del sistema[span_4](end_span)
            resultado = eval(exp_python, {"__builtins__": None}, valores)
            # [span_5](start_span)Convertimos el resultado booleano a 0 o 1[span_5](end_span)
            fila = list(combo) + [1 if resultado else 0]
            tabla_resultados.append(fila)
        except Exception as e:
            return None, f"Error de sintaxis: {str(e)}"
            
    return variables, tabla_resultados
