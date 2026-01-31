# Environment Setup Instructions

> 🇺🇸 **[English](./README_ENV.md)** | 🇪🇸 **[Español](./README_ENV_ES.md)**


This guide will help you recreate the exact development environment for `whisper-pro` using the generated configuration files.

## 1. Python / Conda Environment

We have created an `environment.yml` file that contains all the conda and pip packages used in the project.

### Create the Environment
To create the `whispert` environment from the file, run:

```bash
conda env create -f environment.yml
```

### Activate the Environment
Once created, activate it with:

```bash
conda activate whispert
```

### Update an Existing Environment
If you already have an environment named `whispert` and want to update it to match this configuration:

```bash
conda env update -f environment.yml --prune
```

## 2. Node.js / NPM Dependencies

We have created a `package.json` file with the exact versions of the npm packages.

### Install Dependencies
Run the following command in the project root to install the node modules:

```bash
npm install
```

## 3. Verification

After installation, you can verify the environment:

**Python:**
```bash
conda list
# Should match the provided list
```

**NPM:**
```bash
npm list
# Should match the provided list
```

## 4. GPU Support & CUDA Configuration (Important)

This project uses `faster-whisper` and `ctranslate2`, which rely on NVIDIA libraries for GPU acceleration.

### Prerequisites
1.  **NVIDIA Driver**: You must have a compatible NVIDIA Driver installed on your host system (Linux).
    - Checks: Run `nvidia-smi` in your terminal. You should see your GPU listed and a Driver Version.

### Configuration
The environment installs necessary CUDA libraries (cuBLAS, cuDNN) via pip packages (`nvidia-cublas-cu12`, `nvidia-cudnn-cu12`). However, strictly relying on pip packages sometimes requires setting `LD_LIBRARY_PATH` so the application can locate them at runtime.

**Activator Script (Recommended)**:
We recommend creating a small activation script or adding this to your `.bashrc` / `.zshrc` *after* activating the environment:

```bash
conda activate whispert

# Export specific paths to the pip-installed NVIDIA libraries
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib/python3.10/site-packages/nvidia/cudnn/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib/python3.10/site-packages/nvidia/cublas/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib/python3.10/site-packages/nvidia/cudart/lib:$LD_LIBRARY_PATH
```

Without this, you might encounter errors like `Could not load library libcudnn_ops_infer.so.8`.

### Verification of GPU Access
To confirm that `faster-whisper` can see your GPU, you can run a quick Python check:

```python
from faster_whisper import WhisperModel
import torch

print(f"PyTorch CUDA Available: {torch.cuda.is_available()}")
# Note: faster-whisper uses CTranslate2, not PyTorch directly for inference, 
# but checking PyTorch CUDA availability is a good proxy for driver health.

try:
    model = WhisperModel("tiny", device="cuda", compute_type="float16")
    print("Success: Model loaded on GPU!")
except Exception as e:
    print(f"Error loading on GPU: {e}")
```

## 5. Automated Verification

We have included a script `verify_env.py` to automatically check your environment configuration, dependencies, and GPU setup.

### Usage
Make sure your environment is activated, then run:

```bash
python verify_env.py
```

The script will produce a color-coded report:
- **[OK] Green**: passed.
- **[FAIL] Red**: Verification failed (e.g., missing package, GPU not visible).
- **[WARN] Yellow**: Potential issue (e.g. missing LD_LIBRARY_PATH).

If successful, you will see:
> **SUCCESS:** Your environment looks perfect! Ready to launch.

