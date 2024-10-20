# image_processing_app/forms.py
from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=255)