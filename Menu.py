from OCR import ocr_transcription
from llavaRunner import llava_transcription_with_ocr  # Updated function
import config  # Import config to initialize paths

def display_menu():
    print("WELCOME TO THE IMAGE TRANSCRIBING TOOL\n======================================\nSelect an option:")
    print("1. OCR Image to Text Transcription (English only)")
    print("2. LLAVA Image Transcription")
    print("3. LLAVA Transcription with OCR Integration")
    print("4. Exit")

def main():
    while True:
        display_menu()
        choice = input("Enter your method: ").strip()

        if choice == '1':
            ocr_transcription()
        elif choice == '2':
            llava_transcription()
        elif choice == '3':
            llava_transcription_with_ocr()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.\n")

if __name__ == "__main__":
    main()
