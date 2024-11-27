# image_processing/image_processing_app/forms.py
from django import forms

class UploadImageForm(forms.Form):
    image = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get("image")

        if not image:
            raise forms.ValidationError("You must provide an image file.")
        return cleaned_data

class SearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=False)