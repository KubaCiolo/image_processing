from agh_vqis import process_single_mm_file, VQIs
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Define the path to the directory containing the pictures
pictures_dir = Path(r'C:\Users\jakub_lk\OneDrive\.inżynierka\Es_pdfs(Art2)\From 2023-01-01 to 2023-01-31_3724PDFs_pictures')

# Iterate over the pictures in the directory
for picture in pictures_dir.glob('*.jpg'):  # Assuming the pictures are in .jpg format
    try:
        process_single_mm_file(picture)
    except Exception as e:
        logging.error(f"Error processing {picture}: {e}")
        continue