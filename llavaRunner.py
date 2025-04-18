# llavaRunner.py

import subprocess
from config import OLLAMA_PATH
from OCR import image_to_text

def llava_transcribe(image_path):
    """
    Use LLAVA (via ollama) with an improved prompt for higher fidelity.
    """
    # First, get the raw OCR to feed into prompt context
    ocr_raw = image_to_text(image_path) or "No text detected by OCR."

    # Better prompt engineering:
    # 1) Explicitly request plain text output (no quotes, no labels).
    # 2) Give two few‑shot examples of 'Image→Transcription'.
    # 3) Ask for corrections of obvious OCR misreads.
    prompt = f"""
You are a meticulous transcription assistant. Given a handwritten or printed image,
your job is to produce a clean, plain‑text transcription only (no quotes, labels,
or commentary).

When in doubt, correct obvious OCR errors (e.g., '5' vs. 'S') and preserve line breaks.

EXAMPLES:
---
Image: [photo of handwritten note saying "Meet at 10AM on 2025-04-18"]
Transcription:
Meet at 10AM on 2025-04-18

Image: [scan of printed label: "Batch #0042, Item: Nozzle XL"]
Transcription:
Batch #0042, Item: Nozzle XL
---

Now transcribe this image.  
OCR pre‑read (for context):
\"\"\"
{ocr_raw}
\"\"\"  

Provide only the cleaned transcription below:
"""

    # Call LLAVA via ollama
    cmd = [
        OLLAMA_PATH, "run", "llava",
        prompt.strip(),  # the improved prompt
        image_path
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return f"[LLAVA ERROR] {proc.stderr.strip()}"
    # Strip any accidental surrounding quotes or whitespace
    return proc.stdout.strip().strip('"').strip("'")
