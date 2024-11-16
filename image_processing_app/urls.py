# image_processing_app/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import index, archive, download_csv, delete_metric

urlpatterns = [
    path('', index, name='index'),
    path('archive/', archive, name='archive'),
    path('download_csv/<str:filename>/', download_csv, name='download_csv'),
    path('delete_metric/<int:metric_id>/', delete_metric, name='delete_metric'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)