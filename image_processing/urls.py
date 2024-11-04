# image_processing/urls.py
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('image_processing_app.urls')),
    path('accounts/', include('allauth.urls')),  # Add this line
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)