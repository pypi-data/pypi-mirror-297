import os
import subprocess
import sys
from pathlib import Path
from .env_manager import (
    check_extracted,
    download_zip,
    extract_zip,
    cleanup,
    EXTRACT_DIR,
    ZIP_FILE,
    ZIP_URL
)

def setup_embedded_python():
    """Setup the embedded Python by downloading and extracting it if necessary."""
    if not check_extracted(EXTRACT_DIR):
        print("Embedded Python not found. Attempting to download and extract.")
        download_zip(ZIP_URL, ZIP_FILE)
        extract_zip(ZIP_FILE, EXTRACT_DIR)
        cleanup(ZIP_FILE)
    else:
        print(f"Embedded Python already exists at {EXTRACT_DIR}.")

def ensure_virtualenv_installed(python_path):
    """Ensure the 'virtualenv' package is installed in the given Python interpreter."""
    try:
        subprocess.run([str(python_path), "-m", "virtualenv", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print(f"Installing 'virtualenv' in embedded Python at {python_path}...")
        subprocess.run([str(python_path), "-m", "pip", "install", "virtualenv"], check=True)

def create_virtualenv(venv_name):
    """Create a virtual environment using the predefined embedded Python interpreter path."""
    setup_embedded_python()  # Ensure the embedded Python is ready

    python_path = EXTRACT_DIR / 'python.exe'  # Use the predefined path to the embedded Python
    
    if python_path.exists():
        print(f"Embedded Python found at: {python_path}")
    else:
        # Fallback to system Python if embedded Python is not found
        print("Embedded Python not found. Using the current Python interpreter.")
        python_path = Path(sys.executable)

    if os.path.exists(venv_name):
        print(f"Virtual environment '{venv_name}' already exists.")
        return

    ensure_virtualenv_installed(python_path)

    print(f"Creating virtual environment '{venv_name}' using {python_path}...")
    subprocess.run([str(python_path), "-m", "virtualenv", venv_name])
    print(f"Virtual environment '{venv_name}' created successfully.")
