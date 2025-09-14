# Actividad 6: Análisis y Mejora de Imágenes con TensorFlow

Este proyecto implementa un sistema completo de análisis y mejora de imágenes usando TensorFlow, que incluye:

## 🚀 Características

- **Carga de imágenes**: Soporte para múltiples formatos (JPG, PNG, BMP, TIFF)
- **Reducción de ruido**: Filtro Gaussiano usando TensorFlow I/O
- **Mejora de contraste**: Ecualización de histograma con OpenCV
- **Superresolución**: Modelo ESRGAN pre-entrenado desde TensorFlow Hub
- **Visualización**: Mostrar cada paso del proceso
- **Guardado automático**: Exportar todas las imágenes procesadas

## 📋 Requisitos

```bash
pip install -r requirements.txt
```

### Dependencias principales:
- `tensorflow>=2.13.0`
- `tensorflow-hub>=0.14.0`
- `tensorflow-io>=0.33.0`
- `opencv-python>=4.8.0`
- `Pillow>=10.0.0`
- `matplotlib>=3.7.0`
- `numpy>=1.24.0`

## 🖼️ Uso

### Uso básico:
```python
from image_analysis import ImageAnalyzer

# Crear analizador
analyzer = ImageAnalyzer()

# Procesar imagen
results = analyzer.process_image("tu_imagen.jpg")

# Guardar resultados
analyzer.save_results(results)
```

### Ejecutar desde línea de comandos:
```bash
cd act6
python image_analysis.py
```

## 📁 Estructura de archivos

```
act6/
├── image_analysis.py      # Archivo principal con clase ImageAnalyzer
├── simple_example.py      # Ejemplo simplificado
├── output/                # Directorio de salida (se crea automáticamente)
│   ├── 01_original.jpg
│   ├── 02_denoised.jpg
│   ├── 03_enhanced.jpg
│   └── 04_super_resolution.jpg
└── README.md              # Este archivo
```

## 🔧 Proceso de mejora de imágenes

1. **Carga**: Leer imagen de baja resolución
2. **Reducción de ruido**: Aplicar filtro Gaussiano
3. **Mejora de contraste**: Ecualización de histograma
4. **Superresolución**: Modelo ESRGAN para aumentar resolución
5. **Guardado**: Exportar todas las versiones procesadas

## ⚠️ Notas importantes

- **Conexión a internet**: Requerida para descargar el modelo de superresolución
- **Memoria**: El modelo ESRGAN puede requerir bastante RAM
- **Formatos soportados**: JPG, JPEG, PNG, BMP, TIFF
- **Tamaño de imagen**: Recomendado máximo 1024x1024 píxeles para mejor rendimiento

## 🐛 Solución de problemas

### Error de conexión:
```
Error al cargar modelo de superresolución: ...
```
**Solución**: Verificar conexión a internet y firewall

### Error de memoria:
```
ResourceExhaustedError: ...
```
**Solución**: Reducir tamaño de imagen o usar imagen más pequeña

### Archivo no encontrado:
```
FileNotFoundError: ...
```
**Solución**: Verificar que la imagen existe en el directorio correcto

## 📊 Resultados esperados

El procesamiento generará 4 imágenes:
- **Original**: Imagen de entrada sin modificar
- **Denoised**: Con ruido reducido usando filtro Gaussiano
- **Enhanced**: Con contraste mejorado por ecualización
- **Super Resolution**: Con resolución aumentada usando IA

## 🔬 Detalles técnicos

- **Filtro Gaussiano**: Kernel 3x3, sigma=1.0
- **Modelo ESRGAN**: Pre-entrenado en TensorFlow Hub
- **Ecualización**: Algoritmo CLAHE de OpenCV
- **Normalización**: Valores de píxel entre 0-1 para TensorFlow
