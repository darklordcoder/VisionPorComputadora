#!/usr/bin/env python3
"""
Actividad 6: Procesamiento de Imágenes (Versión sin TensorFlow Hub)
Implementación de los 3 procesos requeridos usando solo OpenCV:
1. Filtros para reducir el ruido
2. Aumentar el contraste  
3. Técnicas de superresolución para mejorar la definición (interpolación)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2

class ImageProcessorOpenCV:
    """Procesador de imágenes usando solo OpenCV"""
    
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
            axes[i].imshow(img)
            axes[i].set_title(title)
            axes[i].axis('off')
        
        plt.tight_layout()
        plt.show()
    
    def reduce_noise(self, image):
        """
        PROCESO 1: Filtros para reducir el ruido
        Implementa múltiples técnicas de reducción de ruido con OpenCV
        """
        print("\n🔧 PROCESO 1: Reduciendo ruido con filtros")
        print("-" * 50)
        
        image_array = np.array(image)
        
        # Método 1: Filtro Gaussiano
        print("• Aplicando filtro Gaussiano...")
        gaussian_filtered = cv2.GaussianBlur(image_array, (5, 5), 1.0)
        
        # Método 2: Filtro de mediana
        print("• Aplicando filtro de mediana...")
        median_filtered = cv2.medianBlur(image_array, 5)
        
        # Método 3: Filtro bilateral (preserva bordes)
        print("• Aplicando filtro bilateral...")
        bilateral_filtered = cv2.bilateralFilter(image_array, 9, 75, 75)
        
        # Método 4: Filtro de suavizado no local
        print("• Aplicando filtro no local...")
        nlm_filtered = cv2.fastNlMeansDenoisingColored(image_array, None, 10, 10, 7, 21)
        
        # Método 5: Filtro de suavizado adaptativo (usando bilateral con parámetros adaptativos)
        print("• Aplicando filtro adaptativo...")
        adaptive_filtered = cv2.bilateralFilter(image_array, 15, 80, 80)
        
        # Mostrar comparación de métodos
        methods = [
            ("Original", image_array),
            ("Gaussiano", gaussian_filtered),
            ("Mediana", median_filtered),
            ("Bilateral", bilateral_filtered),
            ("No Local", nlm_filtered),
            ("Adaptativo", adaptive_filtered)
        ]
        
        print("✓ Comparando métodos de reducción de ruido...")
        self.display_comparison([img for _, img in methods], [title for title, _ in methods])
        
        # Retornar el mejor resultado (filtro bilateral)
        return bilateral_filtered
    
    def increase_contrast(self, image_array):
        """
        PROCESO 2: Aumentar el contraste
        Implementa múltiples técnicas de mejora de contraste con OpenCV
        """
        print("\n🎨 PROCESO 2: Aumentando contraste")
        print("-" * 50)
        
        # Método 1: Ecualización de histograma simple
        print("• Aplicando ecualización de histograma...")
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        equalized_gray = cv2.equalizeHist(gray)
        equalized_rgb = cv2.cvtColor(equalized_gray, cv2.COLOR_GRAY2RGB)
        
        # Método 2: CLAHE (Contrast Limited Adaptive Histogram Equalization)
        print("• Aplicando CLAHE...")
        lab = cv2.cvtColor(image_array, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        clahe_rgb = cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2RGB)
        
        # Método 3: Ajuste de gamma
        print("• Aplicando ajuste de gamma...")
        gamma = 1.5
        gamma_corrected = np.power(image_array / 255.0, gamma) * 255
        gamma_corrected = np.clip(gamma_corrected, 0, 255).astype(np.uint8)
        
        # Método 4: Estiramiento de contraste
        print("• Aplicando estiramiento de contraste...")
        stretched = image_array.copy()
        for i in range(3):  # Para cada canal RGB
            channel = stretched[:, :, i]
            min_val, max_val = channel.min(), channel.max()
            if max_val > min_val:
                stretched[:, :, i] = ((channel - min_val) / (max_val - min_val) * 255).astype(np.uint8)
        
        # Método 5: Mejora de contraste local
        print("• Aplicando mejora de contraste local...")
        lab_local = cv2.cvtColor(image_array, cv2.COLOR_RGB2LAB)
        l_local, a_local, b_local = cv2.split(lab_local)
        
        # Aplicar CLAHE con parámetros más agresivos
        clahe_local = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(4, 4))
        l_local = clahe_local.apply(l_local)
        
        local_enhanced = cv2.cvtColor(cv2.merge([l_local, a_local, b_local]), cv2.COLOR_LAB2RGB)
        
        # Mostrar comparación de métodos
        methods = [
            ("Original", image_array),
            ("Ecualización", equalized_rgb),
            ("CLAHE", clahe_rgb),
            ("Gamma", gamma_corrected),
            ("Estiramiento", stretched),
            ("Local", local_enhanced)
        ]
        
        print("✓ Comparando métodos de mejora de contraste...")
        self.display_comparison([img for _, img in methods], [title for title, _ in methods])
        
        # Retornar CLAHE (mejor resultado)
        return clahe_rgb
    
    def super_resolution_interpolation(self, image_array):
        """
        PROCESO 3: Técnicas de superresolución para mejorar la definición
        Implementa superresolución usando interpolación avanzada
        """
        print("\n⚡ PROCESO 3: Aplicando superresolución")
        print("-" * 50)
        
        # Factor de escala (2x)
        scale_factor = 2
        
        # Método 1: Interpolación bicúbica
        print("• Aplicando interpolación bicúbica...")
        bicubic = cv2.resize(image_array, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
        
        # Método 2: Interpolación Lanczos
        print("• Aplicando interpolación Lanczos...")
        lanczos = cv2.resize(image_array, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LANCZOS4)
        
        # Método 3: Interpolación con filtro de nitidez
        print("• Aplicando interpolación con nitidez...")
        # Primero interpolación bicúbica
        sharpened = cv2.resize(image_array, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
        
        # Luego aplicar filtro de nitidez
        kernel_sharpen = np.array([[-1,-1,-1],
                                   [-1, 9,-1],
                                   [-1,-1,-1]])
        sharpened = cv2.filter2D(sharpened, -1, kernel_sharpen)
        sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
        
        # Método 4: Superresolución con EDGE_PRESERVING
        print("• Aplicando filtro edge-preserving...")
        edge_preserving = cv2.edgePreservingFilter(image_array, flags=1, sigma_s=50, sigma_r=0.4)
        edge_preserving = cv2.resize(edge_preserving, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
        
        # Método 5: Superresolución con DETAIL_ENHANCE
        print("• Aplicando realce de detalles...")
        detail_enhanced = cv2.detailEnhance(image_array, sigma_s=10, sigma_r=0.15)
        detail_enhanced = cv2.resize(detail_enhanced, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
        
        # Mostrar comparación de métodos
        methods = [
            ("Original", image_array),
            ("Bicúbica", bicubic),
            ("Lanczos", lanczos),
            ("Con Nitidez", sharpened),
            ("Edge-Preserving", edge_preserving),
            ("Detail Enhanced", detail_enhanced)
        ]
        
        print("✓ Comparando métodos de superresolución...")
        self.display_comparison([img for _, img in methods], [title for title, _ in methods])
        
        # Retornar el mejor resultado (detail enhanced)
        return detail_enhanced
    
    def process_complete_pipeline(self, image_path):
        """
        Ejecutar el pipeline completo de los 3 procesos
        """
        print("=" * 60)
        print("🚀 INICIANDO PIPELINE DE PROCESAMIENTO DE IMÁGENES (OpenCV)")
        print("=" * 60)
        
        # Cargar imagen
        original_image = self.load_image(image_path)
        if original_image is None:
            return None
        
        # Convertir a array para procesamiento
        image_array = np.array(original_image)
        
        # PROCESO 1: Reducir ruido
        denoised_image = self.reduce_noise(original_image)
        
        # PROCESO 2: Aumentar contraste
        enhanced_image = self.increase_contrast(denoised_image)
        
        # PROCESO 3: Superresolución
        final_image = self.super_resolution_interpolation(enhanced_image)
        
        # Mostrar resultado final
        print("\n📊 RESULTADO FINAL")
        print("-" * 50)
        self.display_comparison(
            [image_array, denoised_image, enhanced_image, final_image],
            ["Original", "Sin Ruido", "Contraste Mejorado", "Superresolución"]
        )
        
        # Guardar resultados
        self.save_results({
            'original': original_image,
            'denoised': denoised_image,
            'enhanced': enhanced_image,
            'final': final_image
        })
        
        print("\n✅ PIPELINE COMPLETADO EXITOSAMENTE")
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
            Image.fromarray(results['denoised']).save("output/02_denoised.jpg")
            Image.fromarray(results['enhanced']).save("output/03_enhanced.jpg")
            Image.fromarray(results['final']).save("output/04_super_resolution.jpg")
            
            print("✓ Resultados guardados en carpeta 'output'")
            
        except Exception as e:
            print(f"✗ Error al guardar: {e}")


def main():
    """Función principal"""
    processor = ImageProcessorOpenCV()
    
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
        # Ejecutar pipeline completo
        results = processor.process_complete_pipeline(image_path)
        
        if results:
            print("\n🎉 ¡Procesamiento completado!")
            print("📁 Revisa la carpeta 'output' para ver los resultados")
        
    except KeyboardInterrupt:
        print("\n⏹️  Proceso interrumpido")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
