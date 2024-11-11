# image_processing_app/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.contrib import messages
from django.conf import settings
from .forms import UploadImageForm
from .models import VideoQualityMetrics
from pathlib import Path
import logging
from image_processing_app.utils.image_processing import process_image  # Import the process_image function
from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)

def index(request):
    logger.info("Starting index view")
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            
            # Define the path to save the uploaded image
            image_path = Path(settings.MEDIA_ROOT) / 'uploads' / image.name
            
            # Ensure the uploads directory exists
            image_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save the uploaded image to the defined path
            logger.info(f"Uploading image to {image_path}")
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            # Process the image using agh_vqis
            try:
                output_csv_path = process_image(image_path)
                download_link = f"/download_csv/{output_csv_path.name}"
                messages.success(request, mark_safe(f"Image processed successfully. <a href='{download_link}'>Download the results here</a>."))
            except Exception as e:
                logger.error(f"Error processing image: {e}")
                messages.error(request, "Error processing image")
            return redirect('index')
        else:
            messages.error(request, "Form is not valid")
            return redirect('index')
    else:
        form = UploadImageForm()
    return render(request, 'index.html', {'form': form})

def archive(request):
    logger.info("Starting archive view")
    metrics = VideoQualityMetrics.objects.all()
    return render(request, 'archive.html', {'metrics': metrics})

def download_csv(request, filename):
    file_path = Path(settings.MEDIA_ROOT) / 'results' / filename
    if file_path.exists():
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
        return response
    else:
        messages.error(request, "File not found")
        return redirect('index')