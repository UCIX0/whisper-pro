# NVIDIA/CUDA Library Configuration Fix

> 🇺🇸 **[English](./README_NVIDIA.md)** | 🇪🇸 **[Español](./README_NVIDIA_ES.md)**

This document explains a common issue encountered when using pip-installed NVIDIA libraries (`nvidia-cublas-cu12`, `nvidia-cudnn-cu12`) on Linux and how I have solved it automatically for this project.

## The Issue: "Could not load library"

When `faster-whisper` (via `ctranslate2`) attempts to run on the GPU, it requires access to shared libraries like `libcublas.so` and `libcudnn.so`.

Even though these libraries are installed in your environment via pip:
- `nvidia-cublas-cu12`
- `nvidia-cudnn-cu12`

Linux's dynamic linker usually does not know where to find them because they reside deeply nested inside the python `site-packages` directory, for example:
`/path/to/env/lib/python3.10/site-packages/nvidia/cudnn/lib`

Without explicit configuration, you might see errors like:
> `RuntimeError: Library cudnn is not found or cannot be loaded`
> `Could not load library libcudnn_ops_infer.so.8. Error: libcudnn_ops_infer.so.8: cannot open shared object file: No such file or directory`

## The Solution: Conda Activation Scripts

To fix this robustly without requiring every user to manually export variables every time, I have implemented **Conda Activation Scripts**.

These scripts automatically run when you activate or deactivate the environment.

### 1. Activation Script (`activate.d`)

I created a script at:
`$CONDA_PREFIX/etc/conda/activate.d/nvidia_vars.sh`

**Content:**
```bash
#!/bin/sh

# Save the old LD_LIBRARY_PATH to restore it later
export OLD_LD_LIBRARY_PATH=$LD_LIBRARY_PATH

# Add the paths to the nvidia pip packages to LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib/python3.10/site-packages/nvidia/cudnn/lib:$CONDA_PREFIX/lib/python3.10/site-packages/nvidia/cublas/lib:$CONDA_PREFIX/lib/python3.10/site-packages/nvidia/cudart/lib:$LD_LIBRARY_PATH
```

This ensures that as soon as you do `conda activate whispert`, the system knows exactly where to find the NVIDIA libraries.

### 2. Deactivation Script (`deactivate.d`)

I also created a script at:
`$CONDA_PREFIX/etc/conda/deactivate.d/nvidia_vars.sh`

**Content:**
```bash
#!/bin/sh

# Restore the original LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$OLD_LD_LIBRARY_PATH
unset OLD_LD_LIBRARY_PATH
```

This cleans up your environment variables when you leave the project environment (`conda deactivate`), preventing conflicts with other projects.

## Verification

You can verify this fix is active by running:

```bash
conda activate whispert
echo $LD_LIBRARY_PATH
```

You should see the paths containing `.../site-packages/nvidia/...` at the beginning of the output.
