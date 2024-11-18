import os
import platform
import shutil

def get_command_path(command_name, default_path=None):
    """
    Attempt to find the command's path using `shutil.which`.
    If not found, return a default path or raise an error.
    """
    path = shutil.which(command_name)
    if path:
        return path

    if default_path and os.path.exists(default_path):
        # print(f"Warning: '{command_name}' not found in PATH. Using default path: {default_path}")
        return default_path

    raise FileNotFoundError(f"'{command_name}' not found. Ensure it is installed and added to PATH.")

def append_to_path(binary_path, separator):
    """Append the binary's directory to PATH if not already present."""
    binary_dir = os.path.dirname(binary_path)
    if binary_dir not in os.environ["PATH"]:
        os.environ["PATH"] += f"{separator}{binary_dir}"

def get_image_files(directory, recursive=False):
    """Retrieve image files from the specified directory."""
    if not os.path.exists(directory):
        print(f"Directory does not exist: {directory}")
        return []
    
    image_extensions = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')
    if recursive:
        files = [os.path.join(root, file) for root, _, filenames in os.walk(directory) for file in filenames if file.lower().endswith(image_extensions)]
    else:
        files = [os.path.join(directory, file) for file in os.listdir(directory) if file.lower().endswith(image_extensions)]
    
    if not files:
        print(f"No image files found in directory: {directory}")
    return files

# Platform-specific configurations
if platform.system() == 'Windows':
    TESSERACT_DEFAULT = r"C:\Users\indigit\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
    OLLAMA_DEFAULT = r"C:\Users\indigit\AppData\Local\Programs\Ollama\ollama.exe"
    PATH_SEPARATOR = ";"
elif platform.system() == 'Darwin':  # macOS
    TESSERACT_DEFAULT = "/opt/homebrew/bin/tesseract"
    OLLAMA_DEFAULT = "/usr/local/bin/ollama"
    PATH_SEPARATOR = ":"
else:  # Linux or other Unix-like systems
    TESSERACT_DEFAULT = "/usr/bin/tesseract"
    OLLAMA_DEFAULT = "/usr/bin/ollama"
    PATH_SEPARATOR = ":"

# Paths to required binaries, using `get_command_path`
TESSERACT_PATH = get_command_path("tesseract", TESSERACT_DEFAULT)
OLLAMA_PATH = get_command_path("ollama", OLLAMA_DEFAULT)

# Append paths to the environment if necessary
append_to_path(TESSERACT_PATH, PATH_SEPARATOR)
append_to_path(OLLAMA_PATH, PATH_SEPARATOR)

# Set ROOT_IMAGE_DIR dynamically if not already set
if "ROOT_IMAGE_DIR" not in os.environ:
    os.environ["ROOT_IMAGE_DIR"] = r"/Users/khang/Desktop/Projects/ImageTranscriber/TranscribeImages"

ROOT_IMAGE_DIR = os.environ["ROOT_IMAGE_DIR"]

# Ensure the directory exists
# if not os.path.exists(ROOT_IMAGE_DIR):
#     print(f"Creating directory: {ROOT_IMAGE_DIR}")
#     os.makedirs(ROOT_IMAGE_DIR)

images = get_image_files(ROOT_IMAGE_DIR, recursive=False)  # Set recursive=True if needed
if images:
    print(f"Found {len(images)} image(s)")
else:
    print("No images found in the directory.")
