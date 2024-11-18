import os
import subprocess
from OCR import image_to_text  # Import the OCR function
from config import ROOT_IMAGE_DIR  # Import ROOT_IMAGE_DIR from config

def get_image_paths(directory):
    image_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                image_paths.append(os.path.join(root, file))
    return image_paths

def llava_transcription_with_ocr():
    image_paths = get_image_paths(ROOT_IMAGE_DIR)  # Use ROOT_IMAGE_DIR from config
    print("LLAVA Image Transcription with OCR Integration")

    if not image_paths:
        print("No images found in the directory.\n")
        return

    for image in image_paths:
        print(f"Processing: {image}")
        
        # Perform OCR on the image
        ocr_text = image_to_text(image)
        ocr_text = ocr_text.strip() if ocr_text else "No text detected by OCR."

        # LLAVA command with OCR output as part of the prompt
        prompt = (
            f"Transcribe the content of this image while preserving its original formatting as much as possible. "
            f"Include visible objects, features, and text, ensuring alignment with the detected structure:\n\n{ocr_text}"
        )
        command = [
            "ollama", 
            "run", 
            "llava", 
            f"{prompt}", 
            f"{image}"
        ]
        
        # Execute the command
        subprocess.run(command)

