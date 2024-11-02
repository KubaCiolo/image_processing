# image_processing_app/urls.py
from django.urls import path
from .views import index, archive

urlpatterns = [
    path('', index, name='index'),
    path('archive/', archive, name='archive'),
]