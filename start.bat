@echo off

REM Obtener la ruta base de Conda
for /f "tokens=*" %%i in ('conda info --base') do (
    set CONDA_BASE=%%i
)

REM Construir las rutas a las bibliotecas de NVIDIA
set NVIDIA_CUDNN_BIN=%CONDA_BASE%\envs\whispert\Lib\site-packages\nvidia\cudnn\bin
set NVIDIA_CUBLAS_BIN=%CONDA_BASE%\envs\whispert\Lib\site-packages\nvidia\cublas\bin
set NVIDIA_CUDART_BIN=%CONDA_BASE%\envs\whispert\Lib\site-packages\nvidia\cudart\bin

REM Añadir las rutas al PATH
set "PATH=%NVIDIA_CUDNN_BIN%;%NVIDIA_CUBLAS_BIN%;%NVIDIA_CUDART_BIN%;%PATH%"

REM Activar el entorno de Conda
call conda activate whispert

REM --- CORRECCIÓN: Usar puerto 8001 para evitar Docker ---
set PORT=8001
echo Verificando puerto %PORT%...

REM Si hay algo corriendo en el puerto 8001 (por ejecuciones pasadas), lo mata
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%PORT%') do (
    echo Liberando puerto %PORT% ocupado por el PID %%a...
    taskkill /F /PID %%a
)
REM --------------------------------------------------------

echo Starting Whisper Web Interface...

REM Verificar si el modelo existe
if not exist ".\\modelo_whisper" (
    echo WARNING: .\modelo_whisper directory not found. Please ensure the model is in place.
)

REM Iniciar Backend
echo Starting Backend on port %PORT%...
cd backend
start "backend" cmd /c "python -m uvicorn main:app --host 0.0.0.0 --port %PORT%"
cd ..

REM Esperar un momento
timeout /t 3 /nobreak > nul

REM Iniciar Frontend
echo Starting Frontend...
cd frontend
start "frontend" cmd /c "npm run dev"
cd ..

echo App running!
echo Backend: http://localhost:%PORT%
echo Frontend: http://localhost:5173
echo Press Ctrl+C in the command prompts to stop.

pause
