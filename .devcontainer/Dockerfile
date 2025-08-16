# syntax=docker/dockerfile:1
FROM mcr.microsoft.com/devcontainers/python:3.11

# Instala dependencias del sistema necesarias para OpenCV y otros paquetes
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        libsm6 \
        libxext6 \
        nginx \
    && rm -rf /var/lib/apt/lists/*


# Copia los requirements desde la raíz del proyecto (un nivel arriba de .devcontainer)
COPY ../requirements.txt /tmp/pip-tmp/
RUN pip install --upgrade pip && pip install -r /tmp/pip-tmp/requirements.txt

# Crea usuario vscode si no existe
ARG USERNAME=vscode
RUN id -u $USERNAME &>/dev/null || useradd -m $USERNAME

# Establece el usuario por defecto
USER $USERNAME

WORKDIR /workspace
