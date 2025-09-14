#!/usr/bin/env python3
"""
Ejemplo simplificado para Actividad 6 (Versión Compatible con DevContainer)
Versión que evita problemas con TensorFlow I/O usando OpenCV
"""

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2

def simple_image_analysis(image_path):
    """
    Análisis simple de imagen con los pasos básicos (sin TensorFlow I/O)
    
    Args:
        image_path (str): Ruta al archivo de imagen
    """
    
    print("🚀 Iniciando análisis simple de imagen...")
    
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
        print("🔧 Reduciendo ruido con OpenCV...")
        image_array = np.array(low_res_image)
        denoised_array = cv2.GaussianBlur(image_array, (5, 5), 1.0)
        
        plt.subplot(1, 4, 2)
        plt.imshow(denoised_array)
        plt.title('Sin Ruido (OpenCV)')
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
        plt.title('Contraste Mejorado (CLAHE)')
        plt.axis('off')
        
        # Paso 4: Superresolución (opcional)
        print("⚡ Intentando aplicar superresolución...")
        try:
            import tensorflow as tf
            import tensorflow_hub as hub
            
            # Cargar modelo
            model_url = "https://tfhub.dev/captain-pool/esrgan-tf2/1"
            super_res_model = hub.load(model_url)
            
            # Aplicar superresolución
            input_tensor = tf.convert_to_tensor(enhanced_rgb, dtype=tf.float32) / 255.0
            input_tensor = tf.expand_dims(input_tensor, axis=0)
            super_res_tensor = super_res_model(input_tensor)
            super_res_tensor = tf.squeeze(super_res_tensor, axis=0)
            
            plt.subplot(1, 4, 4)
            plt.imshow(super_res_tensor)
            plt.title('Superresolución')
            plt.axis('off')
            
            print("✅ Superresolución aplicada exitosamente")
            
        except Exception as e:
            print(f"⚠️  Superresolución no disponible: {e}")
            plt.subplot(1, 4, 4)
            plt.imshow(enhanced_rgb)
            plt.title('Sin Superresolución')
            plt.axis('off')
        
        plt.tight_layout()
        plt.show()
        
        print("✅ Análisis completado exitosamente")
        
        # Guardar resultados
        print("💾 Guardando resultados...")
        import os
        os.makedirs("output", exist_ok=True)
        
        low_res_image.save("output/01_original.jpg")
        Image.fromarray(denoised_array).save("output/02_denoised.jpg")
        Image.fromarray(enhanced_rgb).save("output/03_enhanced.jpg")
        
        print("✅ Resultados guardados en carpeta 'output'")
        
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {image_path}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Cambiar por la ruta de tu imagen
    image_path = "paisaje_urbano_baja_res.jpg"
    simple_image_analysis(image_path)
