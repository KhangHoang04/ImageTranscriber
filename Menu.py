# Menu.py

import os
from OCR import ocr_transcription
from llavaRunner import llava_transcription

# Ensure environment paths are set
os.environ["PATH"] += ";C:\\Users\\indigit\\AppData\\Local\\Programs\\Tesseract-OCR\\"
os.environ["PATH"] += ";C:\\Users\\indigit\\AppData\\Local\\Programs\\Ollama\\"

# Menu options
def display_menu():
    print("WELCOME TO THE IMAGE TRANSCRIBING TOOL\n======================================\nSelect an option:")
    print("1. OCR Image Transcription (English only)")
    print("2. LLAVA Image Transcription")
    print("3. Exit")

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
