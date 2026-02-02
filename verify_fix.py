#!/usr/bin/env python3
import sys
import shutil
import subprocess
import os
import importlib.metadata
import platform

# ANSI Colors


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


errors = []
warnings = []


def print_header(title):
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== {title} ==={Colors.ENDC}")


def check_step(description, success, error_msg=None, is_warning=False):
    if success:
        print(f"{Colors.OKGREEN}[OK]{Colors.ENDC} {description}")
    else:
        tag = "[WARN]" if is_warning else "[FAIL]"
        color = Colors.WARNING if is_warning else Colors.FAIL
        print(f"{color}{tag}{Colors.ENDC} {description}")
        if error_msg:
            print(f"    {Colors.BOLD}Reason:{Colors.ENDC} {error_msg}")

        if is_warning:
            warnings.append(description)
        else:
            errors.append(description)


def check_command(cmd):
    return shutil.which(cmd) is not None


def check_package(package_name, min_version=None):
    try:
        version = importlib.metadata.version(package_name)
        if min_version and version < min_version:
            return False, f"Version {version} < {min_version}"
        return True, f"Installed ({version})"
    except importlib.metadata.PackageNotFoundError:
        return False, "Not installed"

def main():
    print(f"{Colors.BOLD}Starting System Verification for Whisper Pro Environment...{Colors.ENDC}")

    # 1. System Checks
    print_header("System Checks")

    # Python Version
    py_ver = sys.version_info
    check_step(f"Python 3.10+ (Current: {py_ver.major}.{py_ver.minor})",
               py_ver.major == 3 and py_ver.minor >= 10,
               "Python 3.10 or higher is required.")

    # Conda Env
    conda_prefix = os.environ.get('CONDA_PREFIX')
    check_step("Running inside a Conda environment",
               conda_prefix is not None,
               "CONDA_PREFIX not found. Please activate your environment (conda activate whispert).")

    # 2. NVIDIA & CUDA Checks
    print_header("NVIDIA & GPU Configuration")

    # nvidia-smi
    has_smi = check_command('nvidia-smi')
    check_step("NVIDIA Driver (nvidia-smi accessible)", has_smi,
               "Could not find 'nvidia-smi'. Is the NVIDIA Driver installed?")

    if has_smi:
        try:
            output = subprocess.check_output(
                ['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'], encoding='utf-8')
            print(
                f"    {Colors.OKBLUE}Detected GPU:{Colors.ENDC} {output.strip()}")
        except:
            pass

    # Dynamic library path check (LD_LIBRARY_PATH for Linux, PATH for Windows)
    is_windows = platform.system() == "Windows"
    path_var = "PATH" if is_windows else "LD_LIBRARY_PATH"
    lib_path = os.environ.get(path_var, '')

    missing_libs = []
    if conda_prefix:
        # Define paths using os.path.join for cross-platform compatibility
        base_path = os.path.join(conda_prefix, "Lib", "site-packages") if is_windows else os.path.join(conda_prefix, "lib", f"python{sys.version_info.major}.{sys.version_info.minor}", "site-packages")

        # Adjust expected paths for Windows and Linux
        if is_windows:
             expected_paths = [
                os.path.join(base_path, "nvidia", "cudnn", "bin"),
                os.path.join(base_path, "nvidia", "cublas", "bin"),
                os.path.join(base_path, "nvidia", "cudart", "bin")
            ]
        else:
            expected_paths = [
                os.path.join(base_path, "nvidia", "cudnn", "lib"),
                os.path.join(base_path, "nvidia", "cublas", "lib"),
                os.path.join(base_path, "nvidia", "cudart", "lib")
            ]

        for p in expected_paths:
            if p not in lib_path:
                missing_libs.append(p)

    check_step(f"{path_var} configured for pip NVIDIA libs",
               len(missing_libs) == 0,
               f"Missing paths in {path_var}. See README_ENV.md for fixes.\n    Missing: {missing_libs}", is_warning=False)


    # CUDA access via Python
    try:
        import torch
        cuda_avail = torch.cuda.is_available()
        check_step("PyTorch can see CUDA", cuda_avail,
                   "torch.cuda.is_available() returned False")
    except ImportError:
        check_step("PyTorch can see CUDA", False, "PyTorch not installed")

    # 3. Python Dependencies
    print_header("Python Dependencies")
    required_packages = [
        "faster-whisper",
        "ctranslate2",
        "fastapi",
        "uvicorn",
        "torch",
        "nvidia-cudnn-cu12",
        "nvidia-cublas-cu12"
    ]

    for pkg in required_packages:
        ok, msg = check_package(pkg)
        check_step(f"Package: {pkg}", ok, msg)

    # 4. Node.js Environment
    print_header("Node.js / Frontend")

    check_step("npm installed", check_command('npm'), "npm command not found")
    check_step("node_modules exists", os.path.exists("node_modules"),
               "node_modules specific folder not found. Run 'npm install'.")

    # SUMMARY
    print("\n" + "="*40)
    print_header("VERIFICATION SUMMARY")

    if not errors and not warnings:
        print(
            f"{Colors.OKGREEN}SUCCESS:{Colors.ENDC} Your environment looks perfect! Ready to launch.")
    else:
        if errors:
            print(f"{Colors.FAIL}ERRORS ({len(errors)}):{Colors.ENDC}")
            for e in errors:
                print(f" - {e}")
            print(
                f"\n{Colors.BOLD}Action Required:{Colors.ENDC} Please fix the errors above before running the project.")

        if warnings:
            print(f"{Colors.WARNING}WARNINGS ({len(warnings)}):{Colors.ENDC}")
            for w in warnings:
                print(f" - {w}")


if __name__ == "__main__":
    main()