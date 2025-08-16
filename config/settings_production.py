"""
Configuración de producción para Docker
"""

import os
from pathlib import Path

# Directorio raíz del proyecto (dentro del contenedor)
PROJECT_ROOT = Path('/app')

# Configuración de directorios para Docker
DIRECTORIES = {
    'captures': PROJECT_ROOT / 'captures',
    'logs': PROJECT_ROOT / 'logs',
    'static': PROJECT_ROOT / 'static',
    'templates': PROJECT_ROOT / 'templates',
    'src': PROJECT_ROOT / 'src'
}

# Configuración de las cámaras RTSP
CAMERAS = {
    '1': {
        'name': 'Recepcion',
        'url': 'rtsp://94.125.136.236:7447/4c37181c-71a1-3d56-8a0a-e317d75a2ae0_0',
        'status': 'offline',
        'last_capture': None,
        'stream_active': False
    },
    '2': {
        'name': 'Zaguan',
        'url': 'rtsp://94.125.136.236:7447/17d114c7-2b41-351b-b145-b81b2fe90d7a_0',
        'status': 'offline',
        'last_capture': None,
        'stream_active': False
    },
    '3': {
        'name': 'Soporte',
        'url': 'rtsp://94.125.136.236:7447/5c106a76-53bc-3681-bff8-c622c26afe46_0',
        'status': 'offline',
        'last_capture': None,
        'stream_active': False
    },
    '4': {
        'name': 'HelpDesk',
        'url': 'rtsp://94.125.136.236:7447/aa478186-ee99-396b-90f6-2f223b7a8d08_0',
        'status': 'offline',
        'last_capture': None,
        'stream_active': False
    }
}

# Configuración del servidor web para producción
WEB_SERVER_CONFIG = {
    'host': '0.0.0.0',  # Importante para Docker
    'port': 5000,
    'debug': False,      # False en producción
    'capture_dir': str(DIRECTORIES['captures']),
    'log_dir': str(DIRECTORIES['logs'])
}

# Configuración de captura optimizada para Docker
CAPTURE_CONFIG = {
    'default_format': 'jpg',
    'default_quality': 85,  # Calidad reducida para mejor rendimiento
    'default_resolution': (1280, 720),
    'default_fps': 10,
    'buffer_size': 1,
    'capture_delay': 0.5,
    'max_retries': 3
}

# Configuración de almacenamiento para Docker
STORAGE_CONFIG = {
    'base_dir': str(DIRECTORIES['captures']),
    'organize_by_date': True,
    'date_format': '%Y%m%d',
    'max_files_per_camera': 500,  # Reducido para servidor compartido
    'cleanup_old_files': True,
    'file_naming': {
        'prefix': 'cam',
        'include_timestamp': True,
        'include_camera_id': True,
        'timestamp_format': '%Y%m%d_%H%M%S'
    }
}

# Configuración de logging para Docker
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': str(DIRECTORIES['logs'] / 'camera_system.log'),
    'max_size': 5 * 1024 * 1024,  # 5MB (reducido para servidor compartido)
    'backup_count': 3,
    'console_output': True
}

# Configuración de red para Docker
NETWORK_CONFIG = {
    'rtsp_ip': '94.125.136.236',
    'rtsp_port': 7447,
    'timeout': 30,
    'retry_attempts': 3
}

# Configuración de seguridad para producción
SECURITY_CONFIG = {
    'enable_cors': False,
    'max_file_size': 50 * 1024 * 1024,  # 50MB
    'allowed_extensions': ['.jpg', '.jpeg', '.png'],
    'rate_limit': {
        'enabled': True,
        'requests_per_minute': 60
    }
}

# Configuración de rendimiento para Docker
PERFORMANCE_CONFIG = {
    'worker_threads': 4,
    'max_connections': 100,
    'connection_timeout': 60,
    'keep_alive': True,
    'compression': True
}
