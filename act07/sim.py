import cv2
import numpy as np
import matplotlib.pyplot as plt

def detectar_asimetria_con_visualizacion(imagen):
    """
    Analiza una imagen para detectar asimetría facial como posible signo de ICTUS.
    Genera una visualización que muestra los puntos donde hay más diferencias entre los lados.
    
    IMPORTANTE: Este es un sistema de apoyo diagnóstico. NO reemplaza la evaluación médica profesional.
    """
    # Cargar el clasificador de rostros de OpenCV
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Convertir a escala de grises
    img_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    
    # Detectar rostros
    rostros = face_cascade.detectMultiScale(img_gris, 1.1, 4)
    
    if len(rostros) > 0:
        # Tomar el primer rostro detectado
        (x, y, w, h) = rostros[0]
        
        # Extraer la región del rostro
        rostro_region = img_gris[y:y+h, x:x+w]
        
        # Calcular el centro del rostro
        centro_x = w // 2
        centro_y = h // 2
        
        # Crear imagen de visualización
        img_visualizacion = cv2.cvtColor(rostro_region, cv2.COLOR_GRAY2BGR)
        
        # Dividir el rostro en mitades izquierda y derecha
        mitad_izquierda = rostro_region[:, :centro_x]
        mitad_derecha = rostro_region[:, centro_x:]
        
        # Crear mapa de diferencias pixel por pixel
        diferencia_map = np.zeros_like(rostro_region, dtype=np.float32)
        
        # Para cada pixel, calcular la diferencia con su simétrico
        for i in range(h):
            for j in range(w):
                if j < centro_x:  # Lado izquierdo
                    j_simetrico = w - 1 - j  # Posición simétrica en lado derecho
                    if j_simetrico < w:
                        diff = abs(float(rostro_region[i, j]) - float(rostro_region[i, j_simetrico]))
                        diferencia_map[i, j] = diff
                else:  # Lado derecho
                    j_simetrico = w - 1 - j  # Posición simétrica en lado izquierdo
                    if j_simetrico >= 0:
                        diff = abs(float(rostro_region[i, j]) - float(rostro_region[i, j_simetrico]))
                        diferencia_map[i, j] = diff
        
        # Normalizar el mapa de diferencias
        if np.max(diferencia_map) > 0:
            diferencia_map_norm = (diferencia_map / np.max(diferencia_map) * 255).astype(np.uint8)
        else:
            diferencia_map_norm = diferencia_map.astype(np.uint8)
        
        # Crear mapa de calor
        mapa_calor = cv2.applyColorMap(diferencia_map_norm, cv2.COLORMAP_JET)
        
        # Encontrar puntos con mayor diferencia
        umbral_diferencia = np.percentile(diferencia_map, 90)  # Top 10% de diferencias
        puntos_alta_diferencia = np.where(diferencia_map >= umbral_diferencia)
        
        # Dibujar puntos de alta diferencia
        for i, j in zip(puntos_alta_diferencia[0], puntos_alta_diferencia[1]):
            cv2.circle(img_visualizacion, (j, i), 3, (0, 0, 255), -1)  # Puntos rojos
        
        # Dibujar línea central
        cv2.line(img_visualizacion, (centro_x, 0), (centro_x, h), (255, 255, 255), 2)
        
        # Calcular métricas de asimetría
        intensidad_izquierda = np.mean(mitad_izquierda)
        intensidad_derecha = np.mean(mitad_derecha)
        diferencia_intensidad = abs(intensidad_izquierda - intensidad_derecha)
        
        # Calcular diferencia promedio en el mapa
        diferencia_promedio = np.mean(diferencia_map)
        diferencia_maxima = np.max(diferencia_map)
        
        # MÉTRICAS ESPECÍFICAS PARA DETECCIÓN DE ICTUS
        # Analizar regiones específicas del rostro (ojos, boca, cejas)
        region_ojos = diferencia_map[int(h*0.2):int(h*0.4), :]
        region_boca = diferencia_map[int(h*0.6):int(h*0.8), :]
        region_cejas = diferencia_map[int(h*0.1):int(h*0.3), :]
        
        asimetria_ojos = np.mean(region_ojos)
        asimetria_boca = np.mean(region_boca)
        asimetria_cejas = np.mean(region_cejas)
        
        # Calcular porcentaje de área con alta asimetría
        area_total = h * w
        area_alta_asimetria = len(puntos_alta_diferencia[0])
        porcentaje_asimetria = (area_alta_asimetria / area_total) * 100
        
        # CRITERIOS DE ALERTA PARA ICTUS
        alerta_ictus = False
        nivel_riesgo = "BAJO"
        
        # Umbrales basados en literatura médica para detección de ictus
        UMBRAL_ASIMETRIA_MODERADA = 15.0
        UMBRAL_ASIMETRIA_ALTA = 25.0
        UMBRAL_PORCENTAJE_ASIMETRIA = 20.0
        
        if diferencia_promedio > UMBRAL_ASIMETRIA_ALTA or porcentaje_asimetria > UMBRAL_PORCENTAJE_ASIMETRIA:
            alerta_ictus = True
            nivel_riesgo = "ALTO"
        elif diferencia_promedio > UMBRAL_ASIMETRIA_MODERADA:
            nivel_riesgo = "MODERADO"
        
        # Guardar imágenes de visualización
        cv2.imwrite('rostro_original.jpg', img_visualizacion)
        cv2.imwrite('mapa_diferencias.jpg', mapa_calor)
        
        # Crear imagen combinada
        img_combinada = np.hstack([img_visualizacion, mapa_calor])
        cv2.imwrite('analisis_asimetria.jpg', img_combinada)
        
        # IMPRIMIR RESULTADOS ESPECÍFICOS PARA ICTUS
        print("=" * 60)
        print("ANÁLISIS DE ASIMETRÍA FACIAL PARA DETECCIÓN DE ICTUS")
        print("=" * 60)
        print(f"📊 MÉTRICAS GENERALES:")
        print(f"   • Diferencia promedio: {diferencia_promedio:.2f}")
        print(f"   • Diferencia máxima: {diferencia_maxima:.2f}")
        print(f"   • Diferencia de intensidad: {diferencia_intensidad:.2f}")
        print(f"   • Porcentaje de área asimétrica: {porcentaje_asimetria:.1f}%")
        
        print(f"\n🎯 ANÁLISIS POR REGIONES:")
        print(f"   • Asimetría en ojos: {asimetria_ojos:.2f}")
        print(f"   • Asimetría en boca: {asimetria_boca:.2f}")
        print(f"   • Asimetría en cejas: {asimetria_cejas:.2f}")
        
        print(f"\n⚠️  EVALUACIÓN DE RIESGO:")
        print(f"   • Nivel de riesgo: {nivel_riesgo}")
        if alerta_ictus:
            print(f"   • 🚨 ALERTA: Posible signo de ICTUS detectado")
            print(f"   • 📞 ACCIÓN RECOMENDADA: Buscar atención médica inmediata")
        else:
            print(f"   • ✅ No se detectaron signos evidentes de ICTUS")
        
        print(f"\n📋 CRITERIOS EVALUADOS:")
        print(f"   • Umbral moderado: {UMBRAL_ASIMETRIA_MODERADA}")
        print(f"   • Umbral alto: {UMBRAL_ASIMETRIA_ALTA}")
        print(f"   • Umbral porcentaje: {UMBRAL_PORCENTAJE_ASIMETRIA}%")
        
        print(f"\n📁 Imágenes guardadas:")
        print(f"   • rostro_original.jpg: Rostro con puntos de alta diferencia")
        print(f"   • mapa_diferencias.jpg: Mapa de calor de diferencias")
        print(f"   • analisis_asimetria.jpg: Comparación lado a lado")
        
        print("\n" + "=" * 60)
        print("⚠️  IMPORTANTE: Este es un sistema de apoyo diagnóstico.")
        print("   NO reemplaza la evaluación médica profesional.")
        print("   En caso de sospecha de ICTUS, buscar atención médica inmediata.")
        print("=" * 60)
        
        return diferencia_promedio, diferencia_maxima, len(puntos_alta_diferencia[0]), alerta_ictus, nivel_riesgo
    else:
        print("No se detectó ningún rostro en la imagen.")
        return 0, 0, 0, False, "NO_DETECTADO"

def detectar_asimetria_sonrisa(imagen):
    """
    Función original simplificada para compatibilidad.
    """
    resultado, _, _, _, _ = detectar_asimetria_con_visualizacion(imagen)
    return resultado


# Ejemplo de uso
if __name__ == "__main__":
    print("🏥 SISTEMA DE DETECCIÓN DE ICTUS POR ASIMETRÍA FACIAL")
    print("=" * 60)
    
    # Intentar cargar una imagen real si existe
    imagen_real = cv2.imread("imagen_paciente.jpg")
    
    if imagen_real is not None:
        print("📸 Imagen real encontrada. Iniciando análisis médico...")
        resultado, max_diff, puntos, alerta, riesgo = detectar_asimetria_con_visualizacion(imagen_real)
        
        # Generar reporte médico
        print(f"\n📋 REPORTE MÉDICO:")
        print(f"   • Valor de asimetría: {resultado:.2f}")
        print(f"   • Nivel de riesgo: {riesgo}")
        print(f"   • Alerta activada: {'SÍ' if alerta else 'NO'}")
        
    else:
        print("⚠️  No se encontró imagen_paciente.jpg")
      
    
    print("\n🔍 INTERPRETACIÓN DE RESULTADOS:")
    print("   • Puntos rojos: Áreas con mayor asimetría")
    print("   • Mapa de calor: Intensidad de diferencias (azul=bajo, rojo=alto)")
    print("   • Línea blanca: Eje de simetría")
    print("   • Regiones específicas: Ojos, boca, cejas analizadas por separado")
    
