# image_processing/image_processing_app/forms.py

from django import forms
from .models import UploadedImage

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']

class SearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=False)