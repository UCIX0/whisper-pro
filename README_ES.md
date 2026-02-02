# Whisper Pro 🎙️✨

> 🇪🇸 **[Español](./README_ES.md)** | 🇺🇸 **[English](./README.md)**

**Whisper Pro** es una interfaz web de alto rendimiento acelerada por GPU para el modelo Whisper de OpenAI, capaz de transcribir audio con velocidad y precisión de grado profesional. Construido con una pila tecnológica moderna, combina la potencia bruta de `faster-whisper` y `CTranslate2` con un frontend elegante y responsivo en React.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![React](https://img.shields.io/badge/react-18-blue.svg)
![GPU](https://img.shields.io/badge/GPU-NVIDIA%20CUDA-green.svg)

---

## 🚀 Características

-   **Transcripción Ultra-Rápida**: Impulsado por `faster-whisper`, logrando velocidades hasta 4x superiores a la implementación original de Whisper.
-   **Interfaz Moderna**: Interfaz hermosa con modo oscuro, construida con **React**, **TailwindCSS** y **Framer Motion**.
-   **Aceleración por GPU**: Totalmente optimizado para GPUs NVIDIA usando CUDA 12 y CTranslate2.
-   **Retroalimentación en Tiempo Real**: Frontend interactivo con indicadores de progreso y visualización de audio.
-   **Verificación Automatizada del Entorno**: Herramientas integradas para asegurar que tu sistema esté perfectamente configurado.

---

## 🛠️ Arquitectura y Stack Tecnológico

### **Frontend** (Lado del Cliente)
La interfaz de usuario es una Single Page Application (SPA) moderna diseñada para la responsividad y estética.
*   **Framework**: [Vite](https://vitejs.dev/) + [React](https://react.dev/)
*   **Estilos**: [TailwindCSS v4](https://tailwindcss.com/)
*   **Animaciones**: [Framer Motion](https://www.framer.com/motion/)
*   **Iconos**: [Lucide React](https://lucide.dev/)

### **Backend** (Lado del Servidor)
La lógica central reside en una API ASYNC de Python de alto rendimiento.
*   **Framework API**: [FastAPI](https://fastapi.tiangolo.com/)
*   **Servidor**: [Uvicorn](https://www.uvicorn.org/)
*   **Motor de Inferencia**: [Faster Whisper](https://github.com/SYSTRAN/faster-whisper) (omitiendo transformers de HuggingFace para velocidad bruta vía CTranslate2).

---

## 💻 Requisitos del Sistema

Para ejecutar Whisper Pro con la máxima eficiencia, se recomienda el siguiente hardware:

| Componente | Mínimo | Recomendado |
| :--- | :--- | :--- |
| **SO** | Linux (Ubuntu 20.04+) | Linux (Kernel genérico reciente) |
| **GPU** | NVIDIA GTX Serie 10 (4GB VRAM) | NVIDIA RTX Serie 30/40 (8GB+ VRAM) |
| **RAM** | 8 GB | 16 GB+ |
| **Driver** | NVIDIA Driver 535+ | NVIDIA Driver 550+ |
| **CUDA** | Soporte CUDA 12.x | Soporte CUDA 12.x |

> **Nota**: El modo solo CPU es posible pero significativamente más lento y no se recomienda para uso en producción.

---

## 📦 Instalación y Configuración

Proporciono una configuración de entorno estrictamente versionada para garantizar la estabilidad.

### 1. Clonar y Preparar
```bash
git clone https://github.com/tu-repo/whisper-pro.git
cd whisper-pro
```

### 2. Entorno Python (Conda)
Este proyecto usa **Conda** para gestionar Python y las librerías del sistema (como `ffmpeg` y `cudnn`).
```bash
# Crear el entorno desde el archivo
conda env create -f environment.yml

# Activar
conda activate whispert
```

### 3. Dependencias del Frontend (Node.js)
```bash
# Instalar paquetes NPM
npm install
```

### 4. Verificar Entorno (Opcional pero Recomendado)
He incluido una herramienta de verificación personalizada para comprobar la visibilidad de tu GPU, rutas CUDA y dependencias.
```bash
python verify_env.py
```
*   **Verde [OK]**: Estás listo.
*   **Rojo [FAIL]**: Accede a `README_ENV.md` para instrucciones de solución de problemas.

---

## ⚡ Inicio Rápido

Proporciono un script de inicio consolidado que maneja los puertos y lanza ambos servicios.

```bash
./start.sh
```

Este script:
1.  Verificará y liberará los puertos `8001` (Backend) y `5173` (Frontend).
2.  Activará el entorno conda `whispert`.
3.  Lanzará el backend FastAPI.
4.  Lanzará el servidor de desarrollo Vite.

**Acceder a la aplicación:**
-   **Frontend**: [http://localhost:5173](http://localhost:5173)
-   **Docs API**: [http://localhost:8001/docs](http://localhost:8001/docs)

---

## 📝 Documentación Detallada

### 📘 Detalles del Entorno
Para una inmersión profunda en las versiones de dependencias y la gestión del entorno, por favor consulta la **[Documentación del Entorno](./README_ENV_ES.md)**.

### Solución de Problemas de GPU
Si `verify_env.py` reporta problemas de GPU, probablemente necesites configurar `LD_LIBRARY_PATH` para las librerías NVIDIA instaladas por pip. Mira la sección **Soporte GPU** en `README_ENV_ES.md`.

---

## ⚙️ Desarrollo

**Estructura de Directorios:**
```bash
whisper-pro/
├── backend/            # Aplicación FastAPI
│   ├── main.py        # Punto de entrada
│   └── service.py     # Lógica de inferencia
├── frontend/           # Aplicación React
│   ├── src/           # Componentes y Lógica
│   └── public/        # Activos estáticos
├── environment.yml     # Definición de entorno Conda
└── verify_env.py       # Script de chequeo de salud
```

---

## 👨‍💻 Nota del Desarrollador

Solo una pequeña nota personal: este proyecto comenzó como un pequeño experimento de hobby para ayudarme a sobrevivir a la universidad. Lo construí para transcribir mis clases y luego pasarle el texto a ChatGPT para generar resúmenes y notas de estudio. Ha sido súper útil, ¡así que espero que también te sirva a ti—ya sea para la escuela, el trabajo o solo por diversión!

