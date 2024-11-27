# image_processing_app/views_file.py
import logging
import os
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse
from django.contrib import messages
from django.conf import settings
from .models import VideoQualityMetrics
from pathlib import Path
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from urllib.parse import urlencode
from django.urls import reverse

logger = logging.getLogger(__name__)

def archive(request):
    logger.info("Starting archive view")

    # Get sorting parameters from the request
    sort_by = request.GET.get('sort_by', 'upload_date')
    sort_order = request.GET.get('sort_order', 'desc')
    per_page = request.GET.get('per_page', 25)
    page = request.GET.get('page', 1)
    query = request.GET.get('query', '')

    logger.info(f"Received query parameters: sort_by={sort_by}, sort_order={sort_order}, per_page={per_page}, page={page}, query={query}")

    # Determine the sorting order
    if sort_order == 'asc':
        order_by = sort_by
    else:
        order_by = f'-{sort_by}'

    # Filter metrics based on the search query
    metrics_list = VideoQualityMetrics.objects.filter(
        Q(name__icontains=query) |
        Q(doc_headline__icontains=query) |
        Q(source_url__icontains=query) |
        Q(blockiness__icontains=query) |
        Q(sa__icontains=query) |
        Q(letterbox__icontains=query) |
        Q(pillarbox__icontains=query) |
        Q(blockloss__icontains=query) |
        Q(blur__icontains=query) |
        Q(ta__icontains=query) |
        Q(blackout__icontains=query) |
        Q(freezing__icontains=query) |
        Q(exposure_bri__icontains=query) |
        Q(contrast__icontains=query) |
        Q(interlace__icontains=query) |
        Q(noise__icontains=query) |
        Q(slice__icontains=query) |
        Q(flickering__icontains=query) |
        Q(colourfulness__icontains=query)
    ).order_by(order_by)

    logger.info(f"Filtered metrics count: {metrics_list.count()}")

    # Paginate the metrics
    paginator = Paginator(metrics_list, per_page)
    metrics = paginator.get_page(page)

    logger.info(f"Paginated metrics: {metrics}")

    return render(request, 'archive.html', {
        'metrics': metrics,
        'paginator': paginator,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'per_page': per_page,
        'query': query,
    })

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

    if not file_path.exists():
        logger.info(f"File not found: {file_path}. Creating new results file.")
        # Ensure the results directory exists
        results_dir = Path(settings.MEDIA_ROOT) / 'results'
        results_dir.mkdir(parents=True, exist_ok=True)

        # Get the metrics for the image
        metric = get_object_or_404(VideoQualityMetrics, name=image_name)
        # Create a DataFrame with the metrics
        data = {
            "Frame": [metric.frame],
            "Blockiness": [metric.blockiness],
            "SA": [metric.sa],
            "Letterbox": [metric.letterbox],
            "Pillarbox": [metric.pillarbox],
            "Blockloss": [metric.blockloss],
            "Blur": [metric.blur],
            "TA": [metric.ta],
            "Blackout": [metric.blackout],
            "Freezing": [metric.freezing],
            "Exposure(bri)": [metric.exposure_bri],
            "Contrast": [metric.contrast],
            "Interlace": [metric.interlace],
            "Noise": [metric.noise],
            "Slice": [metric.slice],
            "Flickering": [metric.flickering],
            "Colourfulness": [metric.colourfulness]
        }
        df = pd.DataFrame(data)
        # Save the DataFrame to a CSV file
        df.to_csv(file_path, index=False)
        logger.info(f"Results file created: {file_path}")

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

        # Get the current state parameters
        per_page = request.POST.get('per_page', '25')
        sort_by = request.POST.get('sort_by', 'upload_date')
        query = request.POST.get('query', '')
        page = request.POST.get('page', '1')

        # Redirect to the profile page with the current state parameters
        query_params = urlencode({
            'per_page': per_page,
            'sort_by': sort_by,
            'query': query,
            'page': page
        })
        return redirect(f"{reverse('profile')}?{query_params}")
    return render(request, 'profile.html')