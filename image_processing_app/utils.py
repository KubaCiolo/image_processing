import os
from pathlib import Path
import csv
from PIL import Image
from agh_vqis import process_folder_w_mm_files, VQIs

def process_images(picture_dirs):
    print(f"Processing images in directories: {picture_dirs}")
    vqis = VQIs()
    for picture_dir in picture_dirs:
        print(f"Processing images in directory: {picture_dir}")
        try:
            picture_dir_path = Path(picture_dir)
            if not picture_dir_path.exists() or not picture_dir_path.is_dir():
                print(f"Directory does not exist or is not a directory: {picture_dir_path}")
                continue

            parameters = process_folder_w_mm_files(picture_dir_path, vqis)
            # Only process image files
            for image_file in picture_dir_path.glob('*.*'):
                if image_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
                    process_single_image(image_file, parameters)
        except Exception as e:
            print(f"Error processing images in directory: {picture_dir}, Error: {e}")

def process_single_image(image_file, parameters):
    print(f"Processing image: {image_file}")
    try:
        if not image_file.exists():
            print(f"File does not exist: {image_file}")
            return

        # Verify that the image is not corrupted
        try:
            with Image.open(image_file) as img:
                img.verify()  # Verify that the image is not corrupted
        except (IOError, SyntaxError) as e:
            print(f"Image is corrupted or invalid: {image_file}, Error: {e}")
            return

        # Define a consistent output directory
        output_dir = Path(r"C:\Users\jakub_lk\OneDrive\.inżynierka\image_processing\data")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Define the output file based on the image filename
        output_file = output_dir / f"VQIs_for_{image_file.stem}.csv"

        # Open the output file in write mode
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write headers as expected by the VQI data
            writer.writerow([
                "Frame", "Blockiness", "SA", "Letterbox", "Pillarbox", "Blockloss", "Blur", "TA",
                "Blackout", "Freezing", "Exposure(bri)", "Contrast", "Interlace", "Noise", "Slice", "Flickering"
            ])
            # Iterate over the parameters assuming it's a list of values
            # If parameters contain multiple rows, adjust this accordingly
            if isinstance(parameters, list):
                for parameter_row in parameters:
                    writer.writerow(parameter_row)
            else:
                writer.writerow(parameters)

        print(f"Successfully processed {image_file} and saved VQI data to {output_file}")
    except Exception as e:
        print(f"Error processing image {image_file}: {e}")

# Example usage
picture_dirs = [
    r"C:\Users\jakub_lk\OneDrive\.inżynierka\Es_pdfs(Art2)\From 2023-01-01 to 2023-01-31_3724PDFs_pictures",
    r"C:\Users\jakub_lk\OneDrive\.inżynierka\Es_pdfs(Art2)\From 2023-02-01 to 2023-02-28_3063PDFs_pictures",
    r"C:\Users\jakub_lk\OneDrive\.inżynierka\Es_pdfs(Art2)\From 2023-03-01 to 2023-03-31_1992PDFs_pictures",
    r"C:\Users\jakub_lk\OneDrive\.inżynierka\Es_pdfs(Art2)\From 2023-04-01 to 2023-04-30_5507PDFs_pictures",
    r"C:\Users\jakub_lk\OneDrive\.inżynierka\Es_pdfs(Art2)\From 2023-05-01 to 2023-05-31_1971PDFs_pictures",
    r"C:\Users\jakub_lk\OneDrive\.inżynierka\Es_pdfs(Art2)\From 2023-06-01 to 2023-06-30_2198PDFs_pictures",
    r"C:\Users\jakub_lk\OneDrive\.inżynierka\Es_pdfs(Art2)\From 2023-09-01 to 2023-09-15_329PDFs_pictures",
    r"C:\Users\jakub_lk\OneDrive\.inżynierka\Es_pdfs(Art2)\From 2023-09-16 to 2023-09-30_8750PDFs_pictures"
]

process_images(picture_dirs)