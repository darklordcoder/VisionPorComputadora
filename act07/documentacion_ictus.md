# 🏥 Sistema de Detección de ICTUS por Asimetría Facial

## 📋 Descripción del Sistema

Este sistema utiliza análisis de asimetría facial para detectar posibles signos de ictus (accidente cerebrovascular). La asimetría facial es uno de los signos más reconocibles del ictus y puede ser detectada mediante análisis computacional de imágenes.

## ⚠️ IMPORTANTE - DESCARGO DE RESPONSABILIDAD

**Este sistema es una herramienta de apoyo diagnóstico. NO reemplaza la evaluación médica profesional.**

- En caso de sospecha de ICTUS, buscar atención médica inmediata
- Los resultados deben ser interpretados por profesionales médicos
- Este sistema es para fines de investigación y apoyo diagnóstico únicamente

## 🎯 Criterios de Evaluación

### Umbrales de Riesgo
- **BAJO**: Diferencia promedio < 15.0
- **MODERADO**: Diferencia promedio 15.0 - 25.0
- **ALTO**: Diferencia promedio > 25.0 o porcentaje de asimetría > 20%

### Regiones Analizadas
1. **Ojos**: Región superior del rostro (20%-40% de altura)
2. **Cejas**: Región superior (10%-30% de altura)
3. **Boca**: Región inferior (60%-80% de altura)

## 📊 Métricas Generadas

### Métricas Generales
- **Diferencia promedio**: Valor promedio de asimetría en todo el rostro
- **Diferencia máxima**: Valor más alto de asimetría detectado
- **Diferencia de intensidad**: Diferencia entre mitades izquierda y derecha
- **Porcentaje de área asimétrica**: Porcentaje del rostro con alta asimetría

### Análisis por Regiones
- **Asimetría en ojos**: Valor específico para la región ocular
- **Asimetría en boca**: Valor específico para la región bucal
- **Asimetría en cejas**: Valor específico para la región de cejas

## 🖼️ Imágenes Generadas

### 1. `rostro_original.jpg`
- Rostro original con puntos rojos marcando áreas de alta asimetría
- Línea blanca central mostrando el eje de simetría
- Identificación visual de áreas problemáticas

### 2. `mapa_diferencias.jpg`
- Mapa de calor de diferencias
- Colores: Azul (baja diferencia) → Rojo (alta diferencia)
- Patrones de asimetría en toda la cara

### 3. `analisis_asimetria.jpg`
- Comparación lado a lado del rostro original y mapa de calor
- Vista completa para análisis visual

## 🚨 Sistema de Alertas

### Alerta ACTIVADA cuando:
- Diferencia promedio > 25.0
- O porcentaje de asimetría > 20%

### Acciones Recomendadas:
- **ALERTA ACTIVADA**: Buscar atención médica inmediata
- **SIN ALERTA**: Continuar monitoreo según protocolo médico

## 🔬 Base Científica

### Signos de ICTUS Evaluados:
1. **Asimetría facial**: Parálisis o debilidad de un lado del rostro
2. **Drooping facial**: Caída de características faciales
3. **Asimetría en sonrisa**: Dificultad para sonreír simétricamente
4. **Asimetría en ojos**: Diferencia en apertura o posición de ojos

### Literatura Médica:
- Los umbrales están basados en estudios de detección de ictus
- El análisis por regiones sigue protocolos médicos establecidos
- La detección temprana es crucial para el tratamiento del ictus

## 📱 Uso del Sistema

### Para Profesionales Médicos:
1. Cargar imagen del paciente (`imagen_paciente.jpg`)
2. Ejecutar el análisis
3. Revisar métricas y alertas
4. Analizar imágenes generadas
5. Integrar resultados en evaluación clínica

### Para Investigación:
1. Documentar casos con imágenes
2. Comparar resultados con diagnósticos clínicos
3. Refinar umbrales según población específica
4. Validar sistema con casos conocidos

## 🔧 Configuración Técnica

### Requisitos:
- Python 3.x
- OpenCV
- NumPy
- Matplotlib

### Parámetros Ajustables:
- Umbrales de riesgo
- Regiones de análisis
- Sensibilidad de detección
- Criterios de alerta

## 📞 Contacto de Emergencia

**En caso de sospecha de ICTUS:**
- Llamar servicios de emergencia inmediatamente
- Tiempo es crítico para el tratamiento
- No esperar confirmación del sistema

## 📚 Referencias

- Protocolos de detección de ictus
- Estudios de asimetría facial en neurología
- Guías clínicas de accidente cerebrovascular
- Investigación en detección temprana de ictus

---

**Versión**: 1.0  
**Fecha**: Septiembre 2024  
**Propósito**: Apoyo diagnóstico para detección de ictus
