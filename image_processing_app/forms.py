# image_processing/image_processing_app/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user