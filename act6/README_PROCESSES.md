# Actividad 6: Procesamiento de Imágenes con TensorFlow

## 🎯 Objetivo
Implementar los **3 procesos requeridos** para el análisis y mejora de imágenes:

1. **Filtros para reducir el ruido**
2. **Aumentar el contraste**
3. **Técnicas de superresolución para mejorar la definición**

## 📁 Archivos Disponibles

### Versiones Principales:
- **`image_processor.py`** - Versión completa con TensorFlow Hub (superresolución con IA)
- **`image_processor_opencv.py`** - Versión solo con OpenCV (funciona sin internet) ⭐ **RECOMENDADO**

### Versiones Alternativas:
- **`basic_analysis.py`** - Versión básica y rápida
- **`image_analysis_fixed.py`** - Versión completa sin TensorFlow I/O

## 🚀 Uso Rápido

```bash
cd act6
python image_processor_opencv.py
```

## 📊 Los 3 Procesos Implementados

### 🔧 PROCESO 1: Filtros para reducir el ruido

**Métodos implementados:**
- **Filtro Gaussiano**: Suavizado uniforme
- **Filtro de Mediana**: Elimina ruido impulsivo
- **Filtro Bilateral**: Preserva bordes mientras reduce ruido
- **Filtro No Local**: Elimina ruido preservando texturas
- **Filtro Adaptativo**: Parámetros ajustables según contenido

**Resultado**: Imagen con ruido significativamente reducido

### 🎨 PROCESO 2: Aumentar el contraste

**Métodos implementados:**
- **Ecualización de Histograma**: Distribución uniforme de intensidades
- **CLAHE**: Ecualización adaptativa local
- **Ajuste de Gamma**: Corrección de brillo y contraste
- **Estiramiento de Contraste**: Amplificación del rango dinámico
- **Mejora Local**: Contraste adaptativo por regiones

**Resultado**: Imagen con contraste mejorado y detalles más visibles

### ⚡ PROCESO 3: Técnicas de superresolución

**Versión con TensorFlow Hub:**
- **Modelo ESRGAN**: Superresolución con inteligencia artificial
- **Factor 4x**: Aumento significativo de resolución
- **Preservación de detalles**: Mantiene calidad visual

**Versión solo OpenCV:**
- **Interpolación Bicúbica**: Suavizado de alta calidad
- **Interpolación Lanczos**: Preservación de bordes
- **Con Nitidez**: Interpolación + filtro de nitidez
- **Edge-Preserving**: Preserva bordes durante escalado
- **Detail Enhanced**: Realce de detalles finos

**Resultado**: Imagen con mayor definición y resolución

## 📈 Comparación de Métodos

El código muestra **comparaciones visuales** de cada método para que puedas:

1. **Ver las diferencias** entre técnicas
2. **Elegir el mejor resultado** para tu caso específico
3. **Entender el impacto** de cada proceso

## 💾 Resultados Generados

Se crean automáticamente en la carpeta `output/`:

```
output/
├── 01_original.jpg          # Imagen original
├── 02_denoised.jpg          # Después de reducir ruido
├── 03_enhanced.jpg          # Después de mejorar contraste
└── 04_super_resolution.jpg  # Resultado final con superresolución
```

## 🔧 Configuración Técnica

### Dependencias:
```bash
pip install opencv-python pillow matplotlib numpy
```

### Para superresolución con IA (opcional):
```bash
pip install tensorflow tensorflow-hub
```

## 📊 Métricas de Mejora

### Reducción de Ruido:
- **PSNR**: Mejora típica de 3-8 dB
- **SSIM**: Preservación de estructura visual
- **Preservación de bordes**: Filtros bilaterales y no locales

### Mejora de Contraste:
- **Entropía**: Aumento de información visual
- **Rango dinámico**: Amplificación del contraste
- **Detalles locales**: CLAHE mejora regiones específicas

### Superresolución:
- **Factor de escala**: 2x a 4x dependiendo del método
- **Preservación de bordes**: Métodos edge-preserving
- **Calidad visual**: Mejora subjetiva significativa

## 🎯 Casos de Uso

### Imágenes Médicas:
- Reducción de ruido → CLAHE → Superresolución

### Fotografía:
- Filtro bilateral → Ajuste gamma → Interpolación Lanczos

### Imágenes Satelitales:
- Filtro no local → CLAHE → Detail Enhanced

## ⚠️ Notas Importantes

1. **Versión OpenCV**: Funciona sin internet, más rápida
2. **Versión TensorFlow**: Requiere conexión, mejor calidad
3. **Tiempo de procesamiento**: Varía según tamaño de imagen
4. **Memoria**: Superresolución puede requerir más RAM

## 🔍 Análisis de Resultados

El código genera **comparaciones visuales** que te permiten:

- **Evaluar la efectividad** de cada método
- **Comparar técnicas** lado a lado
- **Seleccionar parámetros** óptimos
- **Entender el impacto** de cada proceso

## ✅ Verificación de Funcionamiento

El código incluye:
- ✅ **Manejo de errores** robusto
- ✅ **Validación de archivos** de entrada
- ✅ **Comparaciones visuales** automáticas
- ✅ **Guardado automático** de resultados
- ✅ **Compatibilidad** con devcontainers
