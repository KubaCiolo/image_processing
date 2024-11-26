import os
import django
import pandas as pd
import json
from django.conf import settings
from ...models import VideoQualityMetrics 

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

# Paths
csv_dir = r'C:\Users\jakub_lk\OneDrive\.inżynierka\data1'
headlines_file = r'C:\Users\jakub_lk\OneDrive\.inżynierka\headlines(art2).txt'
images_dir = r'C:\Users\jakub_lk\OneDrive\.inżynierka\Es_pdfs(Art2)\From 2023-01-01 to 2023-01-31_3724PDFs_pictures'

# Read headlines file
with open(headlines_file, 'r') as f:
    headlines_data = json.load(f)

# Create a dictionary for quick lookup
headlines_dict = {item['doc_filename']: item for item in headlines_data}

# Process each CSV file
for csv_file in os.listdir(csv_dir):
    if csv_file.endswith('.csv'):
        csv_path = os.path.join(csv_dir, csv_file)
        df = pd.read_csv(csv_path)

        # Extract image name from CSV filename
        image_name = csv_file.replace('.csv', '.jpg')
        image_path = os.path.join(images_dir, image_name)

        # Extract document filename from image name
        doc_filename = '_'.join(image_name.split('_')[:3]) + '.pdf'

        if doc_filename in headlines_dict:
            headline_info = headlines_dict[doc_filename]
            source_url = headline_info['doc_url']
            doc_headline = headline_info['doc_headline']

            # Insert each row into the database
            for _, row in df.iterrows():
                VideoQualityMetrics.objects.create(
                    user=settings.AUTH_USER_MODEL.objects.first(),  # Adjust user assignment as needed
                    image=image_path,
                    name=image_name,  # Use image name as the name
                    source_url=source_url,
                    doc_headline=doc_headline,  # New field
                    frame=row['Frame'],
                    blockiness=row['Blockiness'],
                    sa=row['SA'],
                    letterbox=row['Letterbox'],
                    pillarbox=row['Pillarbox'],
                    blockloss=row['Blockloss'],
                    blur=row['Blur'],
                    ta=row['TA'],
                    blackout=row['Blackout'],
                    freezing=row['Freezing'],
                    exposure_bri=row['Exposure(bri)'],
                    contrast=row['Contrast'],
                    interlace=row['Interlace'],
                    noise=row['Noise'],
                    slice=row['Slice'],
                    flickering=row['Flickering'],
                    colourfulness=0.0  # Assuming default value for colourfulness
                )