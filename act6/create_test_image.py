#!/usr/bin/env python3
"""
Script para crear una imagen de prueba para la Actividad 6
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def create_test_image():
    """Crear una imagen de prueba con ruido y baja resolución"""
    
    print("🖼️  Creando imagen de prueba...")
    
    # Crear una imagen sintética con patrones
    width, height = 200, 150
    
    # Crear patrones de prueba
    x = np.linspace(0, 4*np.pi, width)
    y = np.linspace(0, 3*np.pi, height)
    X, Y = np.meshgrid(x, y)
    
    # Crear diferentes canales RGB
    red = np.sin(X) * np.cos(Y) * 0.5 + 0.5
    green = np.sin(X + np.pi/3) * np.cos(Y + np.pi/4) * 0.5 + 0.5
    blue = np.sin(X + 2*np.pi/3) * np.cos(Y + 2*np.pi/5) * 0.5 + 0.5
    
    # Combinar canales
    image_array = np.stack([red, green, blue], axis=-1)
    
    # Agregar ruido
    noise = np.random.normal(0, 0.1, image_array.shape)
    image_array = np.clip(image_array + noise, 0, 1)
    
    # Convertir a uint8
    image_array = (image_array * 255).astype(np.uint8)
    
    # Crear imagen PIL
    image = Image.fromarray(image_array)
    
    # Guardar imagen
    image.save("input.jpg")
    
    print("✓ Imagen de prueba creada: input.jpg")
    print(f"  Dimensiones: {image.size}")
    
    # Mostrar la imagen creada
    plt.figure(figsize=(8, 6))
    plt.imshow(image)
    plt.title("Imagen de Prueba Creada")
    plt.axis('off')
    plt.show()
    
    return image

if __name__ == "__main__":
    create_test_image()
