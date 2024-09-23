import sys
from portableenv import create_virtualenv  # Import the necessary function from your package

def main():
    if len(sys.argv) != 2:
        print("Usage: python -m portableenv <venv_name>")
        sys.exit(1)
    venv_name = sys.argv[1]
    create_virtualenv(venv_name)  # Call your function to create the virtual environment

if __name__ == "__main__":
    main()
