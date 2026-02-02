# Whisper Pro en Windows: Guía de Instalación y Uso

> ⚠️ **Advertencia**: Esta aplicación fue diseñada y optimizada principalmente para **Linux**. La compatibilidad con Windows es funcional pero podría presentar inestabilidades o no recibir el mismo nivel de mantenimiento que la versión de Linux. Algunas funcionalidades futuras podrían no ser compatibles.

Esta guía detalla los pasos y particularidades para ejecutar **Whisper Pro** en un entorno Windows con aceleración por GPU.

---

## 1. Requisitos Previos

Asegúrate de tener el siguiente software instalado en tu sistema:

1.  **NVIDIA GPU**: Una tarjeta gráfica NVIDIA compatible con CUDA.
2.  **Drivers NVIDIA**: Los drivers de juego (Game Ready) o de estudio (Studio) más recientes.
    *   **Verificación**: Abre el terminal (PowerShell o CMD) y ejecuta `nvidia-smi`. Deberías ver los detalles de tu GPU y la versión del driver.
3.  **Conda**: El gestor de paquetes Anaconda o Miniconda.
    *   **Verificación**: Ejecuta `conda --version` en el terminal.
4.  **Node.js**: Se recomienda la versión LTS.
    *   **Verificación**: Ejecuta `node --version` en el terminal.

---

## 2. Configuración del Entorno

El proceso de configuración es similar al de Linux, pero usarás scripts específicos para Windows.

### a. Clonar el Repositorio
```powershell
git clone https://github.com/tu-repo/whisper-pro.git
cd whisper-pro
```

### b. Crear el Entorno de Conda
Usa el mismo archivo `environment.yml` para crear el entorno. Contiene todas las dependencias de Python, incluidas las librerías CUDA que `faster-whisper` necesita.

```powershell
# Crea el entorno llamado 'whispert'
conda env create -f environment.yml

# Activa el nuevo entorno
conda activate whispert
```

### c. Instalar Dependencias de Node.js
```powershell
# Instala los paquetes del frontend
npm install
```

---

## 3. Lanzamiento de la Aplicación en Windows

A diferencia de Linux que usa `start.sh`, en Windows debes usar el script **`start.bat`**.

```powershell
./start.bat
```

### ¿Qué hace el script `start.bat`?

Este script está diseñado para automatizar la configuración específica de Windows:

1.  **Configura el PATH**: Encuentra la ruta de tu entorno Conda y **añade automáticamente al PATH** las carpetas `bin` de las librerías `cudnn`, `cublas` y `cudart` que se instalaron con pip. Esto es crucial para que Windows encuentre las DLLs de NVIDIA y es el equivalente a configurar `LD_LIBRARY_PATH` en Linux.
2.  **Activa el Entorno**: Ejecuta `conda activate whispert`.
3.  **Libera el Puerto**: Mata cualquier proceso que haya quedado activo en el puerto `8001` de ejecuciones anteriores para evitar conflictos.
4.  **Inicia el Backend**: Lanza el servidor de FastAPI en una nueva ventana de terminal.
5.  **Inicia el Frontend**: Lanza el servidor de desarrollo de Vite (React) en otra ventana.

Una vez que el script finalice, la aplicación estará disponible en:
-   **Frontend**: `http://localhost:5173`
-   **API (Backend)**: `http://localhost:8001`

---

## 4. Verificación del Entorno

Si encuentras problemas, puedes usar el script de verificación para diagnosticar tu configuración. Este script es compatible con Windows.

```powershell
# Asegúrate de que el entorno 'whispert' esté activado
python verify_env.py
```

El script revisará tu versión de Python, la instalación de paquetes, la visibilidad de la GPU y si las rutas de las librerías CUDA están correctamente configuradas en el `PATH` para Windows. Sigue las indicaciones si reporta algún `[FAIL]`.
