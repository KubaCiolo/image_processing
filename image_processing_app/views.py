# image_processing_app/views.py
from django.shortcuts import render
from .models import VideoQualityMetrics
from .forms import SearchForm

def index(request):
    form = SearchForm()
    metrics = []
    if request.method == 'GET' and 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            metrics = VideoQualityMetrics.objects.filter(vqis_filename__icontains=query)
    return render(request, 'index.html', {'form': form, 'metrics': metrics})

def archive(request):
    metrics = VideoQualityMetrics.objects.all()
    return render(request, 'archive.html', {'metrics': metrics})