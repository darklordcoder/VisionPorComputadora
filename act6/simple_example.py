#!/usr/bin/env python3
"""
Ejemplo simplificado para Actividad 6
Versión básica del análisis de imágenes con TensorFlow
"""

from PIL import Image
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_io as tfio
import numpy as np
import cv2

def simple_image_analysis(image_path):
    """
    Análisis simple de imagen con los pasos básicos
    
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
        
        # Paso 2: Convertir a tensor y reducir ruido
        print("🔧 Reduciendo ruido...")
        low_res_tensor = tf.convert_to_tensor(np.array(low_res_image), dtype=tf.float32) / 255.0
        denoised_tensor = tfio.experimental.filter.gaussian(low_res_tensor, ksize=3, sigma=1.0)
        
        plt.subplot(1, 4, 2)
        plt.imshow(denoised_tensor)
        plt.title('Sin Ruido')
        plt.axis('off')
        
        # Paso 3: Mejorar contraste
        print("🎨 Mejorando contraste...")
        denoised_cv = np.array(denoised_tensor * 255, dtype='uint8')
        gray_cv = cv2.cvtColor(denoised_cv, cv2.COLOR_RGB2GRAY)
        equalized_cv = cv2.equalizeHist(gray_cv)
        equalized_rgb = cv2.cvtColor(equalized_cv, cv2.COLOR_GRAY2RGB)
        
        plt.subplot(1, 4, 3)
        plt.imshow(equalized_rgb)
        plt.title('Contraste Mejorado')
        plt.axis('off')
        
        # Paso 4: Superresolución (opcional)
        print("⚡ Aplicando superresolución...")
        try:
            import tensorflow_hub as hub
            
            # Cargar modelo
            model_url = "https://tfhub.dev/captain-pool/esrgan-tf2/1"
            super_res_model = hub.load(model_url)
            
            # Aplicar superresolución
            input_tensor = tf.convert_to_tensor(equalized_rgb, dtype=tf.float32) / 255.0
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
            plt.imshow(equalized_rgb)
            plt.title('Sin Superresolución')
            plt.axis('off')
        
        plt.tight_layout()
        plt.show()
        
        print("✅ Análisis completado exitosamente")
        
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {image_path}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    # Cambiar por la ruta de tu imagen
    image_path = "paisaje_urbano_baja_res.jpg"
    simple_image_analysis(image_path)
