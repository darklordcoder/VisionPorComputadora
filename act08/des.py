import re

def simular_extraccion_datos(texto_documento: str) -> dict:
    """
    Simula la extracción de datos de un texto usando expresiones regulares.
    En un sistema real, este texto provendría de un motor de OCR.
    
    Args:
        texto_documento: Una cadena de texto que contiene la información del solicitante.

    Returns:
        Un diccionario con los datos estructurados.
    """
    datos_extraidos = {}
    
    # Expresión regular para encontrar el ingreso anual (ej: "Ingreso Anual: $55,000")
    match_ingreso = re.search(r"Ingreso Anual: \$([\d,]+)", texto_documento, re.IGNORECASE)
    if match_ingreso:
        # Convierte el número a un entero, eliminando comas
        ingreso_str = match_ingreso.group(1).replace(",", "")
        datos_extraidos['ingreso_anual'] = int(ingreso_str)

    # Expresión regular para encontrar la antigüedad laboral (ej: "Antigüedad: 3 años")
    match_antiguedad = re.search(r"Antigüedad: (\d+)\s+años", texto_documento, re.IGNORECASE)
    if match_antiguedad:
        datos_extraidos['antiguedad_laboral'] = int(match_antiguedad.group(1))
        
    return datos_extraidos

def motor_de_reglas(datos_solicitante: dict) -> tuple[str, str]:
    """
    Aplica un conjunto simple de reglas de negocio a los datos extraídos.
    En un sistema real, estas reglas se cargarían desde una base de conocimiento
    generada a partir de textos legales (Law as Code).

    Args:
        datos_solicitante: Un diccionario con los datos del solicitante.

    Returns:
        Una tupla con la decisión y el motivo.
    """
    # Reglas de negocio codificadas
    INGRESO_MINIMO = 30000
    ANTIGUEDAD_MINIMA = 2

    ingreso = datos_solicitante.get('ingreso_anual')
    antiguedad = datos_solicitante.get('antiguedad_laboral')

    if not all([ingreso, antiguedad]):
        return ("Rechazado", "Faltan datos clave en la solicitud.")

    if ingreso < INGRESO_MINIMO:
        motivo = f"Ingreso de ${ingreso} es menor al mínimo requerido de ${INGRESO_MINIMO}."
        return ("Rechazado", motivo)
    
    if antiguedad < ANTIGUEDAD_MINIMA:
        motivo = f"Antigüedad de {antiguedad} años es menor a la mínima requerida de {ANTIGUEDAD_MINIMA} años."
        return ("Rechazado", motivo)

    return ("Aprobado", "El solicitante cumple con los criterios de ingreso y antigüedad.")

# --- Simulación del Proceso ---

# 1. Texto de un documento de solicitud (simula la salida del OCR)
texto_solicitud_1 = """
Nombre: Juan Pérez
ID: 12345678
Dirección: Calle Falsa 123
---
Datos Financieros
Ingreso Anual: $55,000
Antigüedad: 5 años
---
"""

texto_solicitud_2 = """
Nombre: Maria Lopez
ID: 87654321
---
Datos Financieros
Ingreso Anual: $28,500
Antigüedad: 4 años
---
"""

# 2. Procesar la primera solicitud
print("Procesando Solicitud 1...")
datos_extraidos_1 = simular_extraccion_datos(texto_solicitud_1)
print(f"Datos extraídos: {datos_extraidos_1}")
decision_1, motivo_1 = motor_de_reglas(datos_extraidos_1)
print(f"Decisión: {decision_1}\nMotivo: {motivo_1}\n")

# 3. Procesar la segunda solicitud
print("Procesando Solicitud 2...")
datos_extraidos_2 = simular_extraccion_datos(texto_solicitud_2)
print(f"Datos extraídos: {datos_extraidos_2}")
decision_2, motivo_2 = motor_de_reglas(datos_extraidos_2)
print(f"Decisión: {decision_2}\nMotivo: {motivo_2}")
