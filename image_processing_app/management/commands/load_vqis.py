import os
import csv
from django.core.management.base import BaseCommand
from image_processing_app.models import VQI

class Command(BaseCommand):
    help = 'Load VQI data from CSV files into the database'

    def handle(self, *args, **kwargs):
        base_dir = '/usr/src/app/data'
        self.stdout.write(self.style.SUCCESS(f'Starting to process base directory: {base_dir}'))

        # Check if the base directory exists
        if not os.path.exists(base_dir):
            self.stdout.write(self.style.ERROR(f'Base directory does not exist: {base_dir}'))
            return

        frame_counter = 1  # Initialize frame counter

        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith('.csv'):
                    file_path = os.path.join(root, file)
                    self.stdout.write(self.style.SUCCESS(f'Processing file: {file_path}'))
                    with open(file_path, 'r') as csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            vqi = VQI(
                                frame=frame_counter,  # Use the frame counter
                                blockiness=float(row['Blockiness']),
                                sa=float(row['SA']),
                                letterbox=float(row['Letterbox']),
                                pillarbox=float(row['Pillarbox']),
                                blockloss=float(row['Blockloss']),
                                blur=float(row['Blur']),
                                ta=float(row['TA']),
                                blackout=int(row['Blackout']),
                                freezing=int(row['Freezing']),
                                exposure_bri=float(row['Exposure(bri)']),
                                contrast=float(row['Contrast']),
                                interlace=float(row['Interlace']),
                                noise=float(row['Noise']),
                                slice=float(row['Slice']),
                                flickering=float(row['Flickering'])
                            )
                            vqi.save()
                            self.stdout.write(self.style.SUCCESS(f'Successfully uploaded frame {vqi.frame} from {file}'))
                            frame_counter += 1  # Increment the frame counter

        self.stdout.write(self.style.SUCCESS('Finished processing base directory'))