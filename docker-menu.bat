@echo off
setlocal enabledelayedexpansion

REM Configuración
set "BASE_IMAGE=darklordcoder/pythonopencv"
set "APP_IMAGE=darklordcoder/vision-cameras"
set "BASE_DOCKERFILE=Dockerfile.pythonopencv"
set "APP_DOCKERFILE=Dockerfile"

:menu
cls
echo ========================================
echo           MENU DOCKER VISION
echo ========================================
echo.
echo 1. Construir imagen base (OpenCV)
echo 2. Construir aplicacion (Vision Cameras)
echo 3. Construir ambas imagenes
echo 4. Hacer push de imagen base a Docker Hub
echo 5. Hacer push de aplicacion a Docker Hub
echo 6. Construir y hacer push de imagen base
echo 7. Construir y hacer push de aplicacion
echo 8. Ejecutar con Docker Compose
echo 9. Ver imagenes Docker
echo 10. Limpiar imagenes
echo 0. Salir
echo.
echo ========================================
set /p choice="Selecciona una opcion (0-10): "

if "%choice%"=="1" goto build_base
if "%choice%"=="2" goto build_app
if "%choice%"=="3" goto build_both
if "%choice%"=="4" goto push_base
if "%choice%"=="5" goto push_app
if "%choice%"=="6" goto build_push_base
if "%choice%"=="7" goto build_push_app
if "%choice%"=="8" goto docker_compose
if "%choice%"=="9" goto show_images
if "%choice%"=="10" goto clean_images
if "%choice%"=="0" goto exit
goto invalid_choice

REM ========================================
REM Construir imagen base (OpenCV)
REM ========================================
:build_base
cls
echo ========================================
echo     CONSTRUYENDO IMAGEN BASE
echo ========================================
echo.
echo Construyendo: %BASE_IMAGE%:latest
echo Dockerfile: %BASE_DOCKERFILE%
echo.

docker build -f %BASE_DOCKERFILE% -t %BASE_IMAGE%:latest .

if errorlevel 1 (
    echo.
    echo [ERROR] Error construyendo la imagen base
    pause
    goto menu
)

echo.
echo [SUCCESS] Imagen base construida exitosamente!
echo.
docker images | findstr %BASE_IMAGE%
pause
goto menu

REM ========================================
REM Construir aplicacion (Vision Cameras)
REM ========================================
:build_app
cls
echo ========================================
echo    CONSTRUYENDO APLICACION
echo ========================================
echo.
echo Construyendo: %APP_IMAGE%:latest
echo Dockerfile: %APP_DOCKERFILE%
echo.

docker build -f %APP_DOCKERFILE% -t %APP_IMAGE%:latest .

if errorlevel 1 (
    echo.
    echo [ERROR] Error construyendo la aplicacion
    pause
    goto menu
)

echo.
echo [SUCCESS] Aplicacion construida exitosamente!
echo.
docker images | findstr %APP_IMAGE%
pause
goto menu

REM ========================================
REM Construir ambas imagenes
REM ========================================
:build_both
cls
echo ========================================
echo    CONSTRUYENDO AMBAS IMAGENES
echo ========================================
echo.

echo [1/2] Construyendo imagen base...
docker build -f %BASE_DOCKERFILE% -t %BASE_IMAGE%:latest .
if errorlevel 1 (
    echo [ERROR] Error construyendo imagen base
    pause
    goto menu
)

echo [2/2] Construyendo aplicacion...
docker build -f %APP_DOCKERFILE% -t %APP_IMAGE%:latest .
if errorlevel 1 (
    echo [ERROR] Error construyendo aplicacion
    pause
    goto menu
)

echo.
echo [SUCCESS] Ambas imagenes construidas exitosamente!
echo.
echo Imagenes disponibles:
docker images | findstr -E "(%BASE_IMAGE%|%APP_IMAGE%)"
pause
goto menu

REM ========================================
REM Hacer push de imagen base
REM ========================================
:push_base
cls
echo ========================================
echo    PUSH IMAGEN BASE A DOCKER HUB
echo ========================================
echo.

echo Haciendo push de %BASE_IMAGE%:latest...
docker push %BASE_IMAGE%:latest

if errorlevel 1 (
    echo [ERROR] Error haciendo push de la imagen base
    pause
    goto menu
)

echo.
echo [SUCCESS] Imagen base publicada en Docker Hub!
pause
goto menu

REM ========================================
REM Hacer push de aplicacion
REM ========================================
:push_app
cls
echo ========================================
echo   PUSH APLICACION A DOCKER HUB
echo ========================================
echo.

echo Haciendo push de %APP_IMAGE%:latest...
docker push %APP_IMAGE%:latest

if errorlevel 1 (
    echo [ERROR] Error haciendo push de la aplicacion
    pause
    goto menu
)

echo.
echo [SUCCESS] Aplicacion publicada en Docker Hub!
pause
goto menu

REM ========================================
REM Construir y hacer push de imagen base
REM ========================================
:build_push_base
cls
echo ========================================
echo  CONSTRUIR Y PUSH IMAGEN BASE
echo ========================================
echo.

echo [1/2] Construyendo imagen base...
docker build -f %BASE_DOCKERFILE% -t %BASE_IMAGE%:latest .
if errorlevel 1 (
    echo [ERROR] Error construyendo imagen base
    pause
    goto menu
)

echo [2/2] Haciendo push a Docker Hub...
docker push %BASE_IMAGE%:latest
if errorlevel 1 (
    echo [ERROR] Error haciendo push
    pause
    goto menu
)

echo.
echo [SUCCESS] Imagen base construida y publicada!
pause
goto menu

REM ========================================
REM Construir y hacer push de aplicacion
REM ========================================
:build_push_app
cls
echo ========================================
echo  CONSTRUIR Y PUSH APLICACION
echo ========================================
echo.

echo [1/2] Construyendo aplicacion...
docker build -f %APP_DOCKERFILE% -t %APP_IMAGE%:latest .
if errorlevel 1 (
    echo [ERROR] Error construyendo aplicacion
    pause
    goto menu
)

echo [2/2] Haciendo push a Docker Hub...
docker push %APP_IMAGE%:latest
if errorlevel 1 (
    echo [ERROR] Error haciendo push
    pause
    goto menu
)

echo.
echo [SUCCESS] Aplicacion construida y publicada!
pause
goto menu

REM ========================================
REM Ejecutar con Docker Compose
REM ========================================
:docker_compose
cls
echo ========================================
echo        DOCKER COMPOSE
echo ========================================
echo.
echo 1. Construir y ejecutar
echo 2. Solo ejecutar
echo 3. Detener servicios
echo 4. Ver logs
echo 5. Volver al menu principal
echo.
set /p compose_choice="Selecciona opcion (1-5): "

if "%compose_choice%"=="1" (
    echo Construyendo y ejecutando servicios...
    docker-compose up -d --build
    pause
    goto docker_compose
)
if "%compose_choice%"=="2" (
    echo Ejecutando servicios...
    docker-compose up -d
    pause
    goto docker_compose
)
if "%compose_choice%"=="3" (
    echo Deteniendo servicios...
    docker-compose down
    pause
    goto docker_compose
)
if "%compose_choice%"=="4" (
    echo Mostrando logs...
    docker-compose logs -f
    pause
    goto docker_compose
)
if "%compose_choice%"=="5" goto menu
goto docker_compose

REM ========================================
REM Ver imagenes Docker
REM ========================================
:show_images
cls
echo ========================================
echo         IMAGENES DOCKER
echo ========================================
echo.
echo Imagenes del proyecto:
echo.
docker images | findstr -E "(%BASE_IMAGE%|%APP_IMAGE%)"
echo.
echo Todas las imagenes:
echo.
docker images
pause
goto menu

REM ========================================
REM Limpiar imagenes
REM ========================================
:clean_images
cls
echo ========================================
echo         LIMPIAR IMAGENES
echo ========================================
echo.
echo [WARNING] Esto eliminara todas las imagenes no utilizadas
echo.
set /p clean_choice="¿Estas seguro? (y/N): "
if /i "%clean_choice%"=="y" (
    echo Limpiando imagenes...
    docker system prune -f
    echo [SUCCESS] Limpieza completada
) else (
    echo Limpieza cancelada
)
pause
goto menu

REM ========================================
REM Opcion invalida
REM ========================================
:invalid_choice
echo.
echo [ERROR] Opcion invalida. Selecciona un numero del 0 al 10
pause
goto menu

REM ========================================
REM Salir
REM ========================================
:exit
cls
echo ========================================
echo           ADIOS!
echo ========================================
echo.
echo Gracias por usar Docker Menu Vision
echo.
exit /b 0
