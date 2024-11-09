# image_processing_app/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from .forms import UploadImageForm
from .models import VideoQualityMetrics
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

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
            image_path = Path(settings.MEDIA_ROOT) / 'uploads' / image.name
            
            # Ensure the uploads directory exists
            image_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save the uploaded image to the defined path
            logger.info(f"Uploading image to {image_path}")
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            messages.success(request, "Image uploaded successfully")
            return redirect('home')
        else:
            messages.error(request, "Form is not valid")
            return redirect('home')
    else:
        form = UploadImageForm()
    return render(request, 'index.html', {'form': form})