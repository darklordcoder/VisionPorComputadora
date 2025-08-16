# Dockerfile para aplicación de cámaras RTSP
FROM darklordcoder/pythonopencv:latest

# Copiar requirements e instalar dependencias Python adicionales
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p captures logs static templates config src

# Establecer permisos
RUN chmod +x web_server.py

# Variables de entorno para producción
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Comando de inicio
CMD ["python", "web_server.py"]
