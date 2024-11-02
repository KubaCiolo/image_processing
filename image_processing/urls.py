# image_processing/urls.py
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from image_processing_app.views import home  # Correct import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('image_processing_app.urls')),
    path('accounts/', include('allauth.urls')),  # Include allauth URLs for authentication
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)