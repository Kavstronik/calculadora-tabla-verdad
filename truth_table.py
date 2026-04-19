import pandas as pd
import itertools
import re
from fpdf import FPDF

def normalizar_letras(texto):
    mapeo = {
        '𝒑': 'p', '𝒒': 'q', '𝒓': 'r', '𝑝': 'p', '𝑞': 'q', '𝑟': 'r',
        '𝐩': 'p', '𝐪': 'q', '𝐫': 'r', '𝑷': 'p', '𝑸': 'q', '𝑹': 'r',
        'P': 'p', 'Q': 'q', 'R': 'r',
        '⇒': '->', '⇔': '<->', '≡': '<->',
        ' V ': ' 1 ', ' F ': ' 0 ', ' T ': ' 1 ',
        'v': ' or ', '^': ' and ', '¬': ' not ', '~': ' not '
    }
    for rara, normal in mapeo.items():
        texto = texto.replace(rara, normal)
    
    simbolos = ['∧', '∨', '→', '↔', '⊕', '↑', '↓', '!', '==', '!=', '(', ')', '[', ']', '->', '<->']
    for s in simbolos:
        texto = texto.replace(s, f" {s} ")
    return texto

def motor_traductor_robusto(t):
    # Asegurar que no haya basura de símbolos antes de traducir
    t = t.replace('∧', ' and ').replace('^', ' and ')
    t = t.replace('∨', ' or ').replace(' v ', ' or ')
    t = t.replace('¬', ' not ').replace('~', ' not ')
    t = t.replace('↑', ' nand ').replace('|', ' nand ')
    t = t.replace('↓', ' nor ')
    t = t.replace('⊕', ' xor ').replace('⊻', ' xor ')
    
    while 'xor' in t: t = re.sub(r'(\(.*?\)|\bnot\s+\w+|\b\w+)\s*xor\s*(\(.*?\)|\bnot\s+\w+|\b\w+)', r'(\1 != \2)', t)
    while 'nand' in t: t = re.sub(r'(\(.*?\)|\bnot\s+\w+|\b\w+)\s*not\s*(\(.*?\)|\bnot\s+\w+|\b\w+)', r'(not (\1 and \2))', t)
    while 'nor' in t: t = re.sub(r'(\(.*?\)|\bnot\s+\w+|\b\w+)\s*nor\s*(\(.*?\)|\bnot\s+\w+|\b\w+)', r'(not (\1 or \2))', t)
    while '↔' in t or '<->' in t or '⇔' in t:
        t = re.sub(r'(\(.*?\)|\bnot\s+\w+|\b\w+)\s*(↔|<->|⇔)\s*(\(.*?\)|\bnot\s+\w+|\b\w+)', r'(\1 == \3)', t)
    while '→' in t or '->' in t or '⇒' in t:
        t = re.sub(r'(\(.*?\)|\bnot\s+\w+|\b\w+)\s*(→|->|⇒)\s*(\(.*?\)|\bnot\s+\w+|\b\w+)', r'(not \1 or \3)', t)
    
    t = t.replace(' 1 ', ' True ').replace(' 0 ', ' False ')
    return " ".join(t.split())

def exportar_a_pdf(df, expresion, clasificacion, nombre_archivo="tabla_verdad.pdf"):
    def limpiar_para_pdf(txt):
        txt = str(txt)
        rep = {'→': '->', '↔': '<->', '¬': '~', '∧': '^', '∨': 'v', '[': '(', ']': ')'}
        for k, v in rep.items(): txt = txt.replace(k, v)
        return txt.encode('latin-1', 'replace').decode('latin-1')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Reporte de Tabla de Verdad - UG", ln=True, align='C')
    
    pdf.set_font("Arial", size=10)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Expresion: {limpiar_para_pdf(expresion)}", ln=True)
    pdf.cell(200, 10, txt=f"Clasificacion: {clasificacion}", ln=True)
    pdf.ln(5)

    # Tabla
    pdf.set_font("Arial", 'B', 8) # Un poco más pequeño para que entre el paso a paso
    col_width = 190 / len(df.columns)
    for col in df.columns:
        pdf.cell(col_width, 10, limpiar_para_pdf(col), border=1, align='C')
    pdf.ln()

    pdf.set_font("Arial", size=9)
    for _, row in df.iterrows():
        for val in row:
            pdf.cell(col_width, 10, str(val), border=1, align='C')
        pdf.ln()
    
    pdf.output(nombre_archivo)

def generar_y_descargar(expresion):
    t_normal = normalizar_letras(expresion)
    t_limpio = t_normal.lower().replace('[', '(').replace(']', ')')
    letras = sorted(list(set(re.findall(r'\b[pqr]\b', t_limpio))))
    
    if not letras:
        return None, "Error: No se detectaron variables p, q o r.", None

    # EXTRAER PASOS INTERMEDIOS (Lo nuevo)
    # Busca contenido dentro de paréntesis
    pasos_intermedios = re.findall(r'\(([^()]+)\)', t_limpio)
    # Quitamos duplicados y variables sueltas
    pasos_intermedios = [p for p in list(dict.fromkeys(pasos_intermedios)) if p not in letras]

    combinaciones = list(itertools.product([True, False], repeat=len(letras)))
    filas = []

    for combo in combinaciones:
        ctx = {l: v for l, v in zip(letras, combo)}
        ctx.update({'True': True, 'False': False})
        
        # 1. Variables principales
        fila = {l.upper(): (1 if v else 0) for l, v in zip(letras, combo)}
        
        # 2. EVALUAR PASOS INTERMEDIOS
        for paso in pasos_intermedios:
            t_paso = motor_traductor_robusto(paso)
            try:
                res_p = eval(t_paso, {"__builtins__": None}, ctx)
                fila[f"({paso.upper()})"] = 1 if bool(res_p) else 0
            except:
                fila[f"({paso.upper()})"] = "Err"

        # 3. EVALUAR RESULTADO FINAL
        t_final = motor_traductor_robusto(t_limpio)
        try:
            res_f = eval(t_final, {"__builtins__": None}, ctx)
            fila['RESULTADO'] = 1 if bool(res_f) else 0
        except:
            fila['RESULTADO'] = "Error"
            
        filas.append(fila)

    df = pd.DataFrame(filas)
    
    # Clasificación lógica
    resultados = df['RESULTADO'].unique()
    if len(resultados) == 1:
        tipo = "Tautología" if resultados[0] == 1 else "Contradicción"
    else:
        tipo = "Contingencia"
    
    try:
        exportar_a_pdf(df, expresion, tipo)
    except Exception as e:
        print(f"Error PDF: {e}")
    
    return df, None, tipo
