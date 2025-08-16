@echo off
title Servidor Web Camaras RTSP
color 0E

echo ========================================
echo    SERVIDOR WEB PARA CAMARAS RTSP
echo ========================================
echo.

echo 📡 IP: 94.125.136.236
echo 🔌 Puerto: 7447
echo 📷 Total de camaras: 4
echo 🌐 Puerto Web: 5000
echo.

echo 🚀 Iniciando servidor web...
echo 💡 El servidor estara disponible en: http://localhost:5000
echo 💡 Presiona Ctrl+C para detener el servidor
echo.

set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
"C:\Users\salva\AppData\Local\Programs\Python\Python313\python.exe" -X utf8 web_server.py

echo.
echo ========================================
echo    SERVIDOR WEB DETENIDO
echo ========================================
echo.
pause
