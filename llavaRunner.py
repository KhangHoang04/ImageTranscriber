# llavaRunner.py

import os
import subprocess
from config import ROOT_IMAGE_DIR  # Import ROOT_IMAGE_DIR from config

def get_image_paths(directory):
    image_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                image_paths.append(os.path.join(root, file))
    return image_paths

def llava_transcription():
    image_paths = get_image_paths(ROOT_IMAGE_DIR)  # Use ROOT_IMAGE_DIR from config
    print("LLAVA Image Transcription")

    if not image_paths:
        print("No images found in the directory.\n")
        return

    for image in image_paths:
        print(f"Processing: {image}")
        command = [
            "ollama", 
            "run", 
            "llava", 
            f"List all visible objects, features, and text exactly as they appear in the image. Do not include any interpretations, assumptions, or inferred details. Keep transcription concise yet detailed. Transcribe any text exactly as shown:  {image}"
        ]
        subprocess.run(command)
