# image_processing_app/views_profile.py
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from allauth.account.forms import ChangePasswordForm, AddEmailForm
from .models import VideoQualityMetrics
from django.core.paginator import Paginator
from django.db.models import Q

logger = logging.getLogger(__name__)

@login_required
def profile(request):
    logger.info("Starting profile view")

    # Get sorting parameters from the request
    sort_by = request.GET.get('sort_by', 'upload_date')
    sort_order = request.GET.get('sort_order', 'desc')
    per_page = request.GET.get('per_page', 25)
    page = request.GET.get('page', 1)
    query = request.GET.get('query', '')

    logger.info(f"Received query parameters: sort_by={sort_by}, sort_order={sort_order}, per_page={per_page}, page={page}, query={query}")

    # Determine the sorting order
    if sort_order == 'asc':
        order_by = sort_by
    else:
        order_by = f'-{sort_by}'

    # Filter metrics based on the search query and user
    user_metrics_list = VideoQualityMetrics.objects.filter(
        Q(name__icontains=query) |
        Q(doc_headline__icontains=query) |
        Q(source_url__icontains=query) |
        Q(blockiness__icontains=query) |
        Q(sa__icontains=query) |
        Q(letterbox__icontains=query) |
        Q(pillarbox__icontains=query) |
        Q(blockloss__icontains=query) |
        Q(blur__icontains=query) |
        Q(ta__icontains=query) |
        Q(blackout__icontains=query) |
        Q(freezing__icontains=query) |
        Q(exposure_bri__icontains=query) |
        Q(contrast__icontains=query) |
        Q(interlace__icontains=query) |
        Q(noise__icontains=query) |
        Q(slice__icontains=query) |
        Q(flickering__icontains=query) |
        Q(colourfulness__icontains=query),
        user=request.user
    ).order_by(order_by)

    logger.info(f"Filtered user metrics count: {user_metrics_list.count()}")

    # Paginate the metrics
    paginator = Paginator(user_metrics_list, per_page)
    user_metrics = paginator.get_page(page)

    logger.info(f"Paginated user metrics: {user_metrics}")

    return render(request, 'profile.html', {
        'user_metrics': user_metrics,
        'paginator': paginator,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'per_page': per_page,
        'query': query,
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