from django.shortcuts import render
from .models import VQI

def vqi_list(request):
    vqis = VQI.objects.all()
    return render(request, 'vqi_list.html', {'vqis': vqis})