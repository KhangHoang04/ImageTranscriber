import pytesseract
from PIL import Image

# Supported languages and their codes in Tesseract
language_mapping = {
    'en': 'eng',         # English
    'fr': 'fra',         # French
    'de': 'deu',         # German
    'es': 'spa',         # Spanish
    'it': 'ita',         # Italian
    'nl': 'nld',         # Dutch
    'pt': 'por',         # Portuguese
    'zh-cn': 'chi_sim',  # Chinese Simplified
    'ko': 'kor',         # Korean (added support for Korean)
    # Add more languages as needed
}

# Function to convert image to text using OCR
def image_to_text(image_path, lang='eng'):
    try:
        with Image.open(image_path) as img:
            # Use pytesseract to extract text from image
            text_data = pytesseract.image_to_string(img, config=f'--oem 1 --psm 1', lang=lang)
        return text_data
    except Exception as e:
        return f"Error processing {image_path}: {str(e)}"

# Main function to perform OCR with a specified language
def ocr_with_language(image_path, language_code='eng'):
    if language_code in language_mapping:
        # Get the corresponding Tesseract language code
        tesseract_lang = language_mapping[language_code]
        
        # Perform OCR with the specified language
        final_text = image_to_text(image_path, lang=tesseract_lang)
    else:
        print(f"Language not supported. Defaulting to English. \n")
        final_text = image_to_text(image_path, lang='eng')  # Default to English
    
    return final_text

# Paths to the images you uploaded
image_paths = [
    'Korean.png',
    'test.png',
    'test2.png',
]

# Perform OCR on each image with the desired language (example: Korean for the first, English for others)
language_codes = ['ko', 'en', 'en', 'en', 'en']  # List of languages corresponding to each image

# Iterate through the image paths and perform OCR
for idx, path in enumerate(image_paths):
    language_code = language_codes[idx]
    print(f"Processing {path} with language {language_code}:")
    
    final_extracted_text = ocr_with_language(path, language_code)
    print(f"{final_extracted_text}\n")
