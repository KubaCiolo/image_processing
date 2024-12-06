# image_processing_app/views_profile.py
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from allauth.account.forms import ChangePasswordForm, AddEmailForm
from django.contrib.auth.forms import AuthenticationForm
from allauth.account.models import EmailAddress, EmailConfirmationHMAC
from django.middleware.csrf import get_token
from allauth.account.views import ConfirmEmailView
from .forms import UserProfileForm , CustomUserCreationForm
from .models import VideoQualityMetrics
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404

logger = logging.getLogger(__name__)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'account/custom_login.html', {'form': form})

def signup(request):
    csrf_token = get_token(request)
    logger.info(f"CSRF Token: {csrf_token}")
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create email address record and send verification email
            email_address = EmailAddress.objects.create(user=user, email=user.email, primary=True)
            email_address.send_confirmation(request)
            messages.success(request, 'Please confirm your email address to complete the registration.')
            return redirect('account_login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/custom_signup.html', {'form': form, 'csrf_token': csrf_token})

class CustomConfirmEmailView(ConfirmEmailView):
    template_name = 'account/email_verification.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        email_confirmation = self.get_object()
        context['email'] = email_confirmation.email_address.email
        context['key'] = self.kwargs['key']
        context['csrf_token'] = get_token(self.request)
        return context

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        try:
            return EmailConfirmationHMAC.from_key(key)
        except EmailConfirmationHMAC.DoesNotExist:
            raise Http404("No email confirmation found for this key.")
    
@login_required
def logout_confirmation(request):
    if request.method == 'POST':
        auth_logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('index')
    return render(request, 'account/logout_confirmation.html')

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
    user = request.user
    password_form = ChangePasswordForm(user)
    email_form = AddEmailForm()
    user_form = UserProfileForm(instance=user)

    if request.method == 'POST':
        if 'change_password' in request.POST:
            password_form = ChangePasswordForm(user, request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, "Password changed successfully")
                return redirect('edit_profile')
        elif 'change_email' in request.POST:
            email_form = AddEmailForm(request.POST)
            if email_form.is_valid():
                email_form.save()
                messages.success(request, "Email added successfully")
                return redirect('edit_profile')
        elif 'update_profile' in request.POST:
            user_form = UserProfileForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "Profile updated successfully")
                return redirect('edit_profile')

    return render(request, 'edit_profile.html', {
        'password_form': password_form,
        'email_form': email_form,
        'user_form': user_form,
        'date_joined': user.date_joined,
        'last_login': user.last_login,
    })
    