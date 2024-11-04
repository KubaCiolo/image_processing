# image_processing_app/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadImageForm
from .models import VideoQualityMetrics
from pathlib import Path
import logging
from agh_vqis import VQIs, process_single_mm_file  # Import the necessary functions and classes
import io

logger = logging.getLogger(__name__)

def custom_process_image(image_path):
    logger.info(f"Starting custom_process_image with image_path: {image_path}")
    try:
        logger.info(f"Processing image: {image_path}")
        vqis_processor = VQIs()  # Initialize the VQIs processor
        
        # Create an in-memory file-like object to store the CSV content
        output_file = io.StringIO()
        
        # Process the file
        try:
            result = process_single_mm_file(image_path, vqis_processor, output_file)
        except Exception as e:
            logger.error(f"Error during processing {image_path} - {e}")
            return None
        
        # Get the CSV content from the in-memory file-like object
        csv_content = output_file.getvalue()
        output_file.close()
        
        logger.info(f"VQIS result file generated for {image_path}")
        return csv_content
    except Exception as e:
        logger.error(f"Error processing {image_path}: {e}")
        return None

def upload_image(request):
    logger.info("Starting upload_image view")
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            
            # Define the path to save the uploaded image
            image_path = Path('uploads') / image.name
            
            # Ensure the uploads directory exists
            image_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save the uploaded image to the defined path
            logger.info(f"Uploading image to {image_path}")
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            # Process the image and get the CSV content
            csv_content = custom_process_image(image_path)
            if csv_content:
                logger.info(f"VQIS result file generated for {image_path}")
                response = HttpResponse(csv_content, content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="VQIs_for_{image_path.stem}.csv"'
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
            
            # Define the path to save the uploaded image
            image_path = Path('uploads') / image.name
            
            # Ensure the uploads directory exists
            image_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save the uploaded image to the defined path
            logger.info(f"Uploading image to {image_path}")
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            # Process the image and get the CSV content
            csv_content = custom_process_image(image_path)
            if csv_content:
                response = HttpResponse(csv_content, content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="VQIs_for_{image_path.stem}.csv"'
                return response
            else:
                return HttpResponse("Error processing image", status=500)
    else:
        form = UploadImageForm()
    return render(request, 'index.html', {'form': form})