#!/usr/bin/env python3
"""
Actividad 6: Procesamiento de Imágenes con TensorFlow
Implementación de los 3 procesos requeridos usando TensorFlow:
1. Filtros para reducir el ruido
2. Aumentar el contraste  
3. Técnicas de superresolución para mejorar la definición
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2
import tensorflow as tf
import tensorflow_hub as hub

# Configurar TensorFlow para evitar warnings
tf.get_logger().setLevel('ERROR')

class TensorFlowImageProcessor:
    """Procesador de imágenes usando TensorFlow para los 3 procesos requeridos"""
    
    def __init__(self):
        self.super_res_model = None
        self.model_loaded = False
    
    def load_image(self, image_path):
        """Cargar imagen desde archivo"""
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"El archivo {image_path} no existe")
            
            image = Image.open(image_path)
            print(f"✓ Imagen cargada: {image_path}")
            print(f"  Dimensiones: {image.size}")
            return image
            
        except Exception as e:
            print(f"✗ Error al cargar imagen: {e}")
            return None
    
    def display_comparison(self, images, titles):
        """Mostrar comparación de imágenes"""
        fig, axes = plt.subplots(1, len(images), figsize=(5*len(images), 5))
        if len(images) == 1:
            axes = [axes]
        
        for i, (img, title) in enumerate(zip(images, titles)):
            if isinstance(img, tf.Tensor):
                img = img.numpy()
            axes[i].imshow(img)
            axes[i].set_title(title)
            axes[i].axis('off')
        
        plt.tight_layout()
        plt.show()
    
    def reduce_noise_tensorflow(self, image):
        """
        PROCESO 1: Filtros para reducir el ruido usando TensorFlow
        Implementa múltiples técnicas de reducción de ruido con TensorFlow
        """
        print("\n🔧 PROCESO 1: Reduciendo ruido con TensorFlow")
        print("-" * 50)
        
        # Convertir imagen PIL a tensor de TensorFlow
        image_array = np.array(image)
        image_tensor = tf.convert_to_tensor(image_array, dtype=tf.float32) / 255.0
        
        # Método 1: Filtro Gaussiano usando TensorFlow
        print("• Aplicando filtro Gaussiano con TensorFlow...")
        gaussian_kernel = tf.constant([
            [1, 2, 1],
            [2, 4, 2],
            [1, 2, 1]
        ], dtype=tf.float32) / 16.0
        
        gaussian_filtered = self.apply_convolution_filter(image_tensor, gaussian_kernel)
        
        # Método 2: Filtro de suavizado usando TensorFlow
        print("• Aplicando filtro de suavizado con TensorFlow...")
        smooth_kernel = tf.constant([
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ], dtype=tf.float32) / 9.0
        
        smooth_filtered = self.apply_convolution_filter(image_tensor, smooth_kernel)
        
        # Método 3: Filtro de nitidez usando TensorFlow
        print("• Aplicando filtro de nitidez con TensorFlow...")
        sharpen_kernel = tf.constant([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ], dtype=tf.float32)
        
        sharpen_filtered = self.apply_convolution_filter(image_tensor, sharpen_kernel)
        
        # Método 4: Filtro de mediana usando TensorFlow (aproximación)
        print("• Aplicando filtro de mediana con TensorFlow...")
        median_filtered = self.apply_median_filter_tensorflow(image_tensor)
        
        # Método 5: Filtro de reducción de ruido usando TensorFlow
        print("• Aplicando filtro de reducción de ruido con TensorFlow...")
        noise_reduction_filtered = self.apply_noise_reduction_tensorflow(image_tensor)
        
        # Convertir tensores de vuelta a arrays para visualización
        original_array = image_array
        gaussian_array = np.array(gaussian_filtered * 255, dtype=np.uint8)
        smooth_array = np.array(smooth_filtered * 255, dtype=np.uint8)
        sharpen_array = np.array(sharpen_filtered * 255, dtype=np.uint8)
        median_array = np.array(median_filtered * 255, dtype=np.uint8)
        noise_reduction_array = np.array(noise_reduction_filtered * 255, dtype=np.uint8)
        
        # Mostrar comparación de métodos
        methods = [
            ("Original", original_array),
            ("Gaussiano TF", gaussian_array),
            ("Suavizado TF", smooth_array),
            ("Nitidez TF", sharpen_array),
            ("Mediana TF", median_array),
            ("Reducción Ruido TF", noise_reduction_array)
        ]
        
        print("✓ Comparando métodos de reducción de ruido con TensorFlow...")
        self.display_comparison([img for _, img in methods], [title for title, _ in methods])
        
        # Retornar el mejor resultado (reducción de ruido)
        return noise_reduction_array
    
    def apply_convolution_filter(self, image_tensor, kernel):
        """Aplicar filtro de convolución usando TensorFlow"""
        # Expandir dimensiones para convolución
        kernel = tf.expand_dims(tf.expand_dims(kernel, -1), -1)
        
        # Aplicar convolución para cada canal
        channels = []
        for i in range(3):  # RGB
            channel = tf.expand_dims(image_tensor[:, :, i], -1)
            filtered = tf.nn.conv2d(
                tf.expand_dims(channel, 0), 
                kernel, 
                strides=[1, 1, 1, 1], 
                padding='SAME'
            )
            channels.append(tf.squeeze(filtered, [0, -1]))
        
        # Combinar canales y normalizar
        result = tf.stack(channels, axis=-1)
        return tf.clip_by_value(result, 0.0, 1.0)
    
    def apply_median_filter_tensorflow(self, image_tensor):
        """Aplicar filtro de mediana usando TensorFlow"""
        # Convertir a escala de grises para simplificar
        gray = tf.image.rgb_to_grayscale(image_tensor)
        
        # Aplicar filtro de mediana usando tf.nn.avg_pool como aproximación
        pooled = tf.nn.avg_pool(
            tf.expand_dims(gray, 0),
            ksize=[1, 3, 3, 1],
            strides=[1, 1, 1, 1],
            padding='SAME'
        )
        
        # Convertir de vuelta a RGB
        pooled_rgb = tf.image.grayscale_to_rgb(tf.squeeze(pooled, 0))
        return pooled_rgb
    
    def apply_noise_reduction_tensorflow(self, image_tensor):
        """Aplicar reducción de ruido usando TensorFlow"""
        # Combinar múltiples técnicas de TensorFlow
        
        # 1. Suavizado gaussiano
        gaussian_kernel = tf.constant([
            [1, 2, 1],
            [2, 4, 2],
            [1, 2, 1]
        ], dtype=tf.float32) / 16.0
        
        smoothed = self.apply_convolution_filter(image_tensor, gaussian_kernel)
        
        # 2. Aplicar filtro de preservación de bordes
        edge_kernel = tf.constant([
            [-1, -1, -1],
            [-1,  8, -1],
            [-1, -1, -1]
        ], dtype=tf.float32)
        
        edges = self.apply_convolution_filter(smoothed, edge_kernel)
        
        # 3. Combinar suavizado con preservación de bordes
        result = smoothed + 0.1 * edges
        return tf.clip_by_value(result, 0.0, 1.0)
    
    def equalize_histogram_tensorflow(self, image_tensor):
        """Implementar ecualización de histograma usando TensorFlow"""
        # Convertir a escala de grises
        gray = tf.image.rgb_to_grayscale(image_tensor)
        
        # Calcular histograma acumulativo
        histogram = tf.histogram_fixed_width(
            tf.cast(gray * 255, tf.int32),
            [0, 255],
            nbins=256
        )
        
        # Calcular función de distribución acumulativa
        cdf = tf.cumsum(histogram)
        cdf_min = tf.reduce_min(cdf)
        
        # Normalizar CDF
        cdf_normalized = (cdf - cdf_min) / (tf.reduce_max(cdf) - cdf_min)
        
        # Aplicar transformación
        gray_equalized = tf.gather(cdf_normalized, tf.cast(gray * 255, tf.int32))
        
        # Convertir de vuelta a RGB
        equalized_rgb = tf.image.grayscale_to_rgb(gray_equalized)
        
        return equalized_rgb
    
    def increase_contrast_tensorflow(self, image_array):
        """
        PROCESO 2: Aumentar el contraste usando TensorFlow
        Implementa múltiples técnicas de mejora de contraste con TensorFlow
        """
        print("\n🎨 PROCESO 2: Aumentando contraste con TensorFlow")
        print("-" * 50)
        
        # Convertir a tensor de TensorFlow
        image_tensor = tf.convert_to_tensor(image_array, dtype=tf.float32) / 255.0
        
        # Método 1: Ajuste de contraste usando TensorFlow
        print("• Aplicando ajuste de contraste con TensorFlow...")
        contrast_factor = 1.5
        contrast_adjusted = tf.image.adjust_contrast(image_tensor, contrast_factor)
        
        # Método 2: Ajuste de brillo usando TensorFlow
        print("• Aplicando ajuste de brillo con TensorFlow...")
        brightness_delta = 0.1
        brightness_adjusted = tf.image.adjust_brightness(image_tensor, brightness_delta)
        
        # Método 3: Ajuste de gamma usando TensorFlow
        print("• Aplicando ajuste de gamma con TensorFlow...")
        gamma = 1.2
        gamma_adjusted = tf.image.adjust_gamma(image_tensor, gamma)
        
        # Método 4: Ecualización de histograma usando TensorFlow (implementación manual)
        print("• Aplicando ecualización de histograma con TensorFlow...")
        equalized = self.equalize_histogram_tensorflow(image_tensor)
        
        # Método 5: Combinación de ajustes usando TensorFlow
        print("• Aplicando combinación de ajustes con TensorFlow...")
        combined = tf.image.adjust_contrast(
            tf.image.adjust_brightness(
                tf.image.adjust_gamma(image_tensor, 1.1), 
                0.05
            ), 
            1.3
        )
        
        # Convertir tensores de vuelta a arrays para visualización
        original_array = image_array
        contrast_array = np.array(contrast_adjusted * 255, dtype=np.uint8)
        brightness_array = np.array(brightness_adjusted * 255, dtype=np.uint8)
        gamma_array = np.array(gamma_adjusted * 255, dtype=np.uint8)
        equalized_array = np.array(equalized * 255, dtype=np.uint8)
        combined_array = np.array(combined * 255, dtype=np.uint8)
        
        # Mostrar comparación de métodos
        methods = [
            ("Original", original_array),
            ("Contraste TF", contrast_array),
            ("Brillo TF", brightness_array),
            ("Gamma TF", gamma_array),
            ("Ecualizado TF", equalized_array),
            ("Combinado TF", combined_array)
        ]
        
        print("✓ Comparando métodos de mejora de contraste con TensorFlow...")
        self.display_comparison([img for _, img in methods], [title for title, _ in methods])
        
        # Retornar el mejor resultado (combinado)
        return combined_array
    
    def load_super_resolution_model(self):
        """Cargar modelo de superresolución desde TensorFlow Hub"""
        try:
            print("\n🤖 Cargando modelo de superresolución desde TensorFlow Hub...")
            model_url = "https://tfhub.dev/captain-pool/esrgan-tf2/1"
            self.super_res_model = hub.load(model_url)
            self.model_loaded = True
            print("✓ Modelo ESRGAN cargado exitosamente")
            return True
        except Exception as e:
            print(f"✗ Error al cargar modelo: {e}")
            print("  Nota: Se requiere conexión a internet")
            return False
    
    def super_resolution_tensorflow(self, image_array):
        """
        PROCESO 3: Técnicas de superresolución usando TensorFlow
        Implementa superresolución usando TensorFlow Hub y técnicas nativas
        """
        print("\n⚡ PROCESO 3: Aplicando superresolución con TensorFlow")
        print("-" * 50)
        
        # Convertir a tensor de TensorFlow
        image_tensor = tf.convert_to_tensor(image_array, dtype=tf.float32) / 255.0
        
        # Método 1: Superresolución con TensorFlow Hub (ESRGAN)
        print("• Intentando aplicar ESRGAN con TensorFlow Hub...")
        if not self.model_loaded:
            self.load_super_resolution_model()
        
        if self.model_loaded:
            try:
                input_tensor = tf.expand_dims(image_tensor, axis=0)
                super_res_tensor = self.super_res_model(input_tensor)
                super_res_tensor = tf.squeeze(super_res_tensor, axis=0)
                esrgan_array = np.array(super_res_tensor * 255, dtype=np.uint8)
                print("✓ ESRGAN aplicado exitosamente")
            except Exception as e:
                print(f"⚠️  ESRGAN falló: {e}")
                esrgan_array = image_array
        else:
            esrgan_array = image_array
        
        # Método 2: Superresolución usando TensorFlow nativo
        print("• Aplicando superresolución nativa de TensorFlow...")
        scale_factor = 2
        new_height = int(image_tensor.shape[0] * scale_factor)
        new_width = int(image_tensor.shape[1] * scale_factor)
        
        # Usar tf.image.resize con interpolación bicúbica
        resized_tensor = tf.image.resize(
            image_tensor, 
            [new_height, new_width], 
            method='bicubic'
        )
        
        # Aplicar filtro de nitidez después del resize
        sharpen_kernel = tf.constant([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ], dtype=tf.float32)
        
        sharpened_tensor = self.apply_convolution_filter(resized_tensor, sharpen_kernel)
        tf_native_array = np.array(sharpened_tensor * 255, dtype=np.uint8)
        
        # Método 3: Superresolución con preservación de bordes
        print("• Aplicando superresolución con preservación de bordes...")
        
        # Detectar bordes primero
        edge_kernel = tf.constant([
            [-1, -1, -1],
            [-1,  8, -1],
            [-1, -1, -1]
        ], dtype=tf.float32)
        
        edges = self.apply_convolution_filter(image_tensor, edge_kernel)
        
        # Resize de la imagen original
        resized_original = tf.image.resize(
            image_tensor, 
            [new_height, new_width], 
            method='bicubic'
        )
        
        # Resize de los bordes
        resized_edges = tf.image.resize(
            edges, 
            [new_height, new_width], 
            method='bicubic'
        )
        
        # Combinar imagen resized con bordes mejorados
        edge_preserved = resized_original + 0.1 * resized_edges
        edge_preserved = tf.clip_by_value(edge_preserved, 0.0, 1.0)
        edge_preserved_array = np.array(edge_preserved * 255, dtype=np.uint8)
        
        # Mostrar comparación de métodos
        methods = [
            ("Original", image_array),
            ("ESRGAN", esrgan_array),
            ("TF Nativo", tf_native_array),
            ("Preserva Bordes", edge_preserved_array)
        ]
        
        print("✓ Comparando métodos de superresolución con TensorFlow...")
        self.display_comparison([img for _, img in methods], [title for title, _ in methods])
        
        # Retornar el mejor resultado (ESRGAN si está disponible, sino TF nativo)
        if self.model_loaded and not np.array_equal(esrgan_array, image_array):
            return esrgan_array
        else:
            return tf_native_array
    
    def process_complete_pipeline(self, image_path):
        """
        Ejecutar el pipeline completo de los 3 procesos usando TensorFlow
        """
        print("=" * 60)
        print("🚀 INICIANDO PIPELINE DE PROCESAMIENTO CON TENSORFLOW")
        print("=" * 60)
        
        # Cargar imagen
        original_image = self.load_image(image_path)
        if original_image is None:
            return None
        
        # Convertir a array para procesamiento
        image_array = np.array(original_image)
        
        # PROCESO 1: Reducir ruido con TensorFlow
        denoised_image = self.reduce_noise_tensorflow(original_image)
        
        # PROCESO 2: Aumentar contraste con TensorFlow
        enhanced_image = self.increase_contrast_tensorflow(denoised_image)
        
        # PROCESO 3: Superresolución con TensorFlow
        final_image = self.super_resolution_tensorflow(enhanced_image)
        
        # Mostrar resultado final
        print("\n📊 RESULTADO FINAL")
        print("-" * 50)
        self.display_comparison(
            [image_array, denoised_image, enhanced_image, final_image],
            ["Original", "Sin Ruido (TF)", "Contraste Mejorado (TF)", "Superresolución (TF)"]
        )
        
        # Guardar resultados
        self.save_results({
            'original': original_image,
            'denoised': denoised_image,
            'enhanced': enhanced_image,
            'final': final_image
        })
        
        print("\n✅ PIPELINE COMPLETADO EXITOSAMENTE CON TENSORFLOW")
        print("=" * 60)
        
        return {
            'original': image_array,
            'denoised': denoised_image,
            'enhanced': enhanced_image,
            'final': final_image
        }
    
    def save_results(self, results):
        """Guardar todas las imágenes procesadas"""
        try:
            os.makedirs("output", exist_ok=True)
            print("\n💾 Guardando resultados...")
            
            results['original'].save("output/01_original.jpg")
            Image.fromarray(results['denoised']).save("output/02_denoised_tensorflow.jpg")
            Image.fromarray(results['enhanced']).save("output/03_enhanced_tensorflow.jpg")
            Image.fromarray(results['final']).save("output/04_super_resolution_tensorflow.jpg")
            
            print("✓ Resultados guardados en carpeta 'output'")
            
        except Exception as e:
            print(f"✗ Error al guardar: {e}")


def main():
    """Función principal"""
    processor = TensorFlowImageProcessor()
    
    # Ruta de la imagen
    image_path = "input.jpg"
    
    # Verificar si existe la imagen
    if not os.path.exists(image_path):
        print(f"❌ No se encontró: {image_path}")
        print("📁 Archivos disponibles:")
        
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        for file in os.listdir('.'):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                print(f"   - {file}")
        return
    
    try:
        # Ejecutar pipeline completo con TensorFlow
        results = processor.process_complete_pipeline(image_path)
        
        if results:
            print("\n🎉 ¡Procesamiento con TensorFlow completado!")
            print("📁 Revisa la carpeta 'output' para ver los resultados")
        
    except KeyboardInterrupt:
        print("\n⏹️  Proceso interrumpido")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
