// Funciones del Dashboard de Cámaras RTSP

// Función para capturar desde todas las cámaras
function captureAll() {
    fetch('/api/capture/all', {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Captura completada: ' + data.message, 'success');
                
                // Si hay información de capturas individuales, descargarlas
                if (data.captures && data.captures.length > 0) {
                    data.captures.forEach(capture => {
                        if (capture.download_url) {
                            setTimeout(() => {
                                downloadImage(capture.download_url, capture.filename, capture.camera_name);
                            }, 1000); // Delay entre descargas
                        }
                    });
                }
                
                // setTimeout(() => location.reload(), 3000); // Sin recarga automática
            } else {
                showNotification('Error: ' + data.error, 'error');
            }
        });
}

// Función para capturar desde una cámara específica
function captureCamera(cameraId) {
    fetch(`/api/capture/${cameraId}`, {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Imagen capturada: ' + data.filename, 'success');
                
                // Descargar automáticamente la imagen
                if (data.download_url) {
                    downloadImage(data.download_url, data.filename, data.camera_name);
                }
                
                // setTimeout(() => location.reload(), 2000); // Sin recarga automática
            } else {
                showNotification('Error: ' + data.error, 'error');
            }
        });
}

// Función para descargar la última captura de una cámara
function downloadLastCapture(cameraId, cameraName, lastCapture) {
    try {
        // Construir URL de descarga
        const downloadUrl = `/download/${cameraId}/web_cam_${cameraId}_${lastCapture}.jpg`;
        const filename = `web_cam_${cameraId}_${lastCapture}.jpg`;
        
        showNotification(`Descargando última captura de ${cameraName}...`, 'success');
        
        // Crear enlace de descarga
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = `${cameraName}_${filename}`;
        link.style.display = 'none';
        
        // Agregar al DOM y hacer clic
        document.body.appendChild(link);
        link.click();
        
        // Limpiar
        document.body.removeChild(link);
        
        // Confirmación
        setTimeout(() => {
            showNotification(`Última captura de ${cameraName} descargada`, 'success');
        }, 1000);
        
    } catch (error) {
        console.error('Error descargando última captura:', error);
        showNotification('Error al descargar última captura', 'error');
    }
}

// Función para descargar imagen automáticamente
function downloadImage(downloadUrl, filename, cameraName) {
    try {
        // Mostrar indicador de descarga
        showNotification(`Descargando imagen de ${cameraName}...`, 'success');
        
        // Crear un enlace temporal para la descarga
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = `${cameraName}_${filename}`;
        link.style.display = 'none';
        
        // Agregar al DOM y hacer clic
        document.body.appendChild(link);
        link.click();
        
        // Limpiar
        document.body.removeChild(link);
        
        // Mostrar confirmación de descarga
        setTimeout(() => {
            showNotification(`Imagen de ${cameraName} descargada exitosamente`, 'success');
        }, 1000);
        
    } catch (error) {
        console.error('Error en descarga automática:', error);
        showNotification('Error en descarga automática', 'error');
    }
}

// Función para alternar stream de cámara
function toggleStream(cameraId) {
    fetch(`/api/stream/${cameraId}/toggle`, {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // location.reload(); // Sin recarga automática
                showNotification('Stream alternado exitosamente', 'success');
            } else {
                showNotification('Error: ' + data.error, 'error');
            }
        });
}

// Función para ver stream
function viewStream(cameraId) {
    window.open(`/stream/${cameraId}`, '_blank');
}

// Función para iniciar todos los streams
function startAllStreams() {
    fetch('/api/stream/start/all', {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Todos los streams iniciados', 'success');
                // setTimeout(() => location.reload(), 1000); // Sin recarga automática
            } else {
                showNotification('Error: ' + data.error, 'error');
            }
        });
}

// Función para detener todos los streams
function stopAllStreams() {
    fetch('/api/stream/stop/all', {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Todos los streams detenidos', 'success');
                // setTimeout(() => location.reload(), 1000); // Sin recarga automática
            } else {
                showNotification('Error: ' + data.error, 'error');
            }
        });
}

// Función para actualizar estado
function refreshStatus() {
    // location.reload(); // Sin recarga automática
    showNotification('Estado actualizado manualmente', 'success');
}

// Función para mostrar notificaciones
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
        type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
    }`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Actualizar estado automáticamente cada 30 segundos
// setInterval(refreshStatus, 30000); // Comentado para evitar recargas automáticas
