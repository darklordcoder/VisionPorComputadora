"""
Configuración centralizada del sistema de cámaras RTSP
"""

import os
from pathlib import Path

# Directorio raíz del proyecto
PROJECT_ROOT = Path(__file__).parent.parent

# Configuración de directorios
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

# Configuración del servidor web
WEB_SERVER_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': False,
    'capture_dir': str(DIRECTORIES['captures']),
    'log_dir': str(DIRECTORIES['logs'])
}

# Configuración de captura
CAPTURE_CONFIG = {
    'default_format': 'jpg',
    'default_quality': 95,
    'default_resolution': (1280, 720),
    'default_fps': 10,
    'buffer_size': 1,
    'capture_delay': 0.5,
    'max_retries': 3
}

# Configuración de almacenamiento
STORAGE_CONFIG = {
    'base_dir': str(DIRECTORIES['captures']),
    'organize_by_date': True,
    'date_format': '%Y%m%d',
    'max_files_per_camera': 1000,
    'cleanup_old_files': True,
    'file_naming': {
        'prefix': 'cam',
        'include_timestamp': True,
        'include_camera_id': True,
        'timestamp_format': '%Y%m%d_%H%M%S'
    }
}

# Configuración de logging
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': str(DIRECTORIES['logs'] / 'camera_system.log'),
    'max_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5,
    'console_output': True
}

# Configuración de red
NETWORK_CONFIG = {
    'rtsp_ip': '94.125.136.236',
    'rtsp_port': 7447,
    'connection_timeout': 10,
    'retry_interval': 5,
    'max_connections': 4
}

def ensure_directories():
    """Crea todos los directorios necesarios si no existen"""
    for dir_path in DIRECTORIES.values():
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Directorio creado/verificado: {dir_path}")

def get_capture_path(camera_id, filename=None, subdirectory=None):
    """
    Obtiene la ruta completa para guardar capturas
    
    Args:
        camera_id: ID de la cámara
        filename: Nombre del archivo (opcional)
        subdirectory: Subdirectorio adicional (opcional)
    
    Returns:
        Path: Ruta completa del directorio o archivo
    """
    base_path = DIRECTORIES['captures']
    
    if STORAGE_CONFIG['organize_by_date']:
        from datetime import datetime
        date_dir = datetime.now().strftime(STORAGE_CONFIG['date_format'])
        base_path = base_path / date_dir
    
    if subdirectory:
        base_path = base_path / subdirectory
    
    # Crear directorio si no existe
    base_path.mkdir(parents=True, exist_ok=True)
    
    if filename:
        return base_path / filename
    
    return base_path

def get_log_path(filename):
    """Obtiene la ruta completa para archivos de log"""
    return DIRECTORIES['logs'] / filename

def get_static_path(filename):
    """Obtiene la ruta completa para archivos estáticos"""
    return DIRECTORIES['static'] / filename

def get_template_path(filename):
    """Obtiene la ruta completa para plantillas"""
    return DIRECTORIES['templates'] / filename

# Crear directorios al importar el módulo
ensure_directories()
