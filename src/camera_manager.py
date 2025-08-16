"""
Gestor de cámaras RTSP
"""

import threading
import time
from datetime import datetime
from config.settings import CAMERAS, CAPTURE_CONFIG, get_capture_path
from src.logging_config import setup_logging
from src.utils import save_capture

# Importar utilidades de OpenCV
from .opencv_utils import OpenCVCamera, save_frame_to_file, show_frame_preview

class RTSPCamera:
    """
    Clase para manejar una cámara RTSP individual
    """
    
    def __init__(self, camera_id, rtsp_url, camera_name):
        """
        Inicializa la cámara RTSP
        
        Args:
            camera_id: ID de la cámara
            rtsp_url: URL RTSP de la cámara
            camera_name: Nombre descriptivo de la cámara
        """
        self.camera_id = camera_id
        self.rtsp_url = rtsp_url
        self.camera_name = camera_name
        self.opencv_camera = OpenCVCamera(rtsp_url, camera_id)
        self.connected = False
        self.is_streaming = False
        self.logger = setup_logging(f"Camera_{camera_id}")
        
    def connect(self):
        """
        Conecta a la cámara RTSP
        
        Returns:
            bool: True si la conexión fue exitosa
        """
        try:
            self.logger.info(f"Conectando a: {self.camera_name}")
            self.logger.info(f"URL: {self.rtsp_url}")
            
            # Conectar usando la librería OpenCV
            if self.opencv_camera.start_capture(
                buffer_size=CAPTURE_CONFIG['buffer_size'],
                fps=CAPTURE_CONFIG['default_fps']
            ):
            
                self.connected = True
                CAMERAS[self.camera_id]['status'] = 'online'
                
                # Obtener información de la cámara
                camera_info = self.opencv_camera.get_camera_info()
                width = camera_info.get('width', 0)
                height = camera_info.get('height', 0)
                fps = camera_info.get('fps', 0)
                
                self.logger.info(f"Conexión exitosa - Resolución: {width}x{height}, FPS: {fps:.1f}")
                return True
            else:
                self.connected = False
                CAMERAS[self.camera_id]['status'] = 'error'
                self.logger.error("No se pudo conectar a la cámara RTSP")
                return False
                
        except Exception as e:
            self.connected = False
            CAMERAS[self.camera_id]['status'] = 'error'
            self.logger.error(f"Error al conectar: {e}")
            return False
    
    def capture_image(self, save_path=None, show_preview=False, capture_type="single"):
        """
        Captura una imagen desde la cámara
        
        Args:
            save_path: Ruta donde guardar (opcional)
            show_preview: Mostrar vista previa
            capture_type: Tipo de captura
            
        Returns:
            dict: Resultado de la captura
        """
        if not self.connected:
            return {'success': False, 'error': 'No hay conexión activa con la cámara'}
        
        try:
            # Capturar frame usando la librería OpenCV
            frame = self.opencv_camera.read_frame()
            
            if frame is None:
                return {'success': False, 'error': 'No se pudo capturar frame de la cámara'}
            
            # Mostrar vista previa si se solicita
            if show_preview:
                show_frame_preview(frame, f'Vista Previa - {self.camera_name}')
            
            # Guardar imagen usando el sistema centralizado
            if save_path:
                # Guardar en ruta específica
                success = save_frame_to_file(frame, save_path, quality=95)
                if success:
                    CAMERAS[self.camera_id]['last_capture'] = datetime.now().strftime('%Y%m%d_%H%M%S')
                    return {
                        'success': True,
                        'filename': save_path,
                        'frame': frame
                    }
                else:
                    return {'success': False, 'error': f'Error al guardar en {save_path}'}
            else:
                # Guardar usando el sistema centralizado
                result = save_capture(frame, self.camera_id, self.camera_name, capture_type)
                if result['success']:
                    CAMERAS[self.camera_id]['last_capture'] = datetime.now().strftime('%Y%m%d_%H%M%S')
                
                return result
            
        except Exception as e:
            self.logger.error(f"Error al capturar imagen: {e}")
            return {'success': False, 'error': str(e)}
    
    def capture_multiple(self, count=5, delay=2, subdirectory="multiple"):
        """
        Captura múltiples imágenes con delay
        
        Args:
            count: Número de imágenes a capturar
            delay: Delay entre capturas en segundos
            subdirectory: Subdirectorio donde guardar
        """
        if not self.connected:
            self.logger.error("No hay conexión activa con la cámara")
            return
        
        self.logger.info(f"Capturando {count} imágenes con delay de {delay} segundos...")
        
        captured_count = 0
        
        for i in range(count):
            self.logger.info(f"Capturando imagen {i+1}/{count}...")
            
            # Capturar imagen
            result = self.capture_image(capture_type="multiple", index=i+1, subdirectory=subdirectory)
            
            if result['success']:
                captured_count += 1
                self.logger.info(f"Imagen {i+1} guardada: {result['filename']}")
                
                # Esperar antes de la siguiente captura (excepto la última)
                if i < count - 1:
                    time.sleep(delay)
            else:
                self.logger.error(f"Error en imagen {i+1}: {result['error']}")
        
        self.logger.info(f"Captura múltiple completada: {captured_count}/{count} imágenes guardadas")
        return captured_count
    
    def continuous_capture(self, duration=30, subdirectory="continuous"):
        """
        Captura continua durante un tiempo específico
        
        Args:
            duration: Duración de la captura en segundos
            subdirectory: Subdirectorio donde guardar
        """
        if not self.connected:
            self.logger.error("No hay conexión activa con la cámara")
            return
        
        self.logger.info(f"Captura continua por {duration} segundos...")
        
        start_time = time.time()
        captured_count = 0
        
        try:
            while time.time() - start_time < duration:
                # Capturar imagen
                result = self.capture_image(capture_type="continuous", subdirectory=subdirectory)
                
                if result['success']:
                    captured_count += 1
                    elapsed = time.time() - start_time
                    self.logger.info(f"Captura {captured_count} - Tiempo: {elapsed:.1f}s / {duration}s")
                
                # Pausa entre capturas
                time.sleep(CAPTURE_CONFIG['capture_delay'])
                
        except KeyboardInterrupt:
            self.logger.info("Captura interrumpida por el usuario")
        
        total_time = time.time() - start_time
        self.logger.info(f"Captura continua completada:")
        self.logger.info(f"  Imágenes capturadas: {captured_count}")
        self.logger.info(f"  Tiempo total: {total_time:.1f} segundos")
        self.logger.info(f"  Velocidad: {captured_count/total_time:.1f} imágenes/segundo")
        
        return captured_count
    
    def start_stream(self):
        """
        Inicia el stream de la cámara
        """
        if not self.connected:
            self.logger.error("No hay conexión activa con la cámara")
            return False
        
        self.is_streaming = True
        CAMERAS[self.camera_id]['stream_active'] = True
        self.logger.info("Stream iniciado")
        return True
    
    def stop_stream(self):
        """
        Detiene el stream de la cámara
        """
        self.is_streaming = False
        CAMERAS[self.camera_id]['stream_active'] = False
        self.logger.info("Stream detenido")
    
    def get_frame(self):
        """
        Obtiene el frame actual de la cámara
        
        Returns:
            numpy.ndarray: Frame de la cámara o None si no está disponible
        """
        if not self.connected or self.cap is None:
            return None
        
        try:
            ret, frame = self.cap.read()
            if ret:
                return frame
            else:
                return None
        except Exception as e:
            self.logger.error(f"Error obteniendo frame: {e}")
            return None
    
    def disconnect(self):
        """
        Desconecta de la cámara
        """
        self.opencv_camera.stop_capture()
        
        self.connected = False
        self.is_streaming = False
        CAMERAS[self.camera_id]['status'] = 'offline'
        CAMERAS[self.camera_id]['stream_active'] = False
        
        self.logger.info("Desconectado de la cámara")
    
    def __enter__(self):
        """
        Context manager para usar 'with'
        """
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager para usar 'with'
        """
        self.disconnect()

class RTSPCameraManager:
    """
    Gestor de múltiples cámaras RTSP
    """
    
    def __init__(self):
        """
        Inicializa el gestor de cámaras
        """
        self.cameras = {}
        self.logger = setup_logging("CameraManager")
        
        # Crear instancias de cámaras
        for camera_id, camera_info in CAMERAS.items():
            self.cameras[camera_id] = RTSPCamera(
                camera_id,
                camera_info['url'],
                camera_info['name']
            )
    
    def list_cameras(self):
        """
        Lista todas las cámaras disponibles
        """
        self.logger.info("=== CÁMARAS RTSP DISPONIBLES ===")
        for camera_id, camera_info in CAMERAS.items():
            self.logger.info(f"{camera_id}. {camera_info['name']}")
            self.logger.info(f"   URL: {camera_info['url']}")
            self.logger.info(f"   Estado: {camera_info['status']}")
    
    def connect_all_cameras(self):
        """
        Conecta a todas las cámaras disponibles
        """
        self.logger.info("Conectando a todas las cámaras...")
        
        for camera_id, camera in self.cameras.items():
            try:
                camera.connect()
                time.sleep(1)  # Pausa entre conexiones
            except Exception as e:
                self.logger.error(f"Error conectando cámara {camera_id}: {e}")
    
    def disconnect_all_cameras(self):
        """
        Desconecta de todas las cámaras
        """
        self.logger.info("Desconectando de todas las cámaras...")
        
        for camera in self.cameras.values():
            try:
                camera.disconnect()
            except Exception as e:
                self.logger.error(f"Error desconectando cámara: {e}")
    
    def capture_from_all_cameras(self, subdirectory="all_cameras"):
        """
        Captura una imagen desde todas las cámaras disponibles
        
        Args:
            subdirectory: Subdirectorio donde guardar las capturas
        """
        self.logger.info("=== CAPTURA DESDE TODAS LAS CÁMARAS ===")
        
        captured_count = 0
        total_cameras = len(self.cameras)
        
        for camera_id, camera in self.cameras.items():
            self.logger.info(f"Conectando a {camera.camera_name}...")
            
            try:
                if camera.connected or camera.connect():
                    # Capturar imagen
                    result = camera.capture_image(capture_type="web", subdirectory=subdirectory)
                    
                    if result['success']:
                        captured_count += 1
                        self.logger.info(f"Imagen capturada desde {camera.camera_name}")
                    else:
                        self.logger.error(f"Error al capturar desde {camera.camera_name}: {result['error']}")
                else:
                    self.logger.error(f"No se pudo conectar a {camera.camera_name}")
                    
            except Exception as e:
                self.logger.error(f"Error con {camera.camera_name}: {e}")
        
        self.logger.info(f"Captura completada: {captured_count}/{total_cameras} cámaras exitosas")
        return captured_count
    
    def get_camera(self, camera_id):
        """
        Obtiene una cámara específica
        
        Args:
            camera_id: ID de la cámara
            
        Returns:
            RTSPCamera: Instancia de la cámara o None si no existe
        """
        return self.cameras.get(camera_id)
    
    def get_status_summary(self):
        """
        Obtiene un resumen del estado de todas las cámaras
        
        Returns:
            dict: Resumen del estado
        """
        summary = {
            'total_cameras': len(self.cameras),
            'online_cameras': 0,
            'offline_cameras': 0,
            'error_cameras': 0,
            'streaming_cameras': 0,
            'cameras': {}
        }
        
        for camera_id, camera in self.cameras.items():
            status = CAMERAS[camera_id]['status']
            summary['cameras'][camera_id] = {
                'name': camera.camera_name,
                'status': status,
                'stream_active': CAMERAS[camera_id]['stream_active'],
                'last_capture': CAMERAS[camera_id]['last_capture']
            }
            
            if status == 'online':
                summary['online_cameras'] += 1
            elif status == 'offline':
                summary['offline_cameras'] += 1
            elif status == 'error':
                summary['error_cameras'] += 1
            
            if CAMERAS[camera_id]['stream_active']:
                summary['streaming_cameras'] += 1
        
        return summary
