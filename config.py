# config.py

import os
import platform
import shutil

def get_command_path(command_name, default_path=None):
    path = shutil.which(command_name)
    if path:
        return path
    if default_path and os.path.exists(default_path):
        return default_path
    raise FileNotFoundError(f"'{command_name}' not found. Ensure it is installed and on PATH.")

def append_to_path(binary_path, separator):
    directory = os.path.dirname(binary_path)
    if directory not in os.environ["PATH"]:
        os.environ["PATH"] += f"{separator}{directory}"

# Platform defaults
if platform.system() == 'Windows':
    TESSERACT_DEFAULT = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    OLLAMA_DEFAULT    = r"C:\Program Files\Ollama\ollama.exe"
    SEP = ";"
elif platform.system() == 'Darwin':
    TESSERACT_DEFAULT = "/opt/homebrew/bin/tesseract"
    OLLAMA_DEFAULT    = "/usr/local/bin/ollama"
    SEP = ":"
else:
    TESSERACT_DEFAULT = "/usr/bin/tesseract"
    OLLAMA_DEFAULT    = "/usr/bin/ollama"
    SEP = ":"

TESSERACT_PATH = get_command_path("tesseract", TESSERACT_DEFAULT)
OLLAMA_PATH    = get_command_path("ollama",   OLLAMA_DEFAULT)

append_to_path(TESSERACT_PATH, SEP)
append_to_path(OLLAMA_PATH,    SEP)

# Input directory (can override via env)
if "ROOT_IMAGE_DIR" not in os.environ:
    os.environ["ROOT_IMAGE_DIR"] = os.path.join(os.getcwd(), "TranscribeImages")
ROOT_IMAGE_DIR = os.environ["ROOT_IMAGE_DIR"]

# Output directory
OUTPUT_DIR = os.path.join(os.getcwd(), "TranscriptionOutput")
if not os.path.isdir(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
