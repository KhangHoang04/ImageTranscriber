import pytesseract
from PIL import Image
import cv2
import numpy as np

def image_to_text(image_path, lang='eng'):
    try:
        # Load the image
        img = Image.open(image_path)

        # Convert to grayscale
        gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)

        # Apply Gaussian Blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply Otsu's thresholding for better binarization
        _, otsu_thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Resize the image to improve OCR results
        resized = cv2.resize(otsu_thresh, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

        # Use pytesseract to extract text (adjust config options)
        text_data = pytesseract.image_to_string(resized, config='--psm 6', lang=lang)
        return text_data

    except Exception as e:
        return f"Error processing {image_path}: {str(e)}"

# Function to perform OCR with a specified language
def ocr_with_language(image_path, language_code='eng'):
    if language_code in language_mapping:
        tesseract_lang = language_mapping[language_code]
        print(f"Using language: {tesseract_lang}")
        final_text = image_to_text(image_path, lang=tesseract_lang)
    else:
        print(f"Language not supported. Defaulting to English.")
        final_text = image_to_text(image_path, lang='eng')  # Default to English

    return final_text

# Supported languages
language_mapping = {
    'en': 'eng',
    'ko': 'kor',
    # Add more languages as needed
}

# Example image paths
image_paths = ['Korean.png', 'test.png']
language_codes = ['ko', 'en', 'en', 'en']

# Iterate through the images and perform OCR
for idx, path in enumerate(image_paths):
    language_code = language_codes[idx]
    extracted_text = ocr_with_language(path, language_code)
    print(f"{extracted_text}\n")
