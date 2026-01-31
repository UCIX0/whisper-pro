#!/bin/bash

# Activar el entorno de Conda
source /home/ucix/anaconda3/etc/profile.d/conda.sh
conda activate whispert

# --- CORRECCIÓN: Usar puerto 8001 para evitar Docker ---
PORT=8001
echo "Verificando puerto $PORT..."

# Si hay algo corriendo en el puerto 8001 (por ejecuciones pasadas), lo mata
if lsof -ti:$PORT; then
    echo "Liberando puerto $PORT ocupado..."
    lsof -ti:$PORT | xargs kill -9
fi
# --------------------------------------------------------

echo "Starting Whisper Web Interface..."

# Verificar si el modelo existe
if [ ! -d "./modelo_whisper" ]; then
    echo "WARNING: ./modelo_whisper directory not found. Please ensure the model is in place."
fi

# Limpiar procesos en segundo plano al salir
trap 'kill 0' EXIT

# Iniciar Backend
echo "Starting Backend on port $PORT..."
cd backend
# Usando uvicorn con el NUEVO PUERTO 8001
/home/ucix/anaconda3/envs/whispert/bin/python -m uvicorn main:app --host 0.0.0.0 --port $PORT &
BACKEND_PID=$!
cd ..

# Esperar un momento
sleep 3

# Iniciar Frontend
echo "Starting Frontend..."
cd frontend
# Vite seguirá en el 5173, eso está bien
npm run dev &
FRONTEND_PID=$!
cd ..

echo "App running!"
echo "Backend: http://localhost:$PORT"
echo "Frontend: http://localhost:5173"
echo "Press Ctrl+C to stop."

wait