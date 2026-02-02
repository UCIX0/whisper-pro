# Instrucciones de Configuración del Entorno 🛠️

> 🇺🇸 **[English](./README_ENV.md)** | 🇪🇸 **[Español](./README_ENV_ES.md)**

Esta guía te ayudará a recrear el entorno de desarrollo exacto para `whisper-pro` utilizando los archivos de configuración generados.

## 1. Entorno Python / Conda

He creado un archivo `environment.yml` que contiene todos los paquetes conda y pip utilizados en el proyecto.

### Crear el Entorno
Para crear el entorno `whispert` desde el archivo, ejecuta:

```bash
conda env create -f environment.yml
```

### Activar el Entorno
Una vez creado, actívalo con:

```bash
conda activate whispert
```

### Actualizar un Entorno Existente
Si ya tienes un entorno llamado `whispert` y quieres actualizarlo para coincidir con esta configuración:

```bash
conda env update -f environment.yml --prune
```

## 2. Dependencias Node.js / NPM

He creado un archivo `package.json` con las versiones exactas de los paquetes npm.

### Instalar Dependencias
Ejecuta el siguiente comando en la raíz del proyecto para instalar los módulos de node:

```bash
npm install
```

## 3. Verificación

Después de la instalación, puedes verificar el entorno:

**Python:**
```bash
conda list
# Debería coincidir con la lista proporcionada
```

**NPM:**
```bash
npm list
# Debería coincidir con la lista proporcionada
```

## 4. Soporte GPU y Configuración CUDA (Importante)

Este proyecto utiliza `faster-whisper` y `ctranslate2`, que dependen de librerías NVIDIA para la aceleración por GPU.

### Prerrequisitos
1.  **Driver NVIDIA**: Debes tener un driver NVIDIA compatible instalado en tu sistema host (Linux).
    - Comprobación: Ejecuta `nvidia-smi` en tu terminal. Deberías ver tu GPU listada y una versión del driver.

### Configuración
El entorno instala las librerías CUDA necesarias (cuBLAS, cuDNN) a través de paquetes pip.

> [!WARNING]
> **Configuración Crítica**: Para asegurar que el sistema encuentre estas librerías, este entorno utiliza **scripts de activación automática** para configurar `LD_LIBRARY_PATH`.
>
> 📄 **Lee la explicación detallada y la solución aquí: [README_NVIDIA_ES.md](./README_NVIDIA_ES.md)**
>
> No configures manualmente `LD_LIBRARY_PATH` a menos que sepas lo que haces, ya que podría entrar en conflicto con la configuración automática.

### Verificación de Acceso a GPU
Para confirmar que `faster-whisper` puede ver tu GPU, puedes ejecutar una comprobación rápida en Python:

```python
from faster_whisper import WhisperModel
import torch

print(f"PyTorch CUDA Available: {torch.cuda.is_available()}")
# Nota: faster-whisper usa CTranslate2, no PyTorch directamente para inferencia, 
# pero comprobar la disponibilidad CUDA de PyTorch es un buen indicador de la salud del driver.

try:
    model = WhisperModel("tiny", device="cuda", compute_type="float16")
    print("Success: Model loaded on GPU!")
except Exception as e:
    print(f"Error loading on GPU: {e}")
```

## 5. Verificación Automatizada

He incluido un script `verify_env.py` para comprobar automáticamente la configuración de tu entorno, dependencias y configuración de GPU.

### Uso
Asegúrate de que tu entorno esté activado, luego ejecuta:

```bash
python verify_env.py
```

El script producirá un informe codificado por colores:
- **[OK] Verde**: pasó.
- **[FAIL] Rojo**: Verificación fallida (ej: paquete faltante, GPU no visible).
- **[WARN] Amarillo**: Problema potencial (ej: falta LD_LIBRARY_PATH).

Si tiene éxito, verás:
> **SUCCESS:** Your environment looks perfect! Ready to launch.
