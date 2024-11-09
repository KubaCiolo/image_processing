from django.shortcuts import render
from django.conf import settings
from .forms import UploadImageForm
from .models import UploadedImage
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def index(request):
    logger.info("Starting index view")
    form = UploadImageForm()
    return render(request, 'index.html', {'form': form})

def archive(request):
    logger.info("Starting archive view")
    metrics = UploadedImage.objects.all()
    return render(request, 'archive.html', {'metrics': metrics})

def home(request):
    logger.info("Starting home view")
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            image = uploaded_image.image
            
            # Define the path to save the uploaded image
            image_path = Path(settings.MEDIA_ROOT) / image.name
            
            # Ensure the uploads directory exists
            if not image_path.parent.exists():
                image_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save the uploaded image to the defined path
            logger.info(f"Uploading image to {image_path}")
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            
            # Verify that the image is saved correctly
            if image_path.exists():
                logger.info(f"Image successfully uploaded to {image_path}")
                return render(request, 'index.html', {'form': form, 'message': 'Image uploaded successfully'})
            else:
                logger.error(f"Failed to upload image to {image_path}")
                return render(request, 'index.html', {'form': form, 'message': 'Failed to upload image'})
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
            image = uploaded_image.image
            
            # Define the path to save the uploaded image
            image_path = Path(settings.MEDIA_ROOT) / image.name
            
            # Ensure the uploads directory exists
            if not image_path.parent.exists():
                image_path.parent.mkdir(parents=True, exist_ok=True)
                
            # Save the uploaded image to the defined path
            logger.info(f"Uploading image to {image_path}")
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
           
            # Verify that the image is saved correctly
            if image_path.exists():
                logger.info(f"Image successfully uploaded to {image_path}")
                return render(request, 'upload_image.html', {'form': form, 'message': 'Image uploaded successfully'})
            else:
                logger.error(f"Failed to upload image to {image_path}")
                return render(request, 'upload_image.html', {'form': form, 'message': 'Failed to upload image'})
        else:
            logger.error("Form is not valid")
    else:
        form = UploadImageForm()
    return render(request, 'upload_image.html', {'form': form})