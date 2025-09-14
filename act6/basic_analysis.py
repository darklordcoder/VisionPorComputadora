#!/usr/bin/env python3
"""
Ejemplo básico para Actividad 6 (Solo OpenCV - Sin TensorFlow Hub)
Versión que funciona completamente sin problemas de compatibilidad
"""

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os

def basic_image_analysis(image_path):
    """
    Análisis básico de imagen usando solo OpenCV (sin TensorFlow Hub)
    
    Args:
        image_path (str): Ruta al archivo de imagen
    """
    
    print("🚀 Iniciando análisis básico de imagen...")
    
    try:
        # Paso 1: Cargar imagen
        print("📸 Cargando imagen...")
        low_res_image = Image.open(image_path)
        
        plt.figure(figsize=(15, 5))
        
        # Mostrar imagen original
        plt.subplot(1, 4, 1)
        plt.imshow(low_res_image)
        plt.title('Original')
        plt.axis('off')
        
        # Paso 2: Reducir ruido con OpenCV
        print("🔧 Reduciendo ruido con filtro Gaussiano...")
        image_array = np.array(low_res_image)
        denoised_array = cv2.GaussianBlur(image_array, (5, 5), 1.0)
        
        plt.subplot(1, 4, 2)
        plt.imshow(denoised_array)
        plt.title('Sin Ruido')
        plt.axis('off')
        
        # Paso 3: Mejorar contraste con CLAHE
        print("🎨 Mejorando contraste con CLAHE...")
        
        # Convertir a LAB para mejor procesamiento
        lab = cv2.cvtColor(denoised_array, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        
        # Aplicar CLAHE al canal L
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Recombinar canales
        enhanced_lab = cv2.merge([l, a, b])
        enhanced_rgb = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
        
        plt.subplot(1, 4, 3)
        plt.imshow(enhanced_rgb)
        plt.title('Contraste Mejorado')
        plt.axis('off')
        
        # Paso 4: Aplicar filtro de nitidez
        print("🔍 Aplicando filtro de nitidez...")
        
        # Crear kernel de nitidez
        kernel_sharpen = np.array([[-1,-1,-1],
                                   [-1, 9,-1],
                                   [-1,-1,-1]])
        
        # Aplicar filtro de nitidez
        sharpened = cv2.filter2D(enhanced_rgb, -1, kernel_sharpen)
        sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
        
        plt.subplot(1, 4, 4)
        plt.imshow(sharpened)
        plt.title('Imagen Mejorada')
        plt.axis('off')
        
        plt.tight_layout()
        plt.show()
        
        print("✅ Análisis completado exitosamente")
        
        # Guardar resultados
        print("💾 Guardando resultados...")
        os.makedirs("output", exist_ok=True)
        
        low_res_image.save("output/01_original.jpg")
        Image.fromarray(denoised_array).save("output/02_denoised.jpg")
        Image.fromarray(enhanced_rgb).save("output/03_enhanced.jpg")
        Image.fromarray(sharpened).save("output/04_improved.jpg")
        
        print("✅ Resultados guardados en carpeta 'output':")
        print("   - 01_original.jpg")
        print("   - 02_denoised.jpg") 
        print("   - 03_enhanced.jpg")
        print("   - 04_improved.jpg")
        
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {image_path}")
        print("📁 Archivos disponibles en el directorio:")
        
        # Listar archivos de imagen disponibles
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        available_images = []
        
        for file in os.listdir('.'):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                available_images.append(file)
        
        if available_images:
            print("🖼️  Imágenes disponibles:")
            for img in available_images:
                print(f"   - {img}")
        else:
            print("   No se encontraron archivos de imagen en el directorio actual")
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Cambiar por la ruta de tu imagen
    image_path = "paisaje_urbano_baja_res.jpg"
    basic_image_analysis(image_path)
