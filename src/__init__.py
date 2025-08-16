"""
Paquete principal del sistema de cámaras RTSP
"""

from .camera_manager import RTSPCamera, RTSPCameraManager
from .logging_config import setup_logging
from .utils import (
    generate_filename,
    save_capture,
    cleanup_old_files,
    get_storage_info,
    create_backup
)

__version__ = "1.0.0"
__author__ = "Sistema de Cámaras RTSP"

__all__ = [
    'RTSPCamera',
    'RTSPCameraManager',
    'setup_logging',
    'generate_filename',
    'save_capture',
    'cleanup_old_files',
    'get_storage_info',
    'create_backup'
]
