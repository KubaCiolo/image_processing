# image_processing_app/urls.py

from django.urls import path
from .views import index, archive, home

urlpatterns = [
    path('', index, name='index'),
    path('archive/', archive, name='archive'),
    path('home/', home, name='home'),  # Adjusted path for home view
]