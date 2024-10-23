#!/bin/bash

# Define image paths
image_paths=(
  "/Users/indigit/Desktop/ImageTranscriber/test.png"
  "/Users/indigit/Desktop/ImageTranscriber/school.png"
  "/Users/indigit/Desktop/ImageTranscriber/text.png"
)

# Loop through each image and run the command
for image in "${image_paths[@]}"; do
  echo "Processing: $image"
  ollama run llava "Describe what you see in this picture and transcribe any text you see. Try not to assume anything that isn't in the image. $image"
done