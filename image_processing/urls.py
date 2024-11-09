# image_processing/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from image_processing_app.views import index, upload_image, archive

urlpatterns = [
    path('', index, name='index'),
    path('upload/', upload_image, name='upload_image'),
    path('archive/', archive, name='archive'),
    path('', include('image_processing_app.urls')),
    path('accounts/', include('allauth.urls')),  # Add this line
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)