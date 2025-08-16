"""
Utilidades del sistema de cámaras RTSP
"""

import os
import logging
import shutil
from datetime import datetime
from pathlib import Path
from config.settings import STORAGE_CONFIG, DIRECTORIES, get_capture_path

# Importar utilidades de OpenCV
from .opencv_utils import save_frame_to_file

def setup_logging_legacy(name, log_file=None):
    """
    Configura el sistema de logging
    
    Args:
        name: Nombre del logger
        log_file: Archivo de log (opcional)
    
    Returns:
        Logger: Logger configurado
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Formato del log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Handler para archivo si se especifica
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
    
    return logger

def generate_filename(camera_id, camera_name, capture_type="single", index=None):
    """
    Genera un nombre de archivo para las capturas
    
    Args:
        camera_id: ID de la cámara
        camera_name: Nombre de la cámara
        capture_type: Tipo de captura (single, multiple, continuous, web)
        index: Índice para capturas múltiples (opcional)
    
    Returns:
        str: Nombre del archivo generado
    """
    timestamp = datetime.now().strftime(STORAGE_CONFIG['file_naming']['timestamp_format'])
    
    # Limpiar nombre de cámara para usar en archivo
    safe_name = camera_name.replace(" ", "_").replace(":", "_")
    
    if capture_type == "single":
        return f"{safe_name}_{timestamp}.jpg"
    elif capture_type == "multiple":
        return f"{safe_name}_{timestamp}_{index:02d}.jpg"
    elif capture_type == "continuous":
        return f"{safe_name}_continuous_{timestamp}.jpg"
    elif capture_type == "web":
        return f"web_cam_{camera_id}_{timestamp}.jpg"
    else:
        return f"{safe_name}_{capture_type}_{timestamp}.jpg"

def save_capture(frame, camera_id, camera_name, capture_type="single", index=None, subdirectory=None):
    """
    Guarda una captura en el directorio correspondiente
    
    Args:
        frame: Frame de OpenCV a guardar
        camera_id: ID de la cámara
        camera_name: Nombre de la cámara
        capture_type: Tipo de captura
        index: Índice para capturas múltiples
        subdirectory: Subdirectorio adicional
    
    Returns:
        dict: Resultado de la operación
    """
    try:
        # Generar nombre de archivo
        filename = generate_filename(camera_id, camera_name, capture_type, index)
        
        # Obtener ruta de guardado
        filepath = get_capture_path(camera_id, filename, subdirectory)
        
        # Guardar imagen usando la librería OpenCV
        success = save_frame_to_file(frame, str(filepath), quality=95)
        
        if success:
            return {
                'success': True,
                'filename': filename,
                'filepath': str(filepath),
                'size': filepath.stat().st_size if filepath.exists() else 0
            }
        else:
            return {
                'success': False,
                'error': 'Error al guardar imagen con OpenCV'
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def cleanup_old_files(camera_id, max_files=None):
    """
    Limpia archivos antiguos de una cámara específica
    
    Args:
        camera_id: ID de la cámara
        max_files: Número máximo de archivos a mantener
    
    Returns:
        int: Número de archivos eliminados
    """
    if max_files is None:
        max_files = STORAGE_CONFIG['max_files_per_camera']
    
    try:
        # Obtener directorio de capturas
        capture_dir = get_capture_path(camera_id)
        
        # Buscar archivos de la cámara
        camera_files = []
        for file_path in capture_dir.rglob(f"*cam_{camera_id}*"):
            if file_path.is_file():
                camera_files.append(file_path)
        
        # Ordenar por fecha de modificación (más reciente primero)
        camera_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Eliminar archivos excedentes
        files_to_delete = camera_files[max_files:]
        deleted_count = 0
        
        for file_path in files_to_delete:
            try:
                file_path.unlink()
                deleted_count += 1
            except Exception as e:
                print(f"Error eliminando archivo {file_path}: {e}")
        
        return deleted_count
        
    except Exception as e:
        print(f"Error en limpieza de archivos: {e}")
        return 0

def get_storage_info():
    """
    Obtiene información del almacenamiento
    
    Returns:
        dict: Información del almacenamiento
    """
    try:
        captures_dir = DIRECTORIES['captures']
        
        total_files = 0
        total_size = 0
        files_by_camera = {}
        
        for file_path in captures_dir.rglob("*.jpg"):
            if file_path.is_file():
                total_files += 1
                total_size += file_path.stat().st_size
                
                # Contar por cámara
                filename = file_path.name
                if "cam_1" in filename:
                    files_by_camera['1'] = files_by_camera.get('1', 0) + 1
                elif "cam_2" in filename:
                    files_by_camera['2'] = files_by_camera.get('2', 0) + 1
                elif "cam_3" in filename:
                    files_by_camera['3'] = files_by_camera.get('3', 0) + 1
                elif "cam_4" in filename:
                    files_by_camera['4'] = files_by_camera.get('4', 0) + 1
        
        return {
            'total_files': total_files,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'files_by_camera': files_by_camera,
            'directory': str(captures_dir)
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'total_files': 0,
            'total_size_mb': 0,
            'files_by_camera': {},
            'directory': str(DIRECTORIES['captures'])
        }

def create_backup():
    """
    Crea una copia de seguridad del directorio de capturas
    
    Returns:
        str: Ruta del archivo de backup
    """
    try:
        from datetime import datetime
        
        # Crear directorio de backups si no existe
        backup_dir = DIRECTORIES['captures'].parent / 'backups'
        backup_dir.mkdir(exist_ok=True)
        
        # Nombre del archivo de backup
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"captures_backup_{timestamp}.zip"
        backup_path = backup_dir / backup_filename
        
        # Crear archivo ZIP
        import zipfile
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in DIRECTORIES['captures'].rglob("*.jpg"):
                zipf.write(file_path, file_path.relative_to(DIRECTORIES['captures']))
        
        return str(backup_path)
        
    except Exception as e:
        print(f"Error creando backup: {e}")
        return None
