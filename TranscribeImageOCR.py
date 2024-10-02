import pytesseract
from PIL import Image

# Function to convert image to text using OCR
def image_to_text(image_path, lang='eng'):
    try:
        with Image.open(image_path) as img:
            # Use pytesseract to extract text from image
            text_data = pytesseract.image_to_string(img, config=f'--oem 1 --psm 1', lang=lang)
        return text_data
    except Exception as e:
        return f"Error processing {image_path}: {str(e)}"

# Main function to perform OCR (default is English only)
def ocr_with_language(image_path):
    # Perform OCR with English language only
    final_text = image_to_text(image_path, lang='eng')
    return final_text

# Paths to the images you want to process
image_paths = [
    'test.png',
    'test2.png',
]

# Iterate through the image paths and perform OCR
for path in image_paths:
    print(f"Processing {path}:")
    
    final_extracted_text = ocr_with_language(path)
    print(f"{final_extracted_text}\n")
