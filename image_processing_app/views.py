# image_processing_app/views.py
from django.shortcuts import render
from django.conf import settings
from .forms import UploadImageForm
from .models import VideoQualityMetrics
from pathlib import Path
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import logging
import os

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
            uploaded_image = form.save()
            logger.info(f"Image successfully uploaded to {uploaded_image.image.url}")
            return render(request, 'index.html', {'form': form, 'message': 'Image uploaded successfully'})
        else:
            logger.error("Form is not valid")
    else:
        form = UploadImageForm()
    return render(request, 'index.html', {'form': form})

def upload_image(request):
    logger.info("Starting upload_image view")
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            logger.info(f"Image successfully uploaded to {uploaded_image.image.url}")
            return render(request, 'upload_image.html', {'form': form, 'message': 'Image uploaded successfully'})
        else:
            logger.error("Form is not valid")
    else:
        form = UploadImageForm()
    return render(request, 'upload_image.html', {'form': form})