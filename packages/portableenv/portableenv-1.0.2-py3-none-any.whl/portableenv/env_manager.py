import os
import zipfile
import urllib.request
import subprocess
from pathlib import Path
import platform

# Constants
ZIP_URL = 'https://github.com/abdulrahimpds/python_embedded/raw/main/python/python_embedded_3.10.9.zip'  # Update with actual URL
ZIP_NAME = 'python_embedded_3.10.9.zip'
APPDATA_DIR = Path(os.getenv('LOCALAPPDATA') if platform.system() == "Windows" else Path.home())
DOWNLOAD_DIR = APPDATA_DIR / 'portableenv'
ZIP_FILE = DOWNLOAD_DIR / ZIP_NAME
EXTRACT_DIR = DOWNLOAD_DIR / 'embedded_python_3.10.9'


# Ensure the download directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Check if the extracted file is there
def check_extracted(extract_dir):
    """Check if the embedded Python directory exists."""
    return extract_dir.exists() and (extract_dir / 'python.exe').exists()

# Download the zip file if not already downloaded
def download_zip(url, zip_file):
    """Download the embedded Python zip file to the designated directory."""
    if not zip_file.exists():
        print(f"Downloading {zip_file.name} from {url}...")
        urllib.request.urlretrieve(url, zip_file)
        print("Download complete.")
    else:
        print(f"{zip_file.name} already exists in {zip_file.parent}. Skipping download.")

# Extract the zip file to the specified directory
def extract_zip(zip_file, extract_to):
    """Extract the zip file to the target directory."""
    print(f"Extracting {zip_file} to {extract_to}...")
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print("Extraction complete.")

# Create a virtual environment using the extracted Python
def create_virtualenv(venv_name, python_path):
    """Create a virtual environment using the extracted Python executable."""
    print(f"Creating virtual environment '{venv_name}' using {python_path} as base interpreter...")
    result = subprocess.run(['virtualenv', venv_name, '--python', python_path])
    if result.returncode == 0:
        print(f"Virtual environment '{venv_name}' created successfully.")
    else:
        print("Failed to create virtual environment.")
        print(f"Error code: {result.returncode}")

# Delete the zip file after extraction
def cleanup(zip_file):
    """Delete the zip file after extraction."""
    if zip_file.exists():
        os.remove(zip_file)
        print(f"{zip_file.name} has been deleted.")

# Main function to orchestrate the workflow
def create_env_with_embedded_python(venv_name):
    # Step 1: Check if the embedded Python is already extracted
    if not check_extracted(EXTRACT_DIR):
        # Step 2: Download the zip file if not already downloaded
        download_zip(ZIP_URL, ZIP_FILE)
        
        # Step 3: Extract the zip file
        extract_zip(ZIP_FILE, EXTRACT_DIR)
        
        # Step 4: Delete the zip file
        cleanup(ZIP_FILE)
    else:
        print(f"Embedded Python already extracted in {EXTRACT_DIR}.")
    
    # Step 5: Create the virtual environment
    python_executable = EXTRACT_DIR / 'python.exe'
    create_virtualenv(venv_name, python_executable)
