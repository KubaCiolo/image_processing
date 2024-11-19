# image_processing_app/views_profile.py
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from allauth.account.forms import ChangePasswordForm, AddEmailForm
from .models import VideoQualityMetrics

logger = logging.getLogger(__name__)

@login_required
def profile(request):
    logger.info("Starting profile view")
    user_metrics = VideoQualityMetrics.objects.filter(user=request.user)
    return render(request, 'profile.html', {
        'user_metrics': user_metrics
    })

@login_required
def edit_profile(request):
    logger.info("Starting edit profile view")
    password_form = ChangePasswordForm(request.user)
    email_form = AddEmailForm()
    if request.method == 'POST':
        if 'password' in request.POST:
            password_form = ChangePasswordForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, "Password changed successfully")
                return redirect('profile')
        elif 'email' in request.POST:
            email_form = AddEmailForm(request.POST)
            if email_form.is_valid():
                email_form.save()
                messages.success(request, "Email added successfully")
                return redirect('profile')
    return render(request, 'edit_profile.html', {
        'password_form': password_form,
        'email_form': email_form
    })