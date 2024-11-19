# image_processing/image_processing_app/forms.py

# image_processing_app/forms.py
from django import forms

class UploadImageForm(forms.Form):
    image = forms.ImageField(required=False)
    image_url = forms.URLField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get("image")
        image_url = cleaned_data.get("image_url")

        if not image and not image_url:
            raise forms.ValidationError("You must provide either an image file or an image URL.")
        return cleaned_data
    
class SearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=False)