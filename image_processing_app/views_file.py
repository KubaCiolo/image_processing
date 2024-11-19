# image_processing_app/views_file.py
import logging
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse
from django.contrib import messages
from django.conf import settings
from .models import VideoQualityMetrics
from pathlib import Path
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

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

def download_from_archive(request, image_name):
    logger.info(f"Received image_name: {image_name}")
    base_name = Path(image_name).stem  # Get the base name without the extension
    filename = f"{base_name}_results.csv"
    file_path = Path(settings.MEDIA_ROOT) / 'results' / filename
    logger.info(f"Looking for file: {file_path}")
    if file_path.exists():
        logger.info(f"File found: {file_path}")
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
        return response
    else:
        logger.error(f"File not found: {file_path}")
        messages.error(request, "File not found")
        return redirect('archive')

@login_required
def delete_metric(request, metric_id):
    metric = get_object_or_404(VideoQualityMetrics, id=metric_id)
    if request.method == 'POST':
        # Delete the image file from the filesystem
        image_path = metric.image.path
        base_name = '_'.join(Path(image_path).stem.split('_')[:-1])  # Get the base name without the last part after the underscore
        extension = Path(image_path).suffix  # Get the file extension

        # Define the upload directory based on the date the file was uploaded
        upload_date = metric.upload_date  # Assuming you have an upload_date field in your model
        upload_dir = Path(settings.MEDIA_ROOT) / 'uploads' / upload_date.strftime('%Y/%m/%d')

        # Construct paths for additional files
        original_image_path = upload_dir / f"{base_name}{extension}"
        result_file_path = Path(settings.MEDIA_ROOT) / 'results' / f"{base_name}_results.csv"

        # Log the paths
        logger.info(f"Image Path: {image_path}")
        logger.info(f"Base Name: {base_name}")
        logger.info(f"Original Image Path: {original_image_path}")
        logger.info(f"Result File Path: {result_file_path}")

        # Delete the original image file
        if os.path.exists(original_image_path):
            os.remove(original_image_path)

        # Delete the result file
        if os.path.exists(result_file_path):
            os.remove(result_file_path)

        # Delete the image file associated with the metric
        if os.path.exists(image_path):
            os.remove(image_path)

        # Delete the metric from the database
        metric.delete()
        messages.success(request, "Metric and associated files deleted successfully")
        if 'profile' in request.META.get('HTTP_REFERER', ''):
            return redirect('profile')
        return redirect('archive')
    return render(request, 'profile.html')