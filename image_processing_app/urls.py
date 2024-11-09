# image_processing_app/urls.py
from django.urls import path
from .views import index, archive, home, upload_image

urlpatterns = [
    path('', index, name='index'),
    path('archive/', archive, name='archive'),
    path('home/', home, name='home'),
    path('upload/', upload_image, name='upload_image'),
]