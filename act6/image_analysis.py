#!/usr/bin/env python3
"""
Actividad 6: Análisis y Mejora de Imágenes con TensorFlow
Proceso completo de mejora de imágenes que incluye:
- Carga de imagen de baja resolución
- Reducción de ruido con filtro Gaussiano
- Mejora de contraste con ecualización de histograma
- Superresolución usando TensorFlow Hub
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_io as tfio

# Configurar TensorFlow para evitar warnings
tf.get_logger().setLevel('ERROR')

class ImageAnalyzer:
    """Clase para análisis y mejora de imágenes usando TensorFlow"""
    
    def __init__(self):
        """Inicializar el analizador de imágenes"""
        self.super_res_model = None
        self.model_loaded = False
        
    def load_image(self, image_path):
        """
        Cargar imagen desde archivo
        
        Args:
            image_path (str): Ruta al archivo de imagen
            
        Returns:
            PIL.Image: Imagen cargada
        """
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"El archivo {image_path} no existe")
            
            image = Image.open(image_path)
            print(f"✓ Imagen cargada exitosamente: {image_path}")
            print(f"  Dimensiones: {image.size}")
            print(f"  Modo: {image.mode}")
            return image
            
        except Exception as e:
            print(f"✗ Error al cargar la imagen: {e}")
            return None
    
    def display_image(self, image, title="Imagen", is_tensor=False):
        """
        Mostrar imagen usando matplotlib
        
        Args:
            image: Imagen a mostrar (PIL.Image o tensor)
            title (str): Título de la imagen
            is_tensor (bool): Si la imagen es un tensor de TensorFlow
        """
        try:
            plt.figure(figsize=(10, 6))
            
            if is_tensor:
                plt.imshow(image)
            else:
                plt.imshow(image)
            
            plt.title(title)
            plt.axis('off')
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"✗ Error al mostrar la imagen: {e}")
    
    def reduce_noise(self, image):
        """
        Reducir ruido usando filtro Gaussiano
        
        Args:
            image (PIL.Image): Imagen de entrada
            
        Returns:
            tf.Tensor: Imagen con ruido reducido
        """
        try:
            print("🔄 Aplicando filtro Gaussiano para reducir ruido...")
            
            # Convertir imagen PIL a tensor de TensorFlow
            image_tensor = tf.convert_to_tensor(np.array(image), dtype=tf.float32) / 255.0
            
            # Aplicar filtro Gaussiano
            # Parámetros ajustables: ksize (tamaño del kernel) y sigma (desviación estándar)
            denoised_tensor = tfio.experimental.filter.gaussian(
                image_tensor, 
                ksize=3, 
                sigma=1.0
            )
            
            print("✓ Ruido reducido exitosamente")
            return denoised_tensor
            
        except Exception as e:
            print(f"✗ Error al reducir ruido: {e}")
            return None
    
    def enhance_contrast(self, image_tensor):
        """
        Mejorar contraste usando ecualización de histograma
        
        Args:
            image_tensor (tf.Tensor): Imagen con ruido reducido
            
        Returns:
            np.ndarray: Imagen con contraste mejorado
        """
        try:
            print("🔄 Mejorando contraste con ecualización de histograma...")
            
            # Convertir tensor a formato de OpenCV
            denoised_cv = np.array(image_tensor * 255, dtype='uint8')
            
            # Convertir a escala de grises
            gray_cv = cv2.cvtColor(denoised_cv, cv2.COLOR_RGB2GRAY)
            
            # Aplicar ecualización de histograma
            equalized_cv = cv2.equalizeHist(gray_cv)
            
            # Convertir de nuevo a RGB para visualización
            equalized_rgb = cv2.cvtColor(equalized_cv, cv2.COLOR_GRAY2RGB)
            
            print("✓ Contraste mejorado exitosamente")
            return equalized_rgb
            
        except Exception as e:
            print(f"✗ Error al mejorar contraste: {e}")
            return None
    
    def load_super_resolution_model(self):
        """
        Cargar modelo de superresolución desde TensorFlow Hub
        
        Returns:
            bool: True si el modelo se cargó exitosamente
        """
        try:
            print("🔄 Cargando modelo de superresolución desde TensorFlow Hub...")
            
            # URL del modelo ESRGAN pre-entrenado
            model_url = "https://tfhub.dev/captain-pool/esrgan-tf2/1"
            
            # Cargar el modelo
            self.super_res_model = hub.load(model_url)
            self.model_loaded = True
            
            print("✓ Modelo de superresolución cargado exitosamente")
            return True
            
        except Exception as e:
            print(f"✗ Error al cargar modelo de superresolución: {e}")
            print("  Nota: Asegúrate de tener conexión a internet")
            return False
    
    def apply_super_resolution(self, image_array):
        """
        Aplicar superresolución a la imagen
        
        Args:
            image_array (np.ndarray): Imagen con contraste mejorado
            
        Returns:
            tf.Tensor: Imagen con superresolución aplicada
        """
        try:
            if not self.model_loaded:
                print("✗ Modelo de superresolución no está cargado")
                return None
            
            print("🔄 Aplicando superresolución...")
            
            # Convertir a tensor y normalizar
            input_tensor = tf.convert_to_tensor(image_array, dtype=tf.float32) / 255.0
            input_tensor = tf.expand_dims(input_tensor, axis=0)  # Añadir dimensión de batch
            
            # Aplicar el modelo de superresolución
            super_res_tensor = self.super_res_model(input_tensor)
            super_res_tensor = tf.squeeze(super_res_tensor, axis=0)  # Quitar dimensión de batch
            
            print("✓ Superresolución aplicada exitosamente")
            return super_res_tensor
            
        except Exception as e:
            print(f"✗ Error al aplicar superresolución: {e}")
            return None
    
    def process_image(self, image_path, show_steps=True):
        """
        Procesar imagen completa: carga, reducción de ruido, mejora de contraste y superresolución
        
        Args:
            image_path (str): Ruta al archivo de imagen
            show_steps (bool): Si mostrar cada paso del proceso
            
        Returns:
            dict: Diccionario con todas las imágenes procesadas
        """
        results = {}
        
        print("=" * 60)
        print("🚀 INICIANDO PROCESAMIENTO DE IMAGEN")
        print("=" * 60)
        
        # Paso 1: Cargar imagen original
        print("\n📸 PASO 1: Cargando imagen original")
        original_image = self.load_image(image_path)
        if original_image is None:
            return results
        
        results['original'] = original_image
        
        if show_steps:
            self.display_image(original_image, "Imagen de Baja Resolución Original")
        
        # Paso 2: Reducir ruido
        print("\n🔧 PASO 2: Reduciendo ruido")
        denoised_tensor = self.reduce_noise(original_image)
        if denoised_tensor is None:
            return results
        
        results['denoised'] = denoised_tensor
        
        if show_steps:
            self.display_image(denoised_tensor, "Imagen con Ruido Reducido", is_tensor=True)
        
        # Paso 3: Mejorar contraste
        print("\n🎨 PASO 3: Mejorando contraste")
        enhanced_image = self.enhance_contrast(denoised_tensor)
        if enhanced_image is None:
            return results
        
        results['enhanced'] = enhanced_image
        
        if show_steps:
            self.display_image(enhanced_image, "Imagen con Contraste Mejorado")
        
        # Paso 4: Cargar modelo de superresolución
        print("\n🤖 PASO 4: Preparando superresolución")
        if not self.load_super_resolution_model():
            print("⚠️  Continuando sin superresolución...")
            return results
        
        # Paso 5: Aplicar superresolución
        print("\n⚡ PASO 5: Aplicando superresolución")
        super_res_image = self.apply_super_resolution(enhanced_image)
        if super_res_image is None:
            return results
        
        results['super_resolution'] = super_res_image
        
        if show_steps:
            self.display_image(super_res_image, "Imagen Mejorada con Superresolución", is_tensor=True)
        
        print("\n" + "=" * 60)
        print("✅ PROCESAMIENTO COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        
        return results
    
    def save_results(self, results, output_dir="act6/output"):
        """
        Guardar todas las imágenes procesadas
        
        Args:
            results (dict): Diccionario con las imágenes procesadas
            output_dir (str): Directorio de salida
        """
        try:
            # Crear directorio de salida si no existe
            os.makedirs(output_dir, exist_ok=True)
            
            print(f"\n💾 Guardando resultados en: {output_dir}")
            
            # Guardar imagen original
            if 'original' in results:
                results['original'].save(os.path.join(output_dir, "01_original.jpg"))
                print("✓ Imagen original guardada")
            
            # Guardar imagen con ruido reducido
            if 'denoised' in results:
                denoised_np = np.array(results['denoised'] * 255, dtype='uint8')
                Image.fromarray(denoised_np).save(os.path.join(output_dir, "02_denoised.jpg"))
                print("✓ Imagen con ruido reducido guardada")
            
            # Guardar imagen con contraste mejorado
            if 'enhanced' in results:
                Image.fromarray(results['enhanced']).save(os.path.join(output_dir, "03_enhanced.jpg"))
                print("✓ Imagen con contraste mejorado guardada")
            
            # Guardar imagen con superresolución
            if 'super_resolution' in results:
                super_res_np = np.array(results['super_resolution'] * 255, dtype='uint8')
                Image.fromarray(super_res_np).save(os.path.join(output_dir, "04_super_resolution.jpg"))
                print("✓ Imagen con superresolución guardada")
            
            print(f"✅ Todos los resultados guardados en: {output_dir}")
            
        except Exception as e:
            print(f"✗ Error al guardar resultados: {e}")


def main():
    """Función principal para ejecutar el análisis de imágenes"""
    
    # Crear instancia del analizador
    analyzer = ImageAnalyzer()
    
    # Ruta de la imagen de entrada
    image_path = "paisaje_urbano_baja_res.jpg"
    
    # Verificar si el archivo existe
    if not os.path.exists(image_path):
        print(f"❌ Error: No se encontró el archivo {image_path}")
        print("📝 Por favor, asegúrate de que el archivo existe en el directorio actual")
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
        
        return
    
    try:
        # Procesar la imagen
        results = analyzer.process_image(image_path, show_steps=True)
        
        # Guardar resultados
        if results:
            analyzer.save_results(results)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
