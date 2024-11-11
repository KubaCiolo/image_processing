# image_processing_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('archive/', views.archive, name='archive'),
    path('download_csv/<str:filename>/', views.download_csv, name='download_csv'),
]