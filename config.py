import os
import subprocess
import platform

def get_command_path(command_name, default_path=None):
    """
    Attempt to find the command's path using `which` (Unix) or `where` (Windows).
    If not found, return a default path.
    """
    # Determine the command based on the OS
    command = 'where' if platform.system() == 'Windows' else 'which'

    try:
        # Run the `which` or `where` command to locate the binary
        result = subprocess.check_output([command, command_name], stderr=subprocess.STDOUT)
        return result.decode('utf-8').strip()
    except subprocess.CalledProcessError:
        if default_path:
            print(f"Warning: '{command_name}' not found. Using default path: {default_path}")
            return default_path
        else:
            raise FileNotFoundError(f"'{command_name}' not found in PATH. Please install it or set the correct PATH.")

# Set default paths based on OS
if platform.system() == 'Windows':
    TESSERACT_DEFAULT = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    OLLAMA_DEFAULT = r"C:\Program Files\Ollama\ollama.exe"
    PATH_SEPARATOR = ";"
else:  # macOS/Linux
    TESSERACT_DEFAULT = "/opt/homebrew/bin/tesseract"
    OLLAMA_DEFAULT = "/usr/local/bin/ollama"
    PATH_SEPARATOR = ":"

# Paths to required binaries, using `get_command_path`
TESSERACT_PATH = get_command_path("tesseract", TESSERACT_DEFAULT)
OLLAMA_PATH = get_command_path("ollama", OLLAMA_DEFAULT)

# Root directory for images
ROOT_IMAGE_DIR = os.getenv("ROOT_IMAGE_DIR", os.path.join(os.path.expanduser("~"), "Desktop/Projects/ImageTranscriber/TranscribeImages"))

# Ensure Tesseract and Ollama paths are added to the PATH
if TESSERACT_PATH not in os.environ["PATH"]:
    os.environ["PATH"] += f"{PATH_SEPARATOR}{TESSERACT_PATH}"
if OLLAMA_PATH not in os.environ["PATH"]:
    os.environ["PATH"] += f"{PATH_SEPARATOR}{OLLAMA_PATH}"
