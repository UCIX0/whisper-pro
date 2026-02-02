# Solución de Configuración Librerías NVIDIA/CUDA

> 🇺🇸 **[English](../en/nvidia.md)** | 🇪🇸 **[Español](./nvidia.md)**

Este documento explica un problema común al usar librerías de NVIDIA instaladas vía pip (`nvidia-cublas-cu12`, `nvidia-cudnn-cu12`) en Linux y cómo lo he solucionado automáticamente en este proyecto.

## El Problema: "Could not load library"

Cuando `faster-whisper` (a través de `ctranslate2`) intenta ejecutarse en la GPU, requiere acceso a librerías compartidas como `libcublas.so` y `libcudnn.so`.

Aunque estas librerías están instaladas en tu entorno mediante pip:
- `nvidia-cublas-cu12`
- `nvidia-cudnn-cu12`

El enlazador dinámico de Linux (dynamic linker) generalmente no sabe dónde encontrarlas porque residen profundamente anidadas dentro del directorio `site-packages` de Python, por ejemplo:
`/ruta/al/env/lib/python3.10/site-packages/nvidia/cudnn/lib`

Sin una configuración explícita, podrías ver errores como:
> `RuntimeError: Library cudnn is not found or cannot be loaded`
> `Could not load library libcudnn_ops_infer.so.8. Error: libcudnn_ops_infer.so.8: cannot open shared object file: No such file or directory`

## La Solución: Scripts de Activación de Conda

Para solucionar esto de manera robusta sin requerir que cada usuario exporte variables manualmente cada vez, he implementado **Scripts de Activación de Conda**.

Estos scripts se ejecutan automáticamente cuando activas o desactivas el entorno.

### 1. Script de Activación (`activate.d`)

He creado un script en:
`$CONDA_PREFIX/etc/conda/activate.d/nvidia_vars.sh`

**Contenido:**
```bash
#!/bin/sh

# Guardar el antiguo LD_LIBRARY_PATH para restaurarlo después
export OLD_LD_LIBRARY_PATH=$LD_LIBRARY_PATH

# Añadir las rutas de los paquetes pip de nvidia al LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib/python3.10/site-packages/nvidia/cudnn/lib:$CONDA_PREFIX/lib/python3.10/site-packages/nvidia/cublas/lib:$CONDA_PREFIX/lib/python3.10/site-packages/nvidia/cudart/lib:$LD_LIBRARY_PATH
```

Esto asegura que tan pronto como hagas `conda activate whispert`, el sistema sepa exactamente dónde encontrar las librerías de NVIDIA.

### 2. Script de Desactivación (`deactivate.d`)

También he creado un script en:
`$CONDA_PREFIX/etc/conda/deactivate.d/nvidia_vars.sh`

**Contenido:**
```bash
#!/bin/sh

# Restaurar el LD_LIBRARY_PATH original
export LD_LIBRARY_PATH=$OLD_LD_LIBRARY_PATH
unset OLD_LD_LIBRARY_PATH
```

Esto limpia tus variables de entorno cuando sales del entorno del proyecto (`conda deactivate`), evitando conflictos con otros proyectos.

## Verificación

Puedes verificar que esta solución está activa ejecutando:

```bash
conda activate whispert
echo $LD_LIBRARY_PATH
```

Deberías ver que las rutas contienen `.../site-packages/nvidia/...` al principio de la salida.
