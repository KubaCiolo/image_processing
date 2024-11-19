# image_processing_app/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views_profile import profile, edit_profile
from .views_image import index
from .views_file import archive, download_csv, download_from_archive, delete_metric

urlpatterns = [
    path('', index, name='index'),
    path('archive/', archive, name='archive'),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('download_csv/<str:filename>/', download_csv, name='download_csv'),
    path('download_from_archive/<str:image_name>/', download_from_archive, name='download_from_archive'),
    path('delete_metric/<int:metric_id>/', delete_metric, name='delete_metric'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)