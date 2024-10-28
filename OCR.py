# OCR.py

import os
from PIL import Image
import pytesseract

# Define root directory for images
root_image_dir = "/Users/indigit/Desktop/ImageTranscriber/TranscribeImages"

def get_image_paths(directory):
    image_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                image_paths.append(os.path.join(root, file))
    return image_paths

def image_to_text(image_path, lang='eng'):
    try:
        with Image.open(image_path) as img:
            text_data = pytesseract.image_to_string(img, config='--oem 1 --psm 1', lang=lang)
        return text_data
    except Exception as e:
        return f"Error processing {image_path}: {str(e)}"

def ocr_transcription():
    image_paths = get_image_paths(root_image_dir)
    print("OCR Image Transcription (English only)")
    
    if not image_paths:
        print("No images found in the directory.\n")
        return

    for path in image_paths:
        print(f"Processing {path}:")
        final_extracted_text = image_to_text(path)
        
        # Check if any text was extracted
        if final_extracted_text.strip():  # if text is not empty
            print(f"\n{final_extracted_text}\n")
        else:
            print("No visible text detected, or OCR is not supported for this image.\n")
