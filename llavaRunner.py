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
        f"Describe what you see in this picture and transcribe any text you see {image}"
    ]
    
    # Execute the command
    subprocess.run(command)
