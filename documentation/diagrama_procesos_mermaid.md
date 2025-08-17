# Diagrama de Procesos Mermaid: Hardware de Visión por Computadora

## 1. DIAGRAMA DE FLUJO PRINCIPAL

### Flujo del Sistema Completo
```mermaid
flowchart TD
    A[LUZ AMBIENTE] --> B[LENTE ÓPTICO]
    B --> C[SENSOR CCD/CMOS]
    C --> D[CONVERSIÓN A/D]
    D --> E[PROCESAMIENTO]
    E --> F[COMPRESIÓN H.264]
    F --> G[INTERFAZ ETHERNET]
    G --> H[RED LOCAL]
    H --> I[COMPUTADORA]
    I --> J[DECODIFICACIÓN]
    J --> K[BUFFER FRAMES]
    K --> L[PROCESAMIENTO OPENCV]
    L --> M[ALMACENAMIENTO]
    M --> N[VISUALIZACIÓN]
    
    style A fill:#e1f5fe
    style M fill:#c8e6c9
    style N fill:#fff3e0
```

## 2. DIAGRAMA DE SECUENCIA

### Flujo de Datos en Tiempo Real
```mermaid
sequenceDiagram
    participant C1 as Cámara 1
    participant C2 as Cámara 2
    participant C3 as Cámara 3
    participant C4 as Cámara 4
    participant R as Red Local
    participant PC as Computadora
    participant S as Software
    participant A as Almacenamiento

    Note over C1,A: TIEMPO: 0ms
    C1->>C1: Captura LUZ
    C2->>C2: Captura LUZ
    C3->>C3: Captura LUZ
    C4->>C4: Captura LUZ
    
    Note over C1,A: TIEMPO: 10ms
    C1->>C1: Compresión H.264
    C2->>C2: Compresión H.264
    C3->>C3: Compresión H.264
    C4->>C4: Compresión H.264
    
    Note over C1,A: TIEMPO: 20ms
    C1->>R: Transmisión RTSP
    C2->>R: Transmisión RTSP
    C3->>R: Transmisión RTSP
    C4->>R: Transmisión RTSP
    
    Note over C1,A: TIEMPO: 30ms
    R->>PC: Recepción de datos
    PC->>PC: Decodificación
    
    Note over C1,A: TIEMPO: 40ms
    PC->>S: Procesamiento OpenCV
    S->>S: Resize/Filter
    
    Note over C1,A: TIEMPO: 50ms
    S->>A: Guardar imagen
    A->>A: Organizar por fecha/cámara
```

## 3. DIAGRAMA DE COMPONENTES

### Arquitectura del Sistema
```mermaid
graph TB
    subgraph "HARDWARE FÍSICO"
        subgraph "CÁMARAS RTSP"
            CAM1[Cámara 1<br/>Recepción]
            CAM2[Cámara 2<br/>Zaguan]
            CAM3[Cámara 3<br/>Soporte]
            CAM4[Cámara 4<br/>HelpDesk]
        end
        
        subgraph "COMPONENTES CÁMARA"
            SENSOR[Sensor<br/>CCD/CMOS]
            LENTE[Lente<br/>Óptico]
            PROC[Procesador<br/>de Imagen]
            COMP[Compresor<br/>H.264]
            ETH[Interfaz<br/>Ethernet]
        end
    end
    
    subgraph "RED LOCAL"
        ROUTER[Router<br/>DHCP/NAT/DNS]
        SWITCH[Switch<br/>VLAN/QoS/PoE]
    end
    
    subgraph "COMPUTADORA CENTRAL"
        CPU[CPU<br/>4+ cores]
        RAM[RAM<br/>16GB DDR4]
        GPU[GPU<br/>OpenCV/CUDA]
        STORAGE[Almacenamiento<br/>SSD/NVMe]
    end
    
    subgraph "SOFTWARE"
        OPENCV[OpenCV<br/>Video/Image/ML]
        PIL[PIL<br/>Image/Filter/Save]
        RTSP[RTSP Client<br/>Stream/Decode/Buffer]
        HTTP[HTTP Server<br/>Web/API/Files]
    end
    
    subgraph "ALMACENAMIENTO"
        CAPTURES[Captures<br/>Images/Video/Date]
        LOGS[Logs<br/>System/Camera/Error]
    end
    
    CAM1 --> SENSOR
    CAM2 --> SENSOR
    CAM3 --> SENSOR
    CAM4 --> SENSOR
    
    SENSOR --> LENTE
    LENTE --> PROC
    PROC --> COMP
    COMP --> ETH
    
    ETH --> ROUTER
    ETH --> SWITCH
    
    ROUTER --> CPU
    SWITCH --> CPU
    
    CPU --> RAM
    CPU --> GPU
    CPU --> STORAGE
    
    CPU --> OPENCV
    CPU --> PIL
    CPU --> RTSP
    CPU --> HTTP
    
    OPENCV --> CAPTURES
    PIL --> CAPTURES
    RTSP --> CAPTURES
    HTTP --> LOGS
```

## 4. DIAGRAMA DE FLUJO DETALLADO

### Proceso de Captura Completo
```mermaid
flowchart TD
    START([Inicio]) --> INIT[Inicialización<br/>Configuración de cámaras]
    INIT --> CONNECT[Conectar RTSP<br/>Establecer conexión]
    CONNECT --> STREAM[Stream de Video<br/>Recepción continua]
    STREAM --> CAPTURE[Captura de Frame<br/>Extraer del buffer]
    CAPTURE --> PROCESS[Procesamiento<br/>Resize/Filter/Conversión]
    PROCESS --> SAVE[Almacenamiento<br/>Guardar JPEG]
    SAVE --> CHECK{¿Continuar?}
    CHECK -->|Sí| CAPTURE
    CHECK -->|No| STOP([Fin])
    
    style START fill:#4caf50
    style STOP fill:#f44336
    style SAVE fill:#2196f3
```

## 5. DIAGRAMA DE CLASES

### Estructura del Software
```mermaid
classDiagram
    class RTSPCameraManager {
        +list_cameras()
        +connect_all_cameras()
        +disconnect_all_cameras()
        +capture_from_all_cameras()
        +get_status_summary()
    }
    
    class RTSPCamera {
        +camera_id
        +rtsp_url
        +camera_name
        +connected
        +is_streaming
        +connect()
        +capture_image()
        +start_stream()
        +disconnect()
    }
    
    class OpenCVCamera {
        +rtsp_url
        +camera_id
        +cap
        +is_running
        +start_capture()
        +stop_capture()
        +read_frame()
        +get_camera_info()
    }
    
    class OpenCVStream {
        +camera_id
        +rtsp_url
        +cap
        +is_running
        +start()
        +stop()
        +get_frame()
    }
    
    RTSPCameraManager --> RTSPCamera : manages
    RTSPCamera --> OpenCVCamera : uses
    RTSPCamera --> OpenCVStream : optional
```

## 6. DIAGRAMA DE ESTADOS

### Estados de la Cámara
```mermaid
stateDiagram-v2
    [*] --> Offline
    Offline --> Connecting : connect()
    Connecting --> Online : success
    Connecting --> Error : failed
    Online --> Streaming : start_stream()
    Streaming --> Online : stop_stream()
    Online --> Offline : disconnect()
    Error --> Offline : reset
    Error --> Connecting : retry
    
    note right of Online : Captura activa
    note right of Streaming : Transmisión en tiempo real
    note right of Error : Error de conexión
```

## 7. DIAGRAMA DE ENTIDAD-RELACIÓN

### Estructura de Datos
```mermaid
erDiagram
    CAMERA {
        string camera_id PK
        string name
        string rtsp_url
        string status
        datetime last_capture
        boolean stream_active
    }
    
    CAPTURE {
        string capture_id PK
        string camera_id FK
        datetime timestamp
        string filename
        string capture_type
        string subdirectory
    }
    
    LOG {
        string log_id PK
        string camera_id FK
        string level
        string message
        datetime timestamp
    }
    
    CAMERA ||--o{ CAPTURE : "generates"
    CAMERA ||--o{ LOG : "produces"
```

## 8. DIAGRAMA DE TIMELINE

### Timeline de Procesamiento
```mermaid
gantt
    title Timeline de Procesamiento de Imágenes
    dateFormat X
    axisFormat %Lms
    
    section Captura
    Luz Ambiente     :0, 5
    Sensor CCD/CMOS  :5, 10
    Conversión A/D   :10, 15
    
    section Compresión
    Procesamiento    :15, 20
    Compresión H.264 :20, 25
    Transmisión      :25, 30
    
    section Red
    Router           :30, 35
    Switch           :35, 40
    
    section Computadora
    Decodificación   :40, 45
    Procesamiento    :45, 50
    Almacenamiento   :50, 55
```

---

**Nota**: Estos diagramas Mermaid pueden ser utilizados en plataformas que soporten la sintaxis Mermaid como:
- GitHub (en archivos .md)
- GitLab
- Notion
- Mermaid Live Editor (online)
- Herramientas de documentación técnica
