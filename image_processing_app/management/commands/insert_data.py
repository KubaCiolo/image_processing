import os
import re
import csv
import psycopg2
import glob
from load_headlines import load_headlines

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
csv_files_path = '/data/*.csv'  # Use the path inside the container

# Path to the headlines file
headlines_file_path = '/data/headlines(Art2).txt'  # Use the path inside the container

# Get list of all CSV files in the directory
csv_files = glob.glob(csv_files_path)

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
    # Extract doc_filename from the CSV filename using regex
    match = re.search(r'for_(doc_\d+_\d+)_img', vqis_filename)
    doc_filename = match.group(1) + '.pdf' if match else "doc_filename_example.pdf"
    
    # Ensure doc_filename ends with .pdf
    if not doc_filename.endswith('.pdf'):
        doc_filename += '.pdf'
    
    # Strip any leading/trailing spaces from doc_filename
    doc_filename = doc_filename.strip()
    
    # Print the extracted doc_filename for debugging
    print(f"Extracted doc_filename: {doc_filename}")
    
    # Get doc_headline and doc_url from headlines data
    if doc_filename in headlines:
        doc_headline = headlines[doc_filename]['doc_headline']
        doc_url = headlines[doc_filename]['doc_url']
        print(f"Using headline for {doc_filename}: {doc_headline}, {doc_url}")  # Debugging statement
    else:
        doc_headline = "NOT FOUND"
        doc_url = "NOT FOUND"
        print(f"No headline found for {doc_filename}, using defaults")  # Debugging statement
    
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

            # Prepend the vqis_filename, doc_filename, doc_headline, and doc_url to the row
            row = [vqis_filename, doc_filename, doc_headline, doc_url] + row
            print(f"Row to be inserted: {row}")  # Print the row to be inserted

            try:
                cur.execute(
                    """
                    INSERT INTO image_processing_app_videoqualitymetrics (vqis_filename, doc_filename, doc_headline, doc_url, frame, blockiness, sa, letterbox, pillarbox, blockloss, blur, ta, blackout, freezing, "Exposure(bri)", contrast, interlace, noise, slice, flickering, colourfulness)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (vqis_filename) DO UPDATE SET
                        doc_filename = EXCLUDED.doc_filename,
                        doc_headline = EXCLUDED.doc_headline,
                        doc_url = EXCLUDED.doc_url,
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
                        "Exposure(bri)" = EXCLUDED."Exposure(bri)",
                        contrast = EXCLUDED.contrast,
                        interlace = EXCLUDED.interlace,
                        noise = EXCLUDED.noise,
                        slice = EXCLUDED.slice,
                        flickering = EXCLUDED.flickering,
                        colourfulness = EXCLUDED.colourfulness
                    """,
                    row
                )
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
