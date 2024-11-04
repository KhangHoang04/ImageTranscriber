# llavaRunner.py

import os
import subprocess

# Define root directory for images
root_image_dir = "/Users/khang/Desktop/Projects/ImageTranscriber/TranscribeImages"

def get_image_paths(directory):
    image_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                image_paths.append(os.path.join(root, file))
    return image_paths

def llava_transcription():
    image_paths = get_image_paths(root_image_dir)
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
            f"Describe what you see in this picture and transcribe any text you see {image}"
        ]
        subprocess.run(command)
