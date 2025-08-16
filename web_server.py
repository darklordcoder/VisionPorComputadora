"""
Servidor Web para Control y Monitoreo de Cámaras RTSP
"""

from flask import Flask, render_template, jsonify, request, Response, send_file
import os
import threading
import time
from datetime import datetime
import json
import base64
from io import BytesIO
from PIL import Image
import numpy as np

# Importar utilidades de OpenCV
from src.opencv_utils import OpenCVStream, encode_frame_to_jpeg

# Importar configuración y módulos del sistema
from config.settings import CAMERAS, WEB_SERVER_CONFIG, DIRECTORIES
from src.camera_manager import RTSPCameraManager
from src.logging_config import setup_logging
from src.utils import get_storage_info, save_capture

app = Flask(__name__)

# Configurar logging
logger = setup_logging("WebServer", WEB_SERVER_CONFIG['log_dir'] + '/web_server.log')

# Configuraciones adicionales para desarrollo
if WEB_SERVER_CONFIG['debug']:
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE'] = 0
    logger.info("Modo DEBUG habilitado - Los templates se recargan automáticamente")

# Crear gestor de cámaras
camera_manager = RTSPCameraManager()

# Instancias de streams de cámaras
camera_streams = {}

class CameraStream:
    """Clase para manejar streams de cámaras RTSP usando OpenCV"""
    
    def __init__(self, camera_id, rtsp_url):
        self.camera_id = camera_id
        self.rtsp_url = rtsp_url
        self.opencv_stream = OpenCVStream(camera_id, rtsp_url)
        self.lock = threading.Lock()
    
    def start(self):
        """Inicia el stream de la cámara"""
        try:
            if self.opencv_stream.start():
                CAMERAS[self.camera_id]['status'] = 'online'
                CAMERAS[self.camera_id]['stream_active'] = True
                
                # Thread para capturar frames
                threading.Thread(target=self._capture_loop, daemon=True).start()
                return True
            else:
                CAMERAS[self.camera_id]['status'] = 'error'
                return False
                
        except Exception as e:
            logger.error(f"Error iniciando stream de cámara {self.camera_id}: {e}")
            CAMERAS[self.camera_id]['status'] = 'error'
            return False
    
    def _capture_loop(self):
        """Loop principal de captura de frames"""
        while self.opencv_stream.is_running:
            try:
                frame = self.opencv_stream.get_frame()
                if frame is not None:
                    with self.lock:
                        self.opencv_stream.frame = frame
                else:
                    time.sleep(0.1)
            except Exception as e:
                logger.error(f"Error en captura de cámara {self.camera_id}: {e}")
                time.sleep(1)
    
    def get_frame(self):
        """Obtiene el frame actual de la cámara"""
        with self.lock:
            if self.opencv_stream.frame is not None:
                return self.opencv_stream.frame.copy()
        return None
    
    def stop(self):
        """Detiene el stream de la cámara"""
        self.opencv_stream.stop()
        CAMERAS[self.camera_id]['status'] = 'offline'
        CAMERAS[self.camera_id]['stream_active'] = False
    
    @property
    def is_running(self):
        """Propiedad para verificar si el stream está ejecutándose"""
        return self.opencv_stream.is_running

def start_camera_streams():
    """Inicia los streams de todas las cámaras"""
    for camera_id in CAMERAS.keys():
        camera_streams[camera_id] = CameraStream(camera_id, CAMERAS[camera_id]['url'])
        camera_streams[camera_id].start()
        time.sleep(1)  # Pequeña pausa entre cámaras

def stop_camera_streams():
    """Detiene todos los streams de cámaras"""
    for stream in camera_streams.values():
        stream.stop()

def capture_from_camera(camera_id):
    """Captura una imagen desde una cámara específica"""
    try:
        if camera_id in camera_streams and camera_streams[camera_id].is_running:
            frame = camera_streams[camera_id].get_frame()
            if frame is not None:
                # Generar nombre de archivo
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"web_cam_{camera_id}_{timestamp}.jpg"
                
                # Usar el sistema centralizado de guardado
                result = save_capture(frame, camera_id, CAMERAS[camera_id]['name'], "web")
                
                if result['success']:
                    CAMERAS[camera_id]['last_capture'] = timestamp
                    # Agregar información adicional para la descarga
                    result['download_url'] = f"/download/{camera_id}/{filename}"
                    result['camera_name'] = CAMERAS[camera_id]['name']
                    return result
                else:
                    return {'success': False, 'error': result['error']}
        
        return {'success': False, 'error': 'Cámara no disponible'}
        
    except Exception as e:
        logger.error(f"Error capturando desde cámara {camera_id}: {e}")
        return {'success': False, 'error': str(e)}


@app.route('/')
def dashboard():
    """Página principal del dashboard"""
    return render_template('dashboard.html', cameras=CAMERAS)

@app.route('/api/status')
def api_status():
    """API para obtener el estado de todas las cámaras"""
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'server_config': WEB_SERVER_CONFIG,
        'cameras': CAMERAS,
        'camera_manager_status': camera_manager.get_status_summary()
    })

@app.route('/api/storage')
def api_storage():
    """API para obtener información del almacenamiento"""
    storage_info = get_storage_info()
    return jsonify(storage_info)

@app.route('/api/capture/<camera_id>', methods=['POST'])
def api_capture_camera(camera_id):
    """API para capturar desde una cámara específica"""
    if camera_id not in CAMERAS:
        return jsonify({'success': False, 'error': 'Cámara no encontrada'})
    
    result = capture_from_camera(camera_id)
    return jsonify(result)

@app.route('/api/capture/all', methods=['POST'])
def api_capture_all():
    """API para capturar desde todas las cámaras"""
    try:
        # Capturar desde cada cámara individualmente para obtener detalles
        captures_info = []
        captured_count = 0
        total_cameras = len(CAMERAS)
        
        for camera_id in CAMERAS.keys():
            try:
                if camera_id in camera_streams and camera_streams[camera_id].is_running:
                    frame = camera_streams[camera_id].get_frame()
                    if frame is not None:
                        # Generar nombre de archivo
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"web_cam_{camera_id}_{timestamp}.jpg"
                        
                        # Guardar imagen
                        result = save_capture(frame, camera_id, CAMERAS[camera_id]['name'], "web", subdirectory="all_cameras")
                        
                        if result['success']:
                            captured_count += 1
                            CAMERAS[camera_id]['last_capture'] = timestamp
                            
                            # Agregar información para descarga
                            capture_info = {
                                'camera_id': camera_id,
                                'camera_name': CAMERAS[camera_id]['name'],
                                'filename': result['filename'],
                                'download_url': f"/download/{camera_id}/{result['filename']}",
                                'filepath': result['filepath'],
                                'size': result['size']
                            }
                            captures_info.append(capture_info)
                        else:
                            logger.error(f"Error al capturar desde cámara {camera_id}: {result['error']}")
                    else:
                        logger.error(f"No se pudo obtener frame de cámara {camera_id}")
                else:
                    logger.error(f"Cámara {camera_id} no está disponible para captura")
                    
            except Exception as e:
                logger.error(f"Error con cámara {camera_id}: {e}")
        
        return jsonify({
            'success': True,
            'message': f'{captured_count}/{total_cameras} cámaras capturaron exitosamente',
            'captured_count': captured_count,
            'total_cameras': total_cameras,
            'captures': captures_info
        })
    except Exception as e:
        logger.error(f"Error en captura masiva: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/stream/<camera_id>/toggle', methods=['POST'])
def api_toggle_stream(camera_id):
    """API para alternar el stream de una cámara"""
    if camera_id not in CAMERAS:
        return jsonify({'success': False, 'error': 'Cámara no encontrada'})
    
    try:
        if camera_id in camera_streams and camera_streams[camera_id].is_running:
            # Detener stream
            camera_streams[camera_id].stop()
            return jsonify({'success': True, 'action': 'stopped'})
        else:
            # Iniciar stream
            if camera_id not in camera_streams:
                camera_streams[camera_id] = CameraStream(camera_id, CAMERAS[camera_id]['url'])
            camera_streams[camera_id].start()
            return jsonify({'success': True, 'action': 'started'})
    except Exception as e:
        logger.error(f"Error alternando stream de cámara {camera_id}: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/stream/start/all', methods=['POST'])
def api_start_all_streams():
    """API para iniciar todos los streams"""
    try:
        start_camera_streams()
        return jsonify({'success': True, 'message': 'Todos los streams iniciados'})
    except Exception as e:
        logger.error(f"Error iniciando streams: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/stream/stop/all', methods=['POST'])
def api_stop_all_streams():
    """API para detener todos los streams"""
    try:
        stop_camera_streams()
        return jsonify({'success': True, 'message': 'Todos los streams detenidos'})
    except Exception as e:
        logger.error(f"Error deteniendo streams: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/stream/<camera_id>')
def stream_camera(camera_id):
    """Stream en tiempo real de una cámara"""
    if camera_id not in camera_streams:
        return "Cámara no encontrada", 404
    
    def generate_frames():
        while True:
            try:
                frame = camera_streams[camera_id].get_frame()
                if frame is not None:
                    # Convertir frame a JPEG usando la librería OpenCV
                    frame_bytes = encode_frame_to_jpeg(frame, quality=80)
                    if frame_bytes:
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                
                time.sleep(0.1)  # 10 FPS
                
            except Exception as e:
                logger.error(f"Error en stream de cámara {camera_id}: {e}")
                time.sleep(1)
    
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/captures')
def list_captures():
    """Lista todas las capturas realizadas"""
    try:
        captures_dir = DIRECTORIES['captures']
        files = []
        
        for file_path in captures_dir.rglob("*.jpg"):
            if file_path.is_file():
                stat = file_path.stat()
                files.append({
                    'filename': file_path.name,
                    'path': str(file_path.relative_to(captures_dir)),
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
        
        # Ordenar por fecha de modificación (más reciente primero)
        files.sort(key=lambda x: x['modified'], reverse=True)
        
        return jsonify({
            'success': True,
            'captures': files,
            'total': len(files),
            'directory': str(captures_dir)
        })
    except Exception as e:
        logger.error(f"Error listando capturas: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download/<camera_id>/<filename>')
def download_camera_capture(camera_id, filename):
    """Descarga una captura específica de una cámara"""
    try:
        # Buscar el archivo en el directorio de capturas
        captures_dir = DIRECTORIES['captures']
        file_path = None
        
        # Buscar en subdirectorios por fecha
        for path in captures_dir.rglob(filename):
            if path.is_file():
                file_path = path
                break
        
        if file_path and file_path.exists():
            # Configurar nombre de descarga con información de la cámara
            camera_name = CAMERAS.get(camera_id, {}).get('name', f'Camera_{camera_id}')
            download_filename = f"{camera_name}_{filename}"
            
            return send_file(
                str(file_path), 
                as_attachment=True,
                download_name=download_filename,
                mimetype='image/jpeg'
            )
        else:
            return "Archivo no encontrado", 404
    except Exception as e:
        logger.error(f"Error descargando captura de cámara {camera_id}: {e}")
        return str(e), 500

@app.route('/captures/<filename>')
def download_capture(filename):
    """Descarga una captura específica (compatibilidad)"""
    try:
        # Buscar el archivo en el directorio de capturas
        captures_dir = DIRECTORIES['captures']
        file_path = None
        
        for path in captures_dir.rglob(filename):
            if path.is_file():
                file_path = path
                break
        
        if file_path and file_path.exists():
            return send_file(str(file_path), as_attachment=True)
        else:
            return "Archivo no encontrado", 404
    except Exception as e:
        logger.error(f"Error descargando captura: {e}")
        return str(e), 500

def main():
    """Función principal del servidor web"""
    logger.info("=== SERVIDOR WEB PARA CAMARAS RTSP ===")
    logger.info(f"IP: {WEB_SERVER_CONFIG['host']}")
    logger.info(f"Puerto: {WEB_SERVER_CONFIG['port']}")
    logger.info(f"Camaras configuradas: {len(CAMERAS)}")
    logger.info(f"Directorio de capturas: {WEB_SERVER_CONFIG['capture_dir']}")
    
    try:
        # Iniciar streams de cámaras
        logger.info("Iniciando streams de camaras...")
        start_camera_streams()
        
        logger.info("Servidor web iniciado exitosamente!")
        logger.info(f"Abre tu navegador en: http://localhost:{WEB_SERVER_CONFIG['port']}")
        logger.info("Usa Ctrl+C para detener el servidor")
        
        # Iniciar servidor Flask
        app.run(
            host=WEB_SERVER_CONFIG['host'],
            port=WEB_SERVER_CONFIG['port'],
            debug=WEB_SERVER_CONFIG['debug'],
            threaded=True
        )
        
    except KeyboardInterrupt:
        logger.info("Servidor detenido por el usuario")
    except Exception as e:
        logger.error(f"Error en el servidor: {e}")
    finally:
        # Detener todos los streams
        logger.info("Deteniendo streams de camaras...")
        stop_camera_streams()
        logger.info("Servidor web detenido")

if __name__ == '__main__':
    main()
