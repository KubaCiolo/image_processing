# image_processing_app/views.py
# image_processing_app/views.py
import os
import logging
import requests
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.contrib import messages
from django.conf import settings
from .forms import UploadImageForm
from .models import VideoQualityMetrics
from pathlib import Path
from .utils.image_processing import process_image  # Import the process_image function
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile, File
from datetime import datetime
from django.utils.text import get_valid_filename
from urllib.parse import urlparse, unquote

logger = logging.getLogger(__name__)

@login_required
def index(request):
    logger.info("Starting index view")
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('image')
            image_url = form.cleaned_data.get('image_url')
            source_url = form.cleaned_data.get('source_url', '')

            # Define the path to save the uploaded image
            today = datetime.today()
            upload_dir = Path(settings.MEDIA_ROOT) / 'uploads' / today.strftime('%Y/%m/%d')
            upload_dir.mkdir(parents=True, exist_ok=True)

            if image_url:
                # Download the image from the URL
                response = requests.get(image_url)
                if response.status_code == 200:
                    # Extract the file name and extension from the URL
                    parsed_url = urlparse(image_url)
                    original_name = get_valid_filename(unquote(Path(parsed_url.path).name))
                    if not original_name:
                        messages.error(request, "Failed to extract file name from URL")
                        return redirect('index')
                    image_path = upload_dir / original_name
                    logger.info(f"Saving downloaded image to {image_path}")
                    with open(image_path, 'wb') as f:
                        f.write(response.content)
                else:
                    messages.error(request, "Failed to download image from URL")
                    return redirect('index')
            else:
                # Save the uploaded image to the defined path
                original_name = get_valid_filename(image.name)
                image_path = upload_dir / original_name
                logger.info(f"Saving uploaded image to {image_path}")
                with open(image_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)

            # Process the image using agh_vqis
            try:
                output_csv_path = process_image(image_path)
                download_link = f"/download_csv/{output_csv_path.name}"
                messages.success(request, mark_safe(f"Image processed successfully. <a href='{download_link}'>Download the results here</a>."))

                # Parse the CSV file and extract metrics
                metrics = {}
                with open(output_csv_path, newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        metrics = row
                        break  # Assuming only one row of metrics

                # Save the metrics to the database
                with open(image_path, 'rb') as img_file:
                    VideoQualityMetrics.objects.create(
                        user=request.user,
                        image=File(img_file, name=image_path.name),
                        name=original_name,
                        source_url=source_url if source_url else None,
                        frame=int(metrics.get('Frame', 0)),
                        blockiness=float(metrics.get('Blockiness', 0.0)),
                        sa=float(metrics.get('SA', 0.0)),
                        letterbox=float(metrics.get('Letterbox', 0.0)),
                        pillarbox=float(metrics.get('Pillarbox', 0.0)),
                        blockloss=float(metrics.get('Blockloss', 0.0)),
                        blur=float(metrics.get('Blur', 0.0)),
                        ta=float(metrics.get('TA', 0.0)),
                        blackout=float(metrics.get('Blackout', 0.0)),
                        freezing=float(metrics.get('Freezing', 0.0)),
                        exposure_bri=float(metrics.get('Exposure(bri)', 0.0)),
                        contrast=float(metrics.get('Contrast', 0.0)),
                        interlace=float(metrics.get('Interlace', 0.0)),
                        noise=float(metrics.get('Noise', 0.0)),
                        slice=float(metrics.get('Slice', 0.0)),
                        flickering=float(metrics.get('Flickering', 0.0)),
                        colourfulness=float(metrics.get('Colourfulness', 0.0))
                    )

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
        return redirect('archive')
    return render(request, 'archive.html')