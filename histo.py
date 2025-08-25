import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Usar backend no interactivo
import matplotlib.pyplot as plt

def analizar_histograma_frecuencia(ruta_imagen):
    """
    Analiza el histograma de frecuencia de una imagen multiespectral
    y muestra la distribución de niveles de gris.
    """
    # Cargar imagen en escala de grises
    img = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        print(f"Error: No se pudo cargar la imagen en la ruta: {ruta_imagen}")
        return
    
    # Calcular histograma
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    
    # Calcular estadísticas básicas
    intensidad_media = np.mean(img)
    intensidad_std = np.std(img)
    intensidad_min = np.min(img)
    intensidad_max = np.max(img)
    
    # Mostrar resultados
    plt.figure(figsize=(15, 5))
    
    # Imagen original
    plt.subplot(1, 3, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Imagen Original')
    plt.axis('off')
    
    # Histograma de frecuencia
    plt.subplot(1, 3, 2)
    plt.plot(hist, color='blue', linewidth=2)
    plt.title('Histograma de Frecuencia')
    plt.xlabel('Nivel de Gris')
    plt.ylabel('Frecuencia')
    plt.grid(True, alpha=0.3)
    
    # Estadísticas de la imagen
    plt.subplot(1, 3, 3)
    plt.axis('off')
    stats_text = f"""
    Estadísticas de la Imagen:
    
    Intensidad Media: {intensidad_media:.2f}
    Desviación Estándar: {intensidad_std:.2f}
    Intensidad Mínima: {intensidad_min}
    Intensidad Máxima: {intensidad_max}
    Rango Dinámico: {intensidad_max - intensidad_min}
    """
    plt.text(0.1, 0.5, stats_text, fontsize=12, 
             verticalalignment='center', fontfamily='monospace')
    
    plt.tight_layout()
    plt.savefig('./captures/analisis_histograma.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Análisis de histograma guardado en: ./captures/analisis_histograma.png")
    
    return {
        'histograma': hist,
        'estadisticas': {
            'media': intensidad_media,
            'std': intensidad_std,
            'min': intensidad_min,
            'max': intensidad_max,
            'rango': intensidad_max - intensidad_min
        }
    }


def aplicar_ecualizacion_histograma(ruta_imagen):
    """
    Aplica ecualización de histograma a una imagen multiespectral
    y compara los resultados antes y después del procesamiento.
    """
    # Cargar imagen en escala de grises
    img = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        print(f"Error: No se pudo cargar la imagen en la ruta: {ruta_imagen}")
        return
    
    # Aplicar ecualización de histograma
    img_ecualizada = cv2.equalizeHist(img)
    
    # Calcular histogramas para ambas imágenes
    hist_original = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist_ecualizado = cv2.calcHist([img_ecualizada], [0], None, [256], [0, 256])
    
    # Calcular métricas de mejora
    contraste_original = np.std(img)
    contraste_ecualizado = np.std(img_ecualizada)
    mejora_contraste = ((contraste_ecualizado - contraste_original) / contraste_original) * 100
    
    # Mostrar resultados comparativos
    plt.figure(figsize=(15, 10))
    
    # Imagen original
    plt.subplot(2, 3, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Imagen Original')
    plt.axis('off')
    
    # Histograma original
    plt.subplot(2, 3, 2)
    plt.plot(hist_original, color='blue', linewidth=2)
    plt.title('Histograma Original')
    plt.xlabel('Nivel de Gris')
    plt.ylabel('Frecuencia')
    plt.grid(True, alpha=0.3)
    
    # Imagen ecualizada
    plt.subplot(2, 3, 4)
    plt.imshow(img, cmap='gray')
    plt.title('Imagen Ecualizada')
    plt.axis('off')
    
    # Histograma ecualizado
    plt.subplot(2, 3, 5)
    plt.plot(hist_ecualizado, color='red', linewidth=2)
    plt.title('Histograma Ecualizado')
    plt.xlabel('Nivel de Gris')
    plt.ylabel('Frecuencia')
    plt.grid(True, alpha=0.3)
    
    # Métricas de mejora
    plt.subplot(2, 3, 3)
    plt.axis('off')
    metrics_text = f"""
    Métricas de Mejora:
    
    Contraste Original: {contraste_original:.2f}
    Contraste Ecualizado: {contraste_ecualizado:.2f}
    Mejora del Contraste: {mejora_contraste:.1f}%
    
    Rango Dinámico Original: {np.max(img) - np.min(img)}
    Rango Dinámico Ecualizado: {np.max(img_ecualizada) - np.min(img_ecualizada)}
    """
    plt.text(0.1, 0.5, metrics_text, fontsize=11, 
             verticalalignment='center', fontfamily='monospace')
    
    plt.tight_layout()
    plt.savefig('./captures/ecualizacion_histograma.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Ecualización de histograma guardada en: ./captures/ecualizacion_histograma.png")
    
    return {
        'imagen_original': img,
        'imagen_ecualizada': img_ecualizada,
        'histograma_original': hist_original,
        'histograma_ecualizado': hist_ecualizado,
        'metricas': {
            'contraste_original': contraste_original,
            'contraste_ecualizado': contraste_ecualizado,
            'mejora_contraste': mejora_contraste
        }
    }


def aplicar_clahe(ruta_imagen, clip_limit=2.0, tile_grid_size=(8,8)):
    """
    Aplica CLAHE (Contrast Limited Adaptive Histogram Equalization)
    a una imagen multiespectral.
    """
    # Cargar imagen en escala de grises
    img = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        print(f"Error: No se pudo cargar la imagen en la ruta: {ruta_imagen}")
        return
    
    # Crear objeto CLAHE
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    
    # Aplicar CLAHE
    img_clahe = clahe.apply(img)
    
    # Calcular histogramas
    hist_original = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist_clahe = cv2.calcHist([img_clahe], [0], None, [256], [0, 256])
    
    # Mostrar comparación
    plt.figure(figsize=(15, 5))
    
    # Imagen original
    plt.subplot(1, 3, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Imagen Original')
    plt.axis('off')
    
    # Imagen con CLAHE
    plt.subplot(1, 3, 2)
    plt.imshow(img_clahe, cmap='gray')
    plt.title('Imagen con CLAHE')
    plt.axis('off')
    
    # Comparación de histogramas
    plt.subplot(1, 3, 3)
    plt.plot(hist_original, color='blue', linewidth=2, label='Original')
    plt.plot(hist_clahe, color='red', linewidth=2, label='CLAHE')
    plt.title('Comparación de Histogramas')
    plt.xlabel('Nivel de Gris')
    plt.ylabel('Frecuencia')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('./captures/comparacion_clahe.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Comparación CLAHE guardada en: ./captures/comparacion_clahe.png")
    
    return {
        'imagen_original': img,
        'imagen_clahe': img_clahe,
        'histograma_original': hist_original,
        'histograma_clahe': hist_clahe
    }


# Código principal
if __name__ == "__main__":
    imgRoute = "./captures/imagen.jpg"
    print("=== ANÁLISIS DE HISTOGRAMAS DE IMÁGENES ===")
    print(f"Analizando imagen: {imgRoute}")
    print()
    
    # Ejecutar las 3 funciones
    print("1. Analizando histograma de frecuencia...")
    analizar_histograma_frecuencia(imgRoute)
    print()
    
    print("2. Aplicando ecualización de histograma...")
    aplicar_ecualizacion_histograma(imgRoute)
    print()
    
    print("3. Aplicando CLAHE...")
    aplicar_clahe(imgRoute)
    print()
    
    print("¡Análisis completado! Revisa los archivos generados en ./captures/")




