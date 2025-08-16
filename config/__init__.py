"""
Paquete de configuración del sistema de cámaras RTSP
"""

from .settings import (
    CAMERAS,
    WEB_SERVER_CONFIG,
    CAPTURE_CONFIG,
    STORAGE_CONFIG,
    LOGGING_CONFIG,
    NETWORK_CONFIG,
    DIRECTORIES,
    ensure_directories,
    get_capture_path,
    get_log_path,
    get_static_path,
    get_template_path
)

__all__ = [
    'CAMERAS',
    'WEB_SERVER_CONFIG',
    'CAPTURE_CONFIG',
    'STORAGE_CONFIG',
    'LOGGING_CONFIG',
    'NETWORK_CONFIG',
    'DIRECTORIES',
    'ensure_directories',
    'get_capture_path',
    'get_log_path',
    'get_static_path',
    'get_template_path'
]
