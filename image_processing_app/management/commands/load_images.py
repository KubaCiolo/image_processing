import os
import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from image_processing_app.models import Image

class Command(BaseCommand):
    help = 'Load images into the database'

    def handle(self, *args, **kwargs):
        base_dir = 'C:\\Users\\jakub_lk\\OneDrive\\.inżynierka\\Es_pdfs(Art2)'
        self.stdout.write(self.style.SUCCESS(f'Starting to process base directory: {base_dir}'))
        
        for root, dirs, files in os.walk(base_dir):
            self.stdout.write(self.style.SUCCESS(f'Checking directory: {root}'))
            if root.endswith('PDFs'):
                self.stdout.write(self.style.SUCCESS(f'Processing directory: {root}'))
                headlines_path = os.path.join(root, 'headlines.txt')
                self.stdout.write(self.style.SUCCESS(f'Looking for headlines.txt at: {headlines_path}'))
                if os.path.exists(headlines_path):
                    self.stdout.write(self.style.SUCCESS(f'Found headlines.txt: {headlines_path}'))
                    with open(headlines_path, 'r') as f:
                        headlines = json.load(f)
                    for headline in headlines:
                        doc_filename = headline['doc_filename']
                        pdf_pictures_dir = root + '_pictures'
                        self.stdout.write(self.style.SUCCESS(f'Checking for images in directory: {pdf_pictures_dir}'))
                        if os.path.exists(pdf_pictures_dir):
                            self.stdout.write(self.style.SUCCESS(f'Processing images in directory: {pdf_pictures_dir}'))
                            for image_filename in os.listdir(pdf_pictures_dir):
                                if image_filename.endswith(('.jpg', '.png')):
                                    image_path = os.path.join(pdf_pictures_dir, image_filename)
                                    self.stdout.write(self.style.SUCCESS(f'Uploading image: {image_path}'))
                                    with open(image_path, 'rb') as img_file:
                                        image = Image(
                                            title=image_filename,
                                            image=img_file,
                                            uploaded_at=timezone.now()
                                        )
                                        image.save()
                                        self.stdout.write(self.style.SUCCESS(f'Successfully uploaded {image_filename}'))
                        else:
                            self.stdout.write(self.style.ERROR(f'Images directory not found: {pdf_pictures_dir}'))
                else:
                    self.stdout.write(self.style.ERROR(f'headlines.txt not found in directory: {root}'))
            else:
                self.stdout.write(self.style.WARNING(f'Skipping directory: {root}'))