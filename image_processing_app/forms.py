# image_processing/image_processing_app/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.hashers import check_password

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

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if User.objects.filter(password__isnull=False).exists():
            for user in User.objects.all():
                if check_password(password1, user.password):
                    raise forms.ValidationError("This password is already in use. Please choose a different password.")
        return password1

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'autofocus': True}))