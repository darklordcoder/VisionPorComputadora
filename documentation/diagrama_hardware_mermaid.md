# Diagramas Mermaid de Hardware: Visión por Computadora

## 1. ARQUITECTURA FÍSICA DEL SISTEMA

### Diagrama de Componentes del Hardware
```mermaid
graph TB
    subgraph "CÁMARAS IP/RTSP"
        CAM1[📷 Cámara 1<br/>Recepción<br/>IP: 94.125.136.236:7447]
        CAM2[📷 Cámara 2<br/>Zaguan<br/>IP: 94.125.136.236:7447]
        CAM3[📷 Cámara 3<br/>Soporte<br/>IP: 94.125.136.236:7447]
        CAM4[📷 Cámara 4<br/>HelpDesk<br/>IP: 94.125.136.236:7447]
    end
    
    subgraph "COMPONENTES INTERNOS CÁMARA"
        SENSOR[🔍 Sensor<br/>CCD/CMOS<br/>1280x720]
        LENTE[🔭 Lente<br/>Óptico<br/>Auto-focus]
        PROC[⚙️ Procesador<br/>de Imagen<br/>H.264]
        COMP[📦 Compresor<br/>H.264<br/>10 FPS]
        ETH[🌐 Ethernet<br/>PoE<br/>Gigabit]
    end
    
    subgraph "RED LOCAL"
        ROUTER[🔄 Router<br/>DHCP/NAT/DNS<br/>QoS]
        SWITCH[🔌 Switch<br/>VLAN/QoS/PoE<br/>Gigabit]
    end
    
    subgraph "COMPUTADORA CENTRAL"
        CPU[🖥️ CPU<br/>4+ cores<br/>2.5+ GHz]
        RAM[💾 RAM<br/>16GB DDR4<br/>3200 MHz]
        GPU[🎮 GPU<br/>OpenCV/CUDA<br/>OpenCL]
        STORAGE[💿 Almacenamiento<br/>SSD/NVMe<br/>1TB+]
        NET[🌐 Tarjeta Red<br/>Gigabit<br/>PoE/VLAN]
    end
    
    subgraph "SOFTWARE"
        OPENCV[🔧 OpenCV<br/>Video/Image/ML]
        PIL[🖼️ PIL<br/>Image/Filter/Save]
        RTSP[📡 RTSP Client<br/>Stream/Decode]
        HTTP[🌍 HTTP Server<br/>Web/API]
    end
    
    subgraph "ALMACENAMIENTO"
        CAPTURES[📁 Captures<br/>Images/Video<br/>YYYYMMDD/]
        LOGS[📋 Logs<br/>System/Camera<br/>Error/Debug]
    end
    
    %% Conexiones de cámaras
    CAM1 --> SENSOR
    CAM2 --> SENSOR
    CAM3 --> SENSOR
    CAM4 --> SENSOR
    
    %% Flujo interno de cámara
    SENSOR --> LENTE
    LENTE --> PROC
    PROC --> COMP
    COMP --> ETH
    
    %% Conexiones de red
    ETH --> ROUTER
    ETH --> SWITCH
    
    %% Conexiones a computadora
    ROUTER --> NET
    SWITCH --> NET
    
    %% Conexiones internas computadora
    NET --> CPU
    CPU --> RAM
    CPU --> GPU
    CPU --> STORAGE
    
    %% Conexiones de software
    CPU --> OPENCV
    CPU --> PIL
    CPU --> RTSP
    CPU --> HTTP
    
    %% Conexiones de almacenamiento
    OPENCV --> CAPTURES
    PIL --> CAPTURES
    RTSP --> CAPTURES
    HTTP --> LOGS
```

## 2. FLUJO DE DATOS EN TIEMPO REAL

### Timeline de Procesamiento Hardware
```mermaid
gantt
    title Timeline de Procesamiento Hardware (0-50ms)
    dateFormat X
    axisFormat %Lms
    
    section Cámaras
    Luz → Sensor     :0, 5
    Sensor → A/D     :5, 10
    A/D → Procesador :10, 15
    Procesador → H.264 :15, 20
    H.264 → Ethernet :20, 25
    
    section Red
    Ethernet → Router :25, 30
    Router → Switch   :30, 35
    Switch → PC      :35, 40
    
    section Computadora
    Red → CPU        :40, 45
    CPU → OpenCV     :45, 50
    OpenCV → Storage :50, 55
```

## 3. DIAGRAMA DE FLUJO DE SEÑALES

### Flujo de Señales desde la Luz hasta el Almacenamiento
```mermaid
flowchart LR
    subgraph "CAPTURA ÓPTICA"
        A[💡 LUZ AMBIENTE] --> B[🔭 LENTE ÓPTICO]
        B --> C[🔍 SENSOR CCD/CMOS]
    end
    
    subgraph "CONVERSIÓN"
        C --> D[⚡ CONVERSIÓN A/D]
        D --> E[🖥️ PROCESAMIENTO]
        E --> F[📦 COMPRESIÓN H.264]
    end
    
    subgraph "TRANSMISIÓN"
        F --> G[🌐 ETHERNET RTSP]
        G --> H[🔄 ROUTER]
        H --> I[🔌 SWITCH]
    end
    
    subgraph "PROCESAMIENTO"
        I --> J[💻 TARJETA RED]
        J --> K[🖥️ CPU]
        K --> L[🎮 GPU]
    end
    
    subgraph "SOFTWARE"
        L --> M[🔧 OpenCV]
        M --> N[🖼️ PIL]
        N --> O[💾 ALMACENAMIENTO]
    end
    
    style A fill:#ffff00
    style O fill:#00ff00
    style M fill:#00ffff
```

## 4. DIAGRAMA DE CONECTIVIDAD DE RED

### Topología de Red para Cámaras RTSP
```mermaid
graph TB
    subgraph "INTERNET"
        WAN[🌍 Internet<br/>WAN]
    end
    
    subgraph "RED LOCAL"
        ROUTER[🔄 Router<br/>94.125.136.1<br/>DHCP/NAT]
        SWITCH[🔌 Switch<br/>VLAN 10<br/>QoS Video]
    end
    
    subgraph "CÁMARAS RTSP"
        CAM1[📷 Cámara 1<br/>Recepción<br/>94.125.136.236:7447]
        CAM2[📷 Cámara 2<br/>Zaguan<br/>94.125.136.236:7447]
        CAM3[📷 Cámara 3<br/>Soporte<br/>94.125.136.236:7447]
        CAM4[📷 Cámara 4<br/>HelpDesk<br/>94.125.136.236:7447]
    end
    
    subgraph "COMPUTADORA"
        PC[💻 PC Central<br/>94.125.136.100<br/>Gigabit Ethernet]
    end
    
    WAN --> ROUTER
    ROUTER --> SWITCH
    SWITCH --> CAM1
    SWITCH --> CAM2
    SWITCH --> CAM3
    SWITCH --> CAM4
    SWITCH --> PC
    
    style ROUTER fill:#ff9999
    style SWITCH fill:#99ff99
    style PC fill:#9999ff
```

## 5. DIAGRAMA DE ESPECIFICACIONES TÉCNICAS

### Comparación de Hardware Mínimo vs Recomendado
```mermaid
graph LR
    subgraph "HARDWARE MÍNIMO"
        MIN_CPU[🖥️ CPU<br/>4 cores<br/>2.0 GHz]
        MIN_RAM[💾 RAM<br/>8GB<br/>DDR4]
        MIN_GPU[🎮 GPU<br/>Integrada]
        MIN_NET[🌐 Red<br/>Gigabit]
        MIN_STORAGE[💿 HDD<br/>500GB]
    end
    
    subgraph "HARDWARE RECOMENDADO"
        REC_CPU[🖥️ CPU<br/>8 cores<br/>3.0 GHz]
        REC_RAM[💾 RAM<br/>32GB<br/>DDR4]
        REC_GPU[🎮 GPU<br/>RTX 3060]
        REC_NET[🌐 Red<br/>2.5 Gigabit]
        REC_STORAGE[💿 NVMe SSD<br/>2TB]
    end
    
    MIN_CPU -.->|Mejora| REC_CPU
    MIN_RAM -.->|Mejora| REC_RAM
    MIN_GPU -.->|Mejora| REC_GPU
    MIN_NET -.->|Mejora| REC_NET
    MIN_STORAGE -.->|Mejora| REC_STORAGE
    
    style MIN_CPU fill:#ffcccc
    style REC_CPU fill:#ccffcc
```

## 6. DIAGRAMA DE ESTADOS DE CONEXIÓN

### Estados de Conexión de las Cámaras
```mermaid
stateDiagram-v2
    [*] --> Desconectado
    
    Desconectado --> Conectando : Conectar RTSP
    Conectando --> Conectado : Conexión exitosa
    Conectando --> Error : Fallo de conexión
    
    Conectado --> Transmitiendo : Iniciar Stream
    Transmitiendo --> Conectado : Detener Stream
    
    Conectado --> Desconectado : Desconectar
    Error --> Desconectado : Reset
    Error --> Conectando : Reintentar
    
    note right of Conectado : Estado estable<br/>Listo para captura
    note right of Transmitiendo : Transmisión<br/>en tiempo real
    note right of Error : Error de red<br/>o cámara
```

## 7. DIAGRAMA DE FLUJO DE CAPTURA

### Proceso de Captura de Imagen
```mermaid
flowchart TD
    START([🚀 Inicio]) --> INIT[⚙️ Inicializar<br/>Configurar cámaras]
    INIT --> CONNECT[🔌 Conectar<br/>RTSP]
    CONNECT --> CHECK{¿Conexión<br/>exitosa?}
    CHECK -->|No| RETRY[🔄 Reintentar]
    RETRY --> CONNECT
    CHECK -->|Sí| STREAM[📡 Stream<br/>Video activo]
    STREAM --> CAPTURE[📸 Capturar<br/>Frame]
    CAPTURE --> PROCESS[🔧 Procesar<br/>OpenCV]
    PROCESS --> SAVE[💾 Guardar<br/>JPEG]
    SAVE --> CONTINUE{¿Continuar<br/>capturando?}
    CONTINUE -->|Sí| CAPTURE
    CONTINUE -->|No| STOP([🛑 Fin])
    
    style START fill:#4caf50
    style STOP fill:#f44336
    style SAVE fill:#2196f3
    style ERROR fill:#ff9800
```

## 8. DIAGRAMA DE MONITOREO

### Sistema de Monitoreo y Logs
```mermaid
graph TB
    subgraph "MÉTRICAS EN TIEMPO REAL"
        FPS[📊 FPS Reales<br/>10 FPS objetivo]
        LATENCY[⏱️ Latencia<br/>< 50ms objetivo]
        QUALITY[🎯 Calidad<br/>1280x720 HD]
        BANDWIDTH[🌊 Ancho de banda<br/>100 Mbps/cámara]
    end
    
    subgraph "LOGS DEL SISTEMA"
        STATUS[📋 Estado<br/>Online/Offline/Error]
        CAPTURES[📸 Capturas<br/>Contador exitosas]
        ERRORS[❌ Errores<br/>Red/Timeout]
        RESOURCES[💻 Recursos<br/>CPU/RAM/Storage]
    end
    
    subgraph "ALERTAS"
        ALERT1[🚨 Cámara offline]
        ALERT2[⚠️ Latencia alta]
        ALERT3[💾 Espacio bajo]
        ALERT4[🌐 Error de red]
    end
    
    FPS --> STATUS
    LATENCY --> ERRORS
    QUALITY --> CAPTURES
    BANDWIDTH --> ERRORS
    
    STATUS --> ALERT1
    LATENCY --> ALERT2
    RESOURCES --> ALERT3
    ERRORS --> ALERT4
```

---

**Nota**: Estos diagramas Mermaid están optimizados para mostrar la arquitectura de hardware y pueden ser utilizados en:
- **GitHub/GitLab**: En archivos README.md
- **Notion**: Con soporte Mermaid
- **Documentación técnica**: Herramientas que soporten Mermaid
- **Presentaciones**: Exportando como imágenes
- **Mermaid Live Editor**: Para edición y visualización online
