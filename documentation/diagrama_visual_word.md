# Diagrama Visual: Hardware de Visión por Computadora

## FLUJO COMPLETO DEL SISTEMA

### Sistema de Visión por Computadora
```
                    SISTEMA DE VISIÓN POR COMPUTADORA
                                    ↓
                            HARDWARE FÍSICO
```

### Componentes del Hardware
```
CÁMARA 1 → SENSOR → LENTE → PROCESADOR → COMPRESOR → INTERFAZ
Recepción   CCD/CMOS ÓPTICO  DE IMAGEN   H.264      ETHERNET

CÁMARA 2 → SENSOR → LENTE → PROCESADOR → COMPRESOR → INTERFAZ
Zaguan     CCD/CMOS ÓPTICO  DE IMAGEN   H.264      ETHERNET

CÁMARA 3 → SENSOR → LENTE → PROCESADOR → COMPRESOR → INTERFAZ
Soporte    CCD/CMOS ÓPTICO  DE IMAGEN   H.264      ETHERNET

CÁMARA 4 → SENSOR → LENTE → PROCESADOR → COMPRESOR → INTERFAZ
HelpDesk   CCD/CMOS ÓPTICO  DE IMAGEN   H.264      ETHERNET
```

### Red Local
```
                    RED LOCAL
                       ↓
            ┌─────────────────────┐
            │ ROUTER    │ SWITCH  │
            │ • DHCP    │ • VLAN  │
            │ • NAT     │ • QoS   │
            │ • DNS     │ • PoE   │
            └─────────────────────┘
```

### Computadora Central
```
                COMPUTADORA CENTRAL
                       ↓
        ┌─────────────────────────────────┐
        │ TARJETA RED │ CPU              │
        │ • GigE      │ • 4+ cores      │
        │ • PoE       │ • 2.5+ GHz      │
        │ • VLAN      │                  │
        └─────────────────────────────────┘
                       ↓
        ┌─────────────────────────────────┐
        │ RAM         │ GPU     │ALMACENA-│
        │ • 16GB      │ • OpenCV│ MIENTO  │
        │ • DDR4      │ • CUDA  │ • SSD   │
        │ • 3200 MHz  │ • OpenCL│ • NVMe  │
        └─────────────────────────────────┘
```

### Software
```
                    SOFTWARE
                       ↓
        ┌─────────────────────────────────┐
        │ OpenCV      │ PIL              │
        │ • Video     │ • Image          │
        │ • Image     │ • Filter         │
        │ • ML        │ • Save           │
        └─────────────────────────────────┘
                       ↓
        ┌─────────────────────────────────┐
        │ RTSP        │ HTTP             │
        │ Client      │ Server           │
        │ • Stream    │ • Web            │
        │ • Decode    │ • API            │
        │ • Buffer    │ • Files          │
        └─────────────────────────────────┘
```

### Almacenamiento
```
                ALMACENAMIENTO
                       ↓
        ┌─────────────────────────────────┐
        │ CAPTURES    │ LOGS             │
        │ • Images    │ • System         │
        │ • Video     │ • Camera         │
        │ • Date      │ • Error          │
        │ • Camera    │ • Debug          │
        └─────────────────────────────────┘
```

## FLUJO DE DATOS EN TIEMPO REAL

### Timeline de Procesamiento
**TIEMPO: 0ms**
- CÁMARA1, CÁMARA2, CÁMARA3, CÁMARA4 capturan LUZ
- Sensores CCD/CMOS convierten luz a señales
- Conversión Digital A/D

**TIEMPO: 10ms**
- Compresores H.264 procesan frames
- Interfaces Ethernet RTSP transmiten datos

**TIEMPO: 20ms**
- Red Local (Router + Switch) recibe datos
- QoS y VLAN gestionan tráfico

**TIEMPO: 30ms**
- Computadora Central recibe datos
- Tarjeta de Red procesa paquetes
- CPU decodifica y procesa

**TIEMPO: 40ms**
- Software OpenCV + PIL procesa frames
- Resize, filtros y conversiones

**TIEMPO: 50ms**
- Almacenamiento en CAPTURES y LOGS
- Organización por fecha y cámara

## ESPECIFICACIONES TÉCNICAS DETALLADAS

### Configuración de Cámaras RTSP

**CÁMARA 1 - RECEPCIÓN**
- IP: 94.125.136.236:7447
- ID: 4c37181c-71a1-3d56-8a0a
- Resolución: 1280x720
- FPS: 10
- Compresión: H.264
- Buffer: 1 frame

**CÁMARA 2 - ZAGUAN**
- IP: 94.125.136.236:7447
- ID: 17d114c7-2b41-351b-b145
- Resolución: 1280x720
- FPS: 10
- Compresión: H.264
- Buffer: 1 frame

**CÁMARA 3 - SOPORTE**
- IP: 94.125.136.236:7447
- ID: 5c106a76-53bc-3681-bff8
- Resolución: 1280x720
- FPS: 10
- Compresión: H.264
- Buffer: 1 frame

**CÁMARA 4 - HELPDESK**
- IP: 94.125.136.236:7447
- ID: aa478186-ee99-396b-90f6
- Resolución: 1280x720
- FPS: 10
- Compresión: H.264
- Buffer: 1 frame

### Requisitos del Sistema

**HARDWARE MÍNIMO**
- CPU: 4 cores @ 2.0 GHz
- RAM: 8GB DDR4
- GPU: Integrada
- Red: Gigabit Ethernet
- Almacenamiento: 500GB HDD

**HARDWARE RECOMENDADO**
- CPU: 8 cores @ 3.0 GHz
- RAM: 32GB DDR4
- GPU: NVIDIA RTX 3060
- Red: 2.5 Gigabit Ethernet
- Almacenamiento: 2TB NVMe SSD

**RED Y CONECTIVIDAD**
- Ancho de banda: 100 Mbps mínimo por cámara
- Latencia: < 50ms para tiempo real
- Protocolo: RTSP sobre TCP
- QoS: Priorización de tráfico de video
- VLAN: Separación de tráfico de cámaras

---

**Nota**: Este diagrama visual muestra cómo todos los componentes del hardware trabajan en conjunto para proporcionar un sistema de visión por computadora robusto y eficiente.
