"""
Configuración avanzada de logging para el sistema de cámaras RTSP
Maneja problemas de codificación en Windows
"""

import logging
import sys
import os
from pathlib import Path
from config.settings import LOGGING_CONFIG, DIRECTORIES

class UTF8StreamHandler(logging.StreamHandler):
    """
    Handler de logging que fuerza la codificación UTF-8
    Soluciona problemas de codificación en Windows
    """
    
    def emit(self, record):
        try:
            # Forzar codificación UTF-8 para la consola
            if hasattr(sys.stdout, 'reconfigure'):
                # Python 3.7+
                sys.stdout.reconfigure(encoding='utf-8')
            elif hasattr(sys.stdout, 'buffer'):
                # Fallback para versiones anteriores
                msg = self.format(record)
                sys.stdout.buffer.write(msg.encode('utf-8'))
                sys.stdout.buffer.write(b'\n')
                sys.stdout.buffer.flush()
                return
        except Exception:
            pass
        
        # Fallback al comportamiento normal
        super().emit(record)

def setup_logging(name, log_file=None, force_utf8=True):
    """
    Configura el sistema de logging con soporte UTF-8
    
    Args:
        name: Nombre del logger
        log_file: Archivo de log (opcional)
        force_utf8: Forzar codificación UTF-8 (por defecto True)
    
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
        
        # Handler para consola con codificación UTF-8
        if force_utf8 and sys.platform.startswith('win'):
            console_handler = UTF8StreamHandler()
        else:
            console_handler = logging.StreamHandler()
        
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Handler para archivo si se especifica
        if log_file:
            try:
                # Asegurar que el directorio de logs existe
                log_path = Path(log_file)
                log_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Usar codificación UTF-8 para archivos
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            except Exception as e:
                # Si falla el archivo, solo usar consola
                logger.warning(f"No se pudo configurar archivo de log: {e}")
    
    return logger

def configure_system_logging():
    """
    Configura el logging del sistema completo
    """
    # Configurar logging del sistema
    logging.basicConfig(
        level=getattr(logging, LOGGING_CONFIG['level']),
        format=LOGGING_CONFIG['format'],
        handlers=[]
    )
    
    # Crear logger principal del sistema
    system_logger = setup_logging(
        "CameraSystem",
        LOGGING_CONFIG['file'],
        force_utf8=True
    )
    
    # Configurar otros loggers importantes
    setup_logging("WebServer", DIRECTORIES['logs'] / 'web_server.log', force_utf8=True)
    setup_logging("CameraManager", DIRECTORIES['logs'] / 'camera_manager.log', force_utf8=True)
    
    return system_logger

def test_logging():
    """
    Prueba el sistema de logging
    """
    logger = setup_logging("TestLogger")
    
    logger.info("=== PRUEBA DE LOGGING ===")
    logger.info("Mensaje de prueba sin emojis")
    logger.info("Mensaje con caracteres especiales: áéíóú ñ")
    logger.info("Mensaje con números: 1234567890")
    logger.info("Mensaje con símbolos: !@#$%^&*()")
    
    print("✅ Logging configurado correctamente")
    print("📝 Revisa los archivos de log para verificar la codificación")

if __name__ == "__main__":
    test_logging()
