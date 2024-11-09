# image_processing_app/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadImageForm
from .models import VideoQualityMetrics
from pathlib import Path
import logging
from agh_vqis import VQIs, process_single_mm_file  # Import the necessary functions and classes

logger = logging.getLogger(__name__)

def custom_process_image(image_path, output_dir):
    logger.info(f"Starting custom_process_image with image_path: {image_path} and output_dir: {output_dir}")
    try:
        logger.info(f"Processing image: {image_path}")
        vqis_processor = VQIs()  # Initialize the VQIs processor
        
        # Define the output file path
        output_file = output_dir / f"VQIs_for_{image_path.stem}.csv"
        
        # Process the file
        try:
            result = process_single_mm_file(image_path, vqis_processor)
        except Exception as e:
            logger.error(f"Skipping {image_path}: Error during processing - {e}")
            return None
        
        # Check if the generated CSV file exists
        if output_file.exists():
            logger.info(f"VQIS result file generated: {output_file}")
            return output_file
        else:
            logger.error(f"Error: Expected output file {output_file} not found.")
            return None
    except Exception as e:
        logger.error(f"Error processing {image_path}: {e}")
        return None

def upload_image(request):
    logger.info("Starting upload_image view")
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            image_path = Path('uploads') / image.name
            output_dir = Path('outputs')
            output_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Uploading image to {image_path}")
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            result_file = custom_process_image(image_path, output_dir)
            if result_file:
                logger.info(f"VQIS result file: {result_file}")
                with open(result_file, 'r') as file:
                    response = HttpResponse(file.read(), content_type='text/csv')
                    response['Content-Disposition'] = f'attachment; filename="{result_file.name}"'
                    return response
            else:
                logger.error("Error processing image")
                return HttpResponse("Error processing image", status=500)
        else:
            logger.error("Form is not valid")
    else:
        form = UploadImageForm()
    return render(request, 'upload_image.html', {'form': form})

def index(request):
    logger.info("Starting index view")
    form = UploadImageForm()
    return render(request, 'index.html', {'form': form})

def archive(request):
    logger.info("Starting archive view")
    metrics = VideoQualityMetrics.objects.all()
    return render(request, 'archive.html', {'metrics': metrics})

def home(request):
    logger.info("Starting home view")
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            image_path = Path('uploads') / image.name
            output_dir = Path('outputs')
            output_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Uploading image to {image_path}")
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            result_file = custom_process_image(image_path, output_dir)
            if result_file:
                with open(result_file, 'r') as file:
                    response = HttpResponse(file.read(), content_type='text/csv')
                    response['Content-Disposition'] = f'attachment; filename="{result_file.name}"'
                    return response
            else:
                return HttpResponse("Error processing image", status=500)
    else:
        form = UploadImageForm()
    return render(request, 'index.html', {'form': form})