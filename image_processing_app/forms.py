# image_processing/image_processing_app/forms.py

from django import forms

class UploadImageForm(forms.Form):
    image = forms.ImageField()
    
class SearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=False)