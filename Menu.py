import subprocess
import os
import sys

# Ensure environment paths are set
os.environ["PATH"] += ";C:\\Users\\indigit\\AppData\\Local\\Programs\\Tesseract-OCR\\"
os.environ["PATH"] += ";C:\\Users\\indigit\\AppData\\Local\\Programs\\Ollama\\"

# Define image paths
image_paths = [
  "/Users/indigit/Desktop/ImageTranscriber/TranscribeImages/school.png"
]

# Menu options
def display_menu():
    print("WELCOME TO THE IMAGE TRANSCRIBING TOOL\n======================================\nSelect an option:")
    print("1. OCR Image Transcription (English only)")
    print("2. LLAVA Image Transcription")
    print("3. Exit")
    print("4. Instruction")

# Function to run OCR transcription (Tesseract)
def ocr_transcription():
    from PIL import Image
    import pytesseract

    def image_to_text(image_path, lang='eng'):
        try:
            with Image.open(image_path) as img:
                text_data = pytesseract.image_to_string(img, config=f'--oem 1 --psm 1', lang=lang)
            return text_data
        except Exception as e:
            return f"Error processing {image_path}: {str(e)}"

    print("OCR Image Transcription (English only)")
    for path in image_paths:
        print(f"Processing {path}:")
        final_extracted_text = image_to_text(path)
        print(f"\n{final_extracted_text}\n")

# Function to run LLAVA transcription
def llava_transcription():
    print("LLAVA Image Transcription")
    for image in image_paths:
        print(f"Processing: {image}")
        command = [
            "ollama", 
            "run", 
            "llava", 
            f"Describe what you see in this picture and transcribe any text you see {image}"
        ]
        subprocess.run(command)

# Main loop for menu interaction
def main():
    while True:
        display_menu()
        choice = input("Enter your method: ").strip()

        if choice == '1':
            ocr_transcription()
        elif choice == '2':
            llava_transcription()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.\n")

if __name__ == "__main__":
    main()
