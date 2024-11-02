# image_processing/image_processing_app/views.py

from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import UploadedImage, VideoQualityMetrics
from agh_vqis import VQIs
from pathlib import Path
import csv

def calculate_vqis(image_path):
    vqis_processor = VQIs()  # Initialize the VQIs processor
    try:
        # Assuming VQIs class has a method to process a single file and generate a CSV file
        result_file = vqis_processor.process_file(Path(image_path))
        print(f"VQIS result file: {result_file}")  # Debugging statement
        
        # Read the CSV file and extract data
        vqis_result = {}
        with open(result_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                for key, value in row.items():
                    vqis_result[key] = value
        
        print(f"VQIS result data: {vqis_result}")  # Debugging statement
        return vqis_result
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return {"Error": "File not found"}
    except csv.Error as e:
        print(f"CSV error: {e}")
        return {"Error": "CSV error"}
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return {"Error": "Error calculating VQIS"}

def index(request):
    form = ImageUploadForm()
    return render(request, 'index.html', {'form': form})

def archive(request):
    metrics = VideoQualityMetrics.objects.all()
    return render(request, 'archive.html', {'metrics': metrics})

def home(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            # Process the image and calculate VQIS
            vqis_result = calculate_vqis(uploaded_image.image.path)
            uploaded_image.vqis_result = vqis_result
            uploaded_image.save()
            return render(request, 'results.html', {'vqis_result': vqis_result})
    else:
        form = ImageUploadForm()
    return render(request, 'index.html', {'form': form})