from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import os

# Load the processor and model for printed text
processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-printed')
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-printed')

# Specify the folder containing images
image_folder = os.path.expanduser("~/Desktop/Projects/ImageTranscriber/TranscribeImages")
output_file = os.path.expanduser("~/Desktop/Projects/ImageTranscriber/transcription_results.txt")

def transcribe_images(folder, output):
    # Check if the folder exists
    if not os.path.exists(folder):
        print(f"Error: Folder '{folder}' does not exist.")
        return

    # Collect all image files in the folder
    image_files = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

    if not image_files:
        print(f"No image files found in folder: {folder}")
        return

    print(f"Found {len(image_files)} images in '{folder}'.")

    # Open the output file for writing
    with open(output, "w") as file:
        for image_file in image_files:
            image_path = os.path.join(folder, image_file)

            try:
                # Load and preprocess the image
                image = Image.open(image_path).convert("RGB")
                pixel_values = processor(images=image, return_tensors="pt").pixel_values

                # Generate transcription with enhanced parameters
                generated_ids = model.generate(
                    pixel_values,
                    max_length=50,  # Increase for longer text
                    num_beams=5,    # Use beam search for better results
                    early_stopping=True
                )
                generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

                # Write the result to the file
                file.write(f"Image: {image_file}\n")
                file.write(f"Transcription: {generated_text}\n\n")

                print(f"Transcribed '{image_file}': {generated_text}")

            except Exception as e:
                print(f"Error processing '{image_file}': {e}")

    print(f"Transcription results saved to '{output}'.")

# Run the transcription function
transcribe_images(image_folder, output_file)
