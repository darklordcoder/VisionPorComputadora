"""
Utilidades de OpenCV para el sistema de cámaras RTSP
"""

import cv2
import numpy as np
from typing import Optional, Tuple, Dict, Any
import logging

logger = logging.getLogger(__name__)

class OpenCVCamera:
    """Clase para manejar cámaras usando OpenCV"""
    
    def __init__(self, rtsp_url: str, camera_id: str = None):
        self.rtsp_url = rtsp_url
        self.camera_id = camera_id
        self.cap = None
        self.is_running = False
        self.frame = None
        self.frame_lock = None
        
    def start_capture(self, buffer_size: int = 1, fps: int = 10) -> bool:
        """Inicia la captura de video desde la cámara RTSP"""
        try:
            self.cap = cv2.VideoCapture(self.rtsp_url)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)
            self.cap.set(cv2.CAP_PROP_FPS, fps)
            
            if self.cap.isOpened():
                self.is_running = True
                logger.info(f"Cámara {self.camera_id} iniciada exitosamente")
                return True
            else:
                logger.error(f"No se pudo abrir la cámara {self.camera_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error iniciando cámara {self.camera_id}: {e}")
            return False
    
    def stop_capture(self):
        """Detiene la captura de video"""
        self.is_running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        logger.info(f"Cámara {self.camera_id} detenida")
    
    def read_frame(self) -> Optional[np.ndarray]:
        """Lee un frame de la cámara"""
        if not self.cap or not self.is_running:
            return None
            
        try:
            ret, frame = self.cap.read()
            if ret:
                return frame
            else:
                return None
        except Exception as e:
            logger.error(f"Error leyendo frame de cámara {self.camera_id}: {e}")
            return None
    
    def get_camera_info(self) -> Dict[str, Any]:
        """Obtiene información de la cámara"""
        if not self.cap:
            return {}
            
        try:
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            
            return {
                'width': width,
                'height': height,
                'fps': fps,
                'is_opened': self.cap.isOpened()
            }
        except Exception as e:
            logger.error(f"Error obteniendo información de cámara {self.camera_id}: {e}")
            return {}

class OpenCVStream:
    """Clase para manejar streams de video usando OpenCV"""
    
    def __init__(self, camera_id: str, rtsp_url: str):
        self.camera_id = camera_id
        self.rtsp_url = rtsp_url
        self.cap = None
        self.is_running = False
        self.frame = None
        
    def start(self) -> bool:
        """Inicia el stream de la cámara"""
        try:
            self.cap = cv2.VideoCapture(self.rtsp_url)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            self.cap.set(cv2.CAP_PROP_FPS, 10)
            
            if self.cap.isOpened():
                self.is_running = True
                logger.info(f"Stream de cámara {self.camera_id} iniciado")
                return True
            else:
                logger.error(f"No se pudo abrir stream de cámara {self.camera_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error iniciando stream de cámara {self.camera_id}: {e}")
            return False
    
    def stop(self):
        """Detiene el stream de la cámara"""
        self.is_running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        logger.info(f"Stream de cámara {self.camera_id} detenido")
    
    def get_frame(self) -> Optional[np.ndarray]:
        """Obtiene el frame actual del stream"""
        if not self.cap or not self.is_running:
            return None
            
        try:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame
                return frame.copy()
            else:
                return None
        except Exception as e:
            logger.error(f"Error obteniendo frame de stream {self.camera_id}: {e}")
            return None

def encode_frame_to_jpeg(frame: np.ndarray, quality: int = 80) -> Optional[bytes]:
    """Codifica un frame a formato JPEG"""
    try:
        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
        if ret:
            return buffer.tobytes()
        else:
            logger.error("Error codificando frame a JPEG")
            return None
    except Exception as e:
        logger.error(f"Error en encode_frame_to_jpeg: {e}")
        return None

def save_frame_to_file(frame: np.ndarray, filepath: str, quality: int = 95) -> bool:
    """Guarda un frame como imagen"""
    try:
        # Configurar parámetros de compresión JPEG
        encode_params = [cv2.IMWRITE_JPEG_QUALITY, quality]
        success = cv2.imwrite(str(filepath), frame, encode_params)
        
        if success:
            logger.info(f"Frame guardado exitosamente en {filepath}")
            return True
        else:
            logger.error(f"Error guardando frame en {filepath}")
            return False
            
    except Exception as e:
        logger.error(f"Error en save_frame_to_file: {e}")
        return False

def show_frame_preview(frame: np.ndarray, window_name: str = "Vista Previa"):
    """Muestra una vista previa del frame en una ventana"""
    try:
        cv2.imshow(window_name, frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except Exception as e:
        logger.error(f"Error mostrando vista previa: {e}")

def resize_frame(frame: np.ndarray, width: int, height: int) -> np.ndarray:
    """Redimensiona un frame a las dimensiones especificadas"""
    try:
        return cv2.resize(frame, (width, height))
    except Exception as e:
        logger.error(f"Error redimensionando frame: {e}")
        return frame

def convert_frame_format(frame: np.ndarray, target_format: str) -> Optional[np.ndarray]:
    """Convierte un frame a un formato específico"""
    try:
        if target_format.lower() == 'bgr':
            return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        elif target_format.lower() == 'rgb':
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        elif target_format.lower() == 'gray':
            return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            logger.warning(f"Formato de conversión no soportado: {target_format}")
            return frame
    except Exception as e:
        logger.error(f"Error convirtiendo formato de frame: {e}")
        return None

def get_frame_dimensions(frame: np.ndarray) -> Tuple[int, int]:
    """Obtiene las dimensiones de un frame"""
    try:
        height, width = frame.shape[:2]
        return width, height
    except Exception as e:
        logger.error(f"Error obteniendo dimensiones de frame: {e}")
        return 0, 0

def is_frame_valid(frame: np.ndarray) -> bool:
    """Verifica si un frame es válido"""
    try:
        return frame is not None and frame.size > 0 and frame.shape[0] > 0 and frame.shape[1] > 0
    except Exception as e:
        logger.error(f"Error verificando validez de frame: {e}")
        return False
