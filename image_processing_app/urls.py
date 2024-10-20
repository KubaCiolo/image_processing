# image_processing_app/urls.py
from django.urls import path
from .views import index, archive, search_view

urlpatterns = [
    path('', index, name='index'),
    path('archive/', archive, name='archive'),
    path('search/', search_view, name='search'),
]