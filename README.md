# Whisper Pro 🎙️✨

> 🇺🇸 **[English](./README.md)** | 🇪🇸 **[Español](./docs/es/index.md)**

**Whisper Pro** is a high-performance, GPU-accelerated web interface for OpenAI's Whisper model, capable of transcribing audio with professional-grade accuracy and speed. Built with a modern tech stack, it combines the raw power of `faster-whisper` and `CTranslate2` with a sleek, responsive React frontend.

> **Environment Setup**: For detailed installation instructions and dependency versions, please refer to the **[Environment Documentation](./docs/en/env.md)**.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![React](https://img.shields.io/badge/react-18-blue.svg)
![GPU](https://img.shields.io/badge/GPU-NVIDIA%20CUDA-green.svg)

---

## 🚀 Features

-   **Ultra-Fast Transcription**: Powered by `faster-whisper`, achieving up to 4x speedups over original Whisper implementation.
-   **Modern UI**: Beautiful, dark-mode capability interface built with **React**, **TailwindCSS**, and **Framer Motion**.
-   **GPU Acceleration**: Fully optimized for NVIDIA GPUs using CUDA 12 and CTranslate2.
-   **Real-time Feedback**: Interactive frontend with progress indicators and audio visualization.
-   **Automated Environment Verification**: Built-in tools to ensure your system is perfectly configured.

---

## 🛠️ Architecture & Tech Stack

### **Frontend** (Client-Side)
The user interface is a modern Single Page Application (SPA) designed for responsiveness and aesthetics.
*   **Framework**: [Vite](https://vitejs.dev/) + [React](https://react.dev/)
*   **Styling**: [TailwindCSS v4](https://tailwindcss.com/)
*   **Animations**: [Framer Motion](https://www.framer.com/motion/)
*   **Icons**: [Lucide React](https://lucide.dev/)

### **Backend** (Server-Side)
The core logic resides in a high-performance Python ASYNC API.
*   **API Framework**: [FastAPI](https://fastapi.tiangolo.com/)
*   **Server**: [Uvicorn](https://www.uvicorn.org/)
*   **Inference Engine**: [Faster Whisper](https://github.com/SYSTRAN/faster-whisper) (bypassing HuggingFace transformers for raw speed via CTranslate2).

---

## 💻 System Requirements

To run Whisper Pro at maximum efficiency, the following hardware is recommended:

| Component | Minimum | Recommended |
| :--- | :--- | :--- |
| **OS** | Linux (Ubuntu 20.04+) | Linux (Latest generic kernel) |
| **GPU** | NVIDIA GTX 10-Series (4GB VRAM) | NVIDIA RTX 30/40-Series (8GB+ VRAM) |
| **RAM** | 8 GB | 16 GB+ |
| **Driver** | NVIDIA Driver 535+ | NVIDIA Driver 550+ |
| **CUDA** | CUDA 12.x support | CUDA 12.x support |

> **Note**: CPU-only mode is possible but significantly slower and not recommended for production use.

---

## 🖥️ Windows Compatibility

This project is optimized for Linux but can be run on **Windows** with GPU acceleration. For detailed setup instructions on Windows, please refer to the specific guide:

> 📄 **[Installation Guide for Windows](./docs/en/windows.md)**

---

## 📦 Installation & Setup

I provide a strictly versioned environment configuration to guarantee stability.

### 1. Clone & Prepare
```bash
git clone https://github.com/your-repo/whisper-pro.git
cd whisper-pro
```

### 2. Python Environment (Conda)
This project uses **Conda** to manage Python and system libraries (like `ffmpeg` and `cudnn`).
```bash
# Create the environment from file
conda env create -f environment.yml

# Activate
conda activate whispert
```

### 3. Frontend Dependencies (Node.js)
```bash
# Install NPM packages
npm install
```

### 4. Verify Environment (Optional but Recommended)
I have included a custom verification tool to check your GPU visibility, CUDA paths, and dependencies.
```bash
python verify_env.py
```
*   **Green [OK]**: You are ready.
*   **Red [FAIL]**: Access `docs/en/env.md` for troubleshooting instructions.

---

## ⚡ Quick Start

I provide a consolidated startup script that handles port management and launches both services.

```bash
./start.sh
```

This script will:
1.  Check and free ports `8001` (Backend) and `5173` (Frontend).
2.  Activate the conda environment `whispert`.
3.  Launch the FastAPI backend.
4.  Launch the Vite development server.

**Access the application:**
-   **Frontend**: [http://localhost:5173](http://localhost:5173)
-   **API Docs**: [http://localhost:8001/docs](http://localhost:8001/docs)

---

## 📝 Documentation

### Environment Details
For a deep dive into the dependency versions and managing the environment, please refer to the [Environment Documentation](./docs/en/env.md)

### GPU Troubleshooting
If `verify_env.py` reports GPU issues, you likely need to configure `LD_LIBRARY_PATH` for the pip-installed NVIDIA libraries. See the **GPU Support** section in `docs/en/env.md`.

---

## ⚙️ Development

**Directory Structure:**
```bash
whisper-pro/
├── backend/            # FastAPI Application
│   ├── main.py        # Entry point
│   └── service.py     # Inference logic
├── frontend/           # React Application
│   ├── src/           # Components & Logic
│   └── public/        # Static assets
├── environment.yml     # Conda environment def
└── verify_env.py       # Health check script
```

---

## 👨‍💻 Developer's Note

Just a quick personal note: this project started as a small hobby experiment to help me survive university. I built it to transcribe my lectures so I could feed the text into ChatGPT for summaries and study notes. It’s been super useful, so I hope it helps you too—whether for school, work, or just for fun!