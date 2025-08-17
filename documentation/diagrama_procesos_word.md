# Diagrama de Procesos: Funcionamiento del Hardware en Visor por Computadora

## 1. COMPONENTES DEL HARDWARE

### 1.1 Dispositivos de Entrada
- **Cámaras IP/RTSP**: Dispositivos de captura de video en tiempo real
- **Sensores de imagen**: CCD/CMOS que convierten luz en señales eléctricas
- **Lentes ópticos**: Sistema de enfoque y captura de luz
- **Interfaces de red**: Ethernet/WiFi para transmisión de datos

### 1.2 Sistema de Procesamiento
- **CPU**: Procesamiento central de datos
- **GPU**: Aceleración de procesamiento de imagen (opcional)
- **RAM**: Memoria de trabajo para frames de video
- **Almacenamiento**: SSD/HDD para guardar imágenes capturadas

### 1.3 Interfaces de Comunicación
- **Tarjeta de red**: Conexión Ethernet para cámaras RTSP
- **USB**: Conexión directa de cámaras (alternativa)
- **Puertos de video**: HDMI/VGA para monitoreo en tiempo real

## 2. FLUJO DE PROCESO COMPLETO

### Diagrama de Flujo Principal
```
CÁMARA IP → RED LOCAL → COMPUTADORA
    ↓           ↓           ↓
• Sensor CCD   • Ethernet  • CPU/GPU
• Lente óptico • WiFi      • RAM
• Procesador   • Router    • Almacenamiento
• Compresión   • Switch    • Software
```

### Proceso de Captura
```
CAPTURA DE LUZ → TRANSMISIÓN DE DATOS → RECEPCIÓN Y PROCESAMIENTO
      ↓                    ↓                        ↓
• Conversión fotónica   • Protocolo RTSP         • Decodificación
• Digitalización        • Stream H.264           • Buffer de frames
• Compresión H.264/JPEG • Latencia               • Procesamiento
```

## 3. PROCESO DETALLADO DE ADQUISICIÓN

### 3.1 Fase de Captura (Hardware de Cámara)
```
LUZ AMBIENTE → LENTE ÓPTICO → SENSOR CCD/CMOS → CONVERSIÓN A/D → PROCESAMIENTO → COMPRESIÓN → TRANSMISIÓN
    ↓              ↓              ↓              ↓              ↓              ↓              ↓
  Filtros      Enfoque        Píxeles        Señales        Corrección      H.264/        Ethernet/
  de color     automático     RGB            digitales      de color       JPEG          WiFi
```

### 3.2 Fase de Transmisión (Red)
```
CÁMARA → ENCODER → COMPRESOR → BUFFER → TRANSMISOR → RED → ROUTER → SWITCH → COMPUTADORA
  ↓        ↓         ↓         ↓         ↓         ↓      ↓        ↓         ↓
Frame   H.264     Stream    Memoria    Paquetes   IP    Routing  Switch   Recepción
original comprimido temporal  de red   TCP/UDP   addr  table   ports    de datos
```

### 3.3 Fase de Procesamiento (Computadora)
```
RECEPCIÓN → DECODIFICACIÓN → BUFFER → PROCESAMIENTO → ALMACENAMIENTO → VISUALIZACIÓN
    ↓            ↓            ↓           ↓              ↓              ↓
 Paquetes    H.264 →     Memoria      OpenCV/        Archivo        Monitor/
 de red     JPEG        RAM          PIL            imagen         Pantalla
```

## 4. ARQUITECTURA DEL SISTEMA IMPLEMENTADO

### 4.1 Gestión de Cámaras RTSP
```
RTSPCameraManager
       ↓
   RTSPCamera
       ↓
 OpenCVCamera
```

**RTSPCameraManager:**
- Gestión de múltiples cámaras
- Conexiones simultáneas
- Estado de conexión
- Captura sincronizada

**RTSPCamera:**
- Conexión individual RTSP
- Captura de frames
- Gestión de estado
- Manejo de errores

**OpenCVCamera:**
- Interfaz OpenCV
- Captura de video
- Procesamiento de frames
- Codificación/Decodificación

### 4.2 Flujo de Datos en Tiempo Real
```
CÁMARA RTSP → STREAM H.264 → DECODIFICADOR → FRAME BUFFER → PROCESAMIENTO → ALMACENAMIENTO
     ↓            ↓              ↓              ↓              ↓              ↓
 94.125.136.236  Puerto 7447   OpenCV        Memoria RAM    OpenCV Utils   Captures/
    IP Servidor    Protocolo     VideoCapture  Frame Array    Resize/Filter  YYYYMMDD/
```

## 5. ESPECIFICACIONES TÉCNICAS DEL HARDWARE

### 5.1 Requisitos de Red
- **Ancho de banda**: Mínimo 10 Mbps por cámara
- **Latencia**: < 100ms para tiempo real
- **Protocolo**: RTSP sobre TCP/UDP
- **Compresión**: H.264/JPEG para optimización

### 5.2 Requisitos de Computadora
- **CPU**: Mínimo 4 cores para 4 cámaras simultáneas
- **RAM**: 8GB mínimo, 16GB recomendado
- **Almacenamiento**: SSD para capturas rápidas
- **Red**: Gigabit Ethernet para múltiples streams

### 5.3 Configuración de Cámaras
- **Resolución**: 1280x720 (HD) configurado
- **FPS**: 10 frames por segundo
- **Formato**: JPEG con calidad 95%
- **Buffer**: 1 frame para minimizar latencia

## 6. FLUJO DE CAPTURA COMPLETO

### Secuencia de Operaciones
1. **INICIALIZACIÓN**
   - Configuración de cámaras

2. **CONEXIÓN RTSP**
   - Establecer conexión

3. **STREAM DE VIDEO**
   - Recepción continua

4. **CAPTURA DE FRAME**
   - Extraer frame del buffer

5. **PROCESAMIENTO**
   - Resize/Filter/Conversión

6. **ALMACENAMIENTO**
   - Guardar JPEG organizado por fecha/cámara

## 7. OPTIMIZACIONES DEL HARDWARE

### 7.1 Red
- **QoS**: Priorización de tráfico de video
- **VLAN**: Separación de tráfico de cámaras
- **Bandwidth**: Reserva de ancho de banda

### 7.2 Computadora
- **GPU**: Aceleración por hardware para OpenCV
- **SSD NVMe**: Almacenamiento ultra-rápido
- **RAM DDR4**: Alta velocidad de transferencia

### 7.3 Cámaras
- **PoE**: Alimentación por Ethernet
- **IR**: Iluminación infrarroja para baja luz
- **PTZ**: Control pan-tilt-zoom remoto

## 8. MONITOREO Y DIAGNÓSTICO

### 8.1 Métricas de Rendimiento
- **FPS reales**: Frames por segundo efectivos
- **Latencia**: Tiempo de captura a visualización
- **Calidad**: Resolución y compresión efectivas
- **Ancho de banda**: Uso de red por cámara

### 8.2 Logs del Sistema
- **Estado de conexión**: Online/Offline/Error
- **Capturas exitosas**: Contador de imágenes
- **Errores de red**: Timeouts y desconexiones
- **Uso de recursos**: CPU, RAM, almacenamiento

---

**Nota**: Este diagrama ilustra cómo el hardware trabaja en conjunto para proporcionar un sistema de visión por computadora robusto y eficiente para la adquisición de imágenes desde múltiples cámaras RTSP en tiempo real.
