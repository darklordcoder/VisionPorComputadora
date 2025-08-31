import cv2
import matplotlib.pyplot as plt
import numpy as np
  
# --- Carga de imagen médica real ---
# Cargamos la imagen radiografia.jpg
imagen_original = cv2.imread('radiografia.jpg', cv2.IMREAD_GRAYSCALE)

# Verificamos que la imagen se cargó correctamente
if imagen_original is None:
    print("Error: No se pudo cargar la imagen 'radiografia.jpg'")
    print("Asegúrate de que el archivo existe en el directorio actual")
    exit()
else:
    print(f"Imagen cargada exitosamente. Dimensiones: {imagen_original.shape}")
  
# --- Aplicación de la ecualización de histograma ---
imagen_ecualizada = cv2.equalizeHist(imagen_original)
  
# --- Visualización de resultados ---
plt.style.use('grayscale')
fig, axs = plt.subplots(2, 2, figsize=(12, 10))
  
# Imagen original
axs[0, 0].imshow(imagen_original)
axs[0, 0].set_title('Imagen Original (Bajo Contraste)')
axs[0, 0].axis('off')
  
# Histograma de la imagen original
axs[1, 0].hist(imagen_original.ravel(), bins=256, range=[0, 256])
axs[1, 0].set_title('Histograma Original')
axs[1, 0].set_xlabel('Intensidad de Píxel')
axs[1, 0].set_ylabel('Frecuencia')
# Imagen ecualizada
axs[0, 1].imshow(imagen_ecualizada)
axs[0, 1].set_title('Imagen Ecualizada')
axs[0, 1].axis('off')

# Histograma de la imagen ecualizada
axs[1, 1].hist(imagen_ecualizada.ravel(), bins=256, range=[0, 256])
axs[1, 1].set_title('Histograma Ecualizado')
axs[1, 1].set_xlabel('Intensidad de Píxel')
axs[1, 1].set_ylabel('Frecuencia')

plt.tight_layout()
# Guardar la figura como imagen PNG
plt.savefig('resultado_ecualizacion.png', dpi=300, bbox_inches='tight')
plt.show()
