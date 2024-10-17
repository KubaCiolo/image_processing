from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # URL for the Django admin interface
    path('', include('image_processing_app.urls')),  # Include URLs from the image_processing_app
]