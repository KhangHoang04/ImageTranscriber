import subprocess

# Define image paths
image_paths = [
    'TranscribeImages/test.png' 
]

# Loop through each image and run the command
for image in image_paths:
    print(f"Processing: {image}")
    
    # Build the ollama command
    command = [
        "ollama", 
        "run", 
        "llava", 
        f"What's in this image? {image}"
    ]
    
    # Execute the command
    subprocess.run(command)
