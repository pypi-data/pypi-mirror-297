import os
import subprocess
import sys
from pathlib import Path
from .env_manager import EXTRACT_DIR  # Import the predefined path from env_manager.py

def ensure_virtualenv_installed(python_path):
    """Ensure the 'virtualenv' package is installed in the given Python interpreter."""
    try:
        # Check if virtualenv is already installed
        subprocess.run([str(python_path), "-m", "virtualenv", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        # Install virtualenv if not present
        print(f"Installing 'virtualenv' in embedded Python at {python_path}...")
        subprocess.run([str(python_path), "-m", "pip", "install", "virtualenv"], check=True)

def create_virtualenv(venv_name):
    """Create a virtual environment using the predefined embedded Python interpreter path."""
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

    # Ensure 'virtualenv' is installed in the embedded Python environment
    ensure_virtualenv_installed(python_path)

    print(f"Creating virtual environment '{venv_name}' using {python_path}...")
    subprocess.run([str(python_path), "-m", "virtualenv", venv_name])
    print(f"Virtual environment '{venv_name}' created successfully.")
