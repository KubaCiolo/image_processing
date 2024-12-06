# image_processing_app/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views_profile import profile, edit_profile, logout_confirmation, login, signup, CustomConfirmEmailView
from .views_image import index
from .views_file import archive, download_csv, download_from_archive, delete_metric
from .views_profile import delete_account

urlpatterns = [
    path('', index, name='index'),
    path('archive/', archive, name='archive'),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('download_csv/<str:filename>/', download_csv, name='download_csv'),
    path('download_from_archive/<str:image_name>/', download_from_archive, name='download_from_archive'),
    path('delete_metric/<int:metric_id>/', delete_metric, name='delete_metric'),
    path('accounts/logout/', logout_confirmation, name='logout_confirmation'),
    path('accounts/login/', login, name='login'),
    path('accounts/signup/', signup, name='account_signup'),
    path('accounts/confirm-email/<str:key>/', CustomConfirmEmailView.as_view(), name='account_confirm_email'),
    path('accounts/delete/', delete_account, name='delete_account'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)