import os
import sys
import subprocess

def create_virtualenv(venv_name):
    """Function to create a virtual environment."""
    if os.path.exists(venv_name):
        print(f"Virtual environment '{venv_name}' already exists.")
        return
    
    print(f"Creating virtual environment '{venv_name}'...")
    subprocess.run([sys.executable, "-m", "venv", venv_name])
    print(f"Virtual environment '{venv_name}' created successfully.")