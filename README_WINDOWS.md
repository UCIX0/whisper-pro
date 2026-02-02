# Whisper Pro on Windows: Installation and Usage Guide

> ⚠️ **Warning**: This application was primarily designed and optimized for **Linux**. Windows compatibility is functional but may exhibit instabilities or not receive the same level of maintenance as the Linux version. Future features may not be compatible.

This guide details the steps and specifics for running **Whisper Pro** in a Windows environment with GPU acceleration.

---

## 1. Prerequisites

Ensure you have the following software installed on your system:

1.  **NVIDIA GPU**: A CUDA-compatible NVIDIA graphics card.
2.  **NVIDIA Drivers**: The latest Game Ready or Studio drivers.
    *   **Verification**: Open a terminal (PowerShell or CMD) and run `nvidia-smi`. You should see your GPU details and driver version.
3.  **Conda**: Anaconda or Miniconda package manager.
    *   **Verification**: Run `conda --version` in the terminal.
4.  **Node.js**: LTS version is recommended.
    *   **Verification**: Run `node --version` in the terminal.

---

## 2. Environment Setup

The setup process is similar to Linux, but you will use Windows-specific scripts.

### a. Clone the Repository
```powershell
git clone https://github.com/your-repo/whisper-pro.git
cd whisper-pro
```

### b. Create the Conda Environment
Use the same `environment.yml` file to create the environment. It contains all Python dependencies, including the CUDA libraries needed by `faster-whisper`.

```powershell
# Create the environment named 'whispert'
conda env create -f environment.yml

# Activate the new environment
conda activate whispert
```

### c. Install Node.js Dependencies
```powershell
# Install the frontend packages
npm install
```

---

## 3. Launching the Application on Windows

Unlike Linux which uses `start.sh`, on Windows, you must use the **`start.bat`** script.

```powershell
./start.bat
```

### What does the `start.bat` script do?

This script is designed to automate Windows-specific configuration:

1.  **Configures the PATH**: It finds your Conda environment's path and **automatically adds the `bin` folders** of the `cudnn`, `cublas`, and `cudart` libraries (installed via pip) to the system's `PATH`. This is crucial for Windows to find the NVIDIA DLLs and is the equivalent of setting `LD_LIBRARY_PATH` on Linux.
2.  **Activates the Environment**: Executes `conda activate whispert`.
3.  **Frees the Port**: Kills any process left running on port `8001` from previous executions to prevent conflicts.
4.  **Starts the Backend**: Launches the FastAPI server in a new terminal window.
5.  **Starts the Frontend**: Launches the Vite development server (React) in another window.

Once the script finishes, the application will be available at:
-   **Frontend**: `http://localhost:5173`
-   **API (Backend)**: `http://localhost:8001`

---

## 4. Environment Verification

If you encounter issues, you can use the verification script to diagnose your setup. This script is compatible with Windows.

```powershell
# Make sure the 'whispert' environment is activated
python verify_env.py
```

The script will check your Python version, package installations, GPU visibility, and whether the CUDA library paths are correctly set in the `PATH` for Windows. Follow its guidance if it reports any `[FAIL]`.
