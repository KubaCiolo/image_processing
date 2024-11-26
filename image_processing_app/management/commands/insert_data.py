import os
import re
import csv
import psycopg2
import glob
import shutil
from load_headlines import load_headlines
from datetime import datetime

# Database connection parameters
conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME', 'postgres'),
    user=os.getenv('DB_USER', 'postgres'),
    password=os.getenv('DB_PASSWORD', 'mysecretpassword'),
    host=os.getenv('DB_HOST', 'db'),  # Use the service name defined in docker-compose.yml
    port=os.getenv('DB_PORT', '5432')  # Use the internal port of the PostgreSQL container
)
cur = conn.cursor()

# Path to the directory containing CSV files
csv_files_path = '/app/data/*.csv'

# Path to the headlines file
headlines_file_path = '/app/data/headlines(Art2).txt'

# Path to the images directory within the Docker container
images_dir = '/app/images'

# Path to the media uploads directory (overwritten to use /app/media/uploads/pdf_images)
media_uploads_dir = '/app/media/uploads/pdf_images'

# Verify the images directory path
print(f"Images directory: {images_dir}")
if os.path.exists(images_dir):
    print(f"Contents of images directory: {os.listdir(images_dir)}")
else:
    print(f"Directory {images_dir} does not exist")

# Get list of all CSV files in the directory
csv_files = glob.glob(csv_files_path)

# Get list of all image files in the images directory
image_files = glob.glob(os.path.join(images_dir, '*.jpg'))

# Print the list of image files for debugging
print(f"Image files: {image_files}")

# Create a dictionary to map image names to their full paths
image_dict = {os.path.basename(img): img for img in image_files}

# Print the contents of image_dict for debugging
print(f"Total images loaded: {len(image_dict)}")
for key, value in image_dict.items():
    print(f"Image key: {key}, value: {value}")

# Expected number of columns in the CSV file (excluding vqis_filename, doc_filename, doc_headline, doc_url)
expected_columns = 17

# Load headlines data
headlines = load_headlines(headlines_file_path)
print(f"Total headlines loaded: {len(headlines)}")  # Debugging statement

# Print the loaded headlines for debugging
for key, value in headlines.items():
    print(f"Headline key: {key}, value: {value}")

# Function to insert data from a CSV file into the PostgreSQL table
def insert_data_from_csv(file_path):
    vqis_filename = os.path.basename(file_path)  # Extract the file name from the path
    # Extract doc_filename and img_name from the CSV filename using regex
    match = re.search(r'VQIs_(\d{4}-\d{2})_for_(doc_\d+_\d+_img_\d+)', vqis_filename)
    if match:
        date_part = match.group(1)
        doc_img_part = match.group(2)
        doc_filename = doc_img_part.split('_img_')[0] + '.pdf'
        img_name = doc_img_part + '.jpg'
        new_img_name = date_part + '_' + doc_img_part + '.jpg'
    else:
        doc_filename = "doc_filename_example.pdf"
        img_name = "img_name_example.jpg"
        new_img_name = "new_img_name_example.jpg"
    
    # Ensure doc_filename ends with .pdf
    if not doc_filename.endswith('.pdf'):
        doc_filename += '.pdf'
    
    # Strip any leading/trailing spaces from doc_filename
    doc_filename = doc_filename.strip()
    
    # Print the extracted doc_filename and img_name for debugging
    print(f"Extracted doc_filename: {doc_filename}")
    print(f"Extracted img_name: {img_name}")
    print(f"New image name: {new_img_name}")
    
    # Get doc_headline and doc_url from headlines data
    if doc_filename in headlines:
        doc_headline = headlines[doc_filename]['doc_headline']
        doc_url = headlines[doc_filename]['doc_url']
        print(f"Using headline for {doc_filename}: {doc_headline}, {doc_url}")  # Debugging statement
    else:
        doc_headline = "NOT FOUND"
        doc_url = "NOT FOUND"
        print(f"No headline found for {doc_filename}, using defaults")  # Debugging statement
    
    # Set the upload date
    upload_date = datetime.now()
    
    # Set the destination path for the image
    dest_image_path = os.path.join(media_uploads_dir, new_img_name)
    
    # Ensure the destination directory exists
    os.makedirs(media_uploads_dir, exist_ok=True)
    
    # Copy the image to the media uploads directory
    src_image_path = image_dict.get(img_name)
    print(f"image from {src_image_path} should be copied to {dest_image_path} in next log")
    if src_image_path:
        shutil.copy(src_image_path, dest_image_path)
        print(f"Copied image {src_image_path} to {dest_image_path}")
    else:
        print(f"Image {img_name} not found in {images_dir}")
        # Fallback: Try to find the image with a different naming convention
        for key in image_dict.keys():
            if img_name in key:
                src_image_path = image_dict[key]
                shutil.copy(src_image_path, dest_image_path)
                print(f"Copied image {src_image_path} to {dest_image_path} using fallback")
                break
    
    print(f"Processing file: {vqis_filename}")  # Print the file name to verify
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) < expected_columns:
                # Fill missing columns with default value (e.g., 0.0)
                row.extend(['0.0'] * (expected_columns - len(row)))
                print(f"Filling missing columns in {file_path}: {row}")
            elif len(row) > expected_columns:
                # Trim extra columns
                row = row[:expected_columns]
                print(f"Trimming extra columns in {file_path}: {row}")

            # Replace empty strings with '0.0' for float columns
            row = ['0.0' if x == '' else x for x in row]

            # Prepend the user_id, image, name, source_url, doc_headline, and upload_date to the row
            relative_image_path = os.path.relpath(dest_image_path, '/app/media')
            row = [3, os.path.join('uploads/pdf_images', new_img_name), new_img_name, doc_url, doc_headline, upload_date] + row
            print(f"Row to be inserted: {row}")  # Print the row to be inserted

            # Ensure the number of placeholders matches the number of values
            placeholders = ', '.join(['%s'] * len(row))
            sql = f"""
                INSERT INTO image_processing_app_videoqualitymetrics (user_id, image, name, source_url, doc_headline, upload_date, frame, blockiness, sa, letterbox, pillarbox, blockloss, blur, ta, blackout, freezing, exposure_bri, contrast, interlace, noise, slice, flickering, colourfulness)
                VALUES ({placeholders})
                ON CONFLICT (name) DO UPDATE SET
                    user_id = EXCLUDED.user_id,
                    image = EXCLUDED.image,
                    source_url = EXCLUDED.source_url,
                    doc_headline = EXCLUDED.doc_headline,
                    upload_date = EXCLUDED.upload_date,
                    frame = EXCLUDED.frame,
                    blockiness = EXCLUDED.blockiness,
                    sa = EXCLUDED.sa,
                    letterbox = EXCLUDED.letterbox,
                    pillarbox = EXCLUDED.pillarbox,
                    blockloss = EXCLUDED.blockloss,
                    blur = EXCLUDED.blur,
                    ta = EXCLUDED.ta,
                    blackout = EXCLUDED.blackout,
                    freezing = EXCLUDED.freezing,
                    exposure_bri = EXCLUDED.exposure_bri,
                    contrast = EXCLUDED.contrast,
                    interlace = EXCLUDED.interlace,
                    noise = EXCLUDED.noise,
                    slice = EXCLUDED.slice,
                    flickering = EXCLUDED.flickering,
                    colourfulness = EXCLUDED.colourfulness
            """
            try:
                cur.execute(sql, tuple(row))
                print(f"Successfully inserted row: {row}")  # Debugging statement
            except Exception as e:
                print(f"Error inserting row {row} from {file_path}: {e}")
                conn.rollback()

        conn.commit()

# Insert data from each CSV file
for csv_file in csv_files:
    try:
        insert_data_from_csv(csv_file)
        print(f"Data from {csv_file} inserted successfully.")
    except Exception as e:
        print(f"Error inserting data from {csv_file}: {e}")
        conn.rollback()

# Close the database connection
cur.close()
conn.close()