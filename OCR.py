# OCR.py

from PIL import Image
import pytesseract

def image_to_text(image_path, lang='eng'):
    """
    Return OCR text or an error message.
    """
    try:
        with Image.open(image_path) as img:
            return pytesseract.image_to_string(img, config='--oem 1 --psm 1', lang=lang).strip()
    except Exception as e:
        return f"[OCR ERROR] {e}"

def ocr_transcribe(image_path):
    """
    Return the OCR transcription for one image.
    """
    txt = image_to_text(image_path)
    return txt if txt else "No text detected."
