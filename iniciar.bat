@echo off
chcp 65001 > nul
echo ======================================================
echo    INICIANDO DIVERTIDA MENTE (BACKEND + FRONTEND)
echo ======================================================
echo.

echo [1/2] Iniciando Servidor Python com Modelos Keras...
start "Divertida Mente - Backend API" cmd /k "python servidor.py"

echo [2/2] Iniciando Frontend React (Vite)...
cd front
start "Divertida Mente - Frontend React" cmd /k "npm.cmd run dev"

echo.
echo Tudo pronto! O frontend estara disponivel em:
echo 👉 http://localhost:5173
echo.
pause
