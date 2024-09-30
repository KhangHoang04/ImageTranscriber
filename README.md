
# ImageTranscriber with Automatic Language Detection

## Description
This project is designed to use Optical Character Recognition (OCR) to transcribe text from images. It utilizes the Tesseract OCR engine, wrapped by the Python library `pytesseract`, and integrates automatic language detection using the `langdetect` library to determine the language of the text in the image and adjust the OCR accordingly.

Supported languages include:
- English
- French
- German
- Spanish
- Italian
- Dutch
- Portuguese
- Chinese (Simplified)
- Korean

The script will first attempt to detect the language of the image, and then run the appropriate OCR based on the detected language.

Here is a demonstration of the Python script performing OCR on an image:

### Before Processing:
<img src="test.png" alt="Original Image" width="400"/>

### After Processing (OCR Output):
<img src="output.png" alt="OCR Output" width="400"/>

## Prerequisites
Before you can run the ImageTranscriber project, you need to have the following installed on your system:
- Python 3.x
- `pytesseract`
- `Tesseract-OCR`
- `langdetect` for language detection

### Virtual Environment
1. Turn on the virtual environment:
   ```bash
   venv\Scripts\activate
   ```

## Installation

### Tesseract-OCR
1. Download and install Tesseract-OCR from the [official Tesseract GitHub repository](https://github.com/tesseract-ocr/tesseract).
2. During the installation, note the directory where Tesseract-OCR is installed. It is usually installed in `C:\Program Files\Tesseract-OCR` or `C:\Users\{Username}\AppData\Local\Programs\Tesseract-OCR`.
3. ****** Add Tesseract-OCR into the path ---> 
$env:PATH += ";C:\Users\indigit\AppData\Local\Programs\Tesseract-OCR\" ************
$env:PATH += ";C:\Users\indigit\AppData\Local\Programs\Ollama\"
$env:PATH += ";C:\Users\indigit\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Miniconda3 (64-bit)"

ollama run llava
>>> What are the text that this image is showing? /Users/indigit/Desktop/ImageTranscriber/house-mouse.jpg
4. Download the trained data files for the languages you need from the [Tesseract language data repository](https://github.com/tesseract-ocr/tessdata). Example language files:
   - `eng.traineddata` for English
   - `fra.traineddata` for French
   - `kor.traineddata` for Korean, etc.
5. Place the `.traineddata` files in the `tessdata` directory where Tesseract is installed.

### Python and pytesseract
1. Install Python if it's not already installed. You can download it from [python.org](https://www.python.org/downloads/).
2. Install the required Python libraries using pip:
   ```bash
   pip install pytesseract langdetect Pillow
   ```

## Usage
To use the script to extract text from an image and detect its language automatically:
1. Place your image in a known directory.
2. Modify the `image_path` variable in the script to point to your image file, e.g., `test.png`.
3. Run the script using:
   ```bash
   python script_name.py
   ```
   Replace `script_name.py` with the name of your Python script.

### Example Script:
```python
import pytesseract
from PIL import Image
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

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
    'ko': 'kor',         # Korean
}

# Function to detect the language of the text in an image
def detect_language(text):
    try:
        detected_lang = detect(text)
        print(f"Detected language: {detected_lang}")
        return detected_lang
    except LangDetectException:
        print("Language detection failed.")
        return None

# Function to convert image to text using OCR
def image_to_text(image_path, lang='eng'):
    with Image.open(image_path) as img:
        # Use pytesseract to extract text from image
        text_data = pytesseract.image_to_string(img, config=f'--oem 1 --psm 6', lang=lang)
    return text_data

# Main function that detects language and performs OCR
def ocr_with_language_detection(image_path):
    # Perform OCR in English first to detect the language
    initial_text = image_to_text(image_path, lang='eng')
    
    # Detect language from the extracted text
    detected_lang_code = detect_language(initial_text)
    
    if detected_lang_code and detected_lang_code in language_mapping:
        # Map the detected language to the correct Tesseract language code
        tesseract_lang = language_mapping[detected_lang_code]
        print(f"Using language: {tesseract_lang}")
        
        # Re-run OCR with the detected language
        final_text = image_to_text(image_path, lang=tesseract_lang)
    else:
        print("Language not supported or detection failed. Defaulting to English.")
        final_text = initial_text  # Use the initially extracted text
    
    return final_text

# Path to the image
image_path = 'test.png'

# Perform OCR with automatic language detection
final_extracted_text = ocr_with_language_detection(image_path)
print(final_extracted_text)
```

### Configure pytesseract
If Tesseract-OCR is not found automatically by pytesseract, you may need to set the path manually in the script:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```
Replace the path with the actual path where Tesseract-OCR is installed on your system.

## Troubleshooting
If you encounter any issues with running Tesseract, ensure that the Tesseract path is correctly added to your PATH environment variable, or provide the path directly in your script as shown in the configuration section.

https://www.devturtleblog.com/ollama-guide/
https://www.devturtleblog.com/llava-ollama-images-to-text/

For further assistance, refer to the [Tesseract documentation](https://tesseract-ocr.github.io/tessdoc/).

## License
This project is licensed under the MIT License - see the LICENSE file for details.
