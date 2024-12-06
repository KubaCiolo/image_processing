from django.test import TestCase
from django.contrib.auth.models import User
from image_processing_app.forms import CustomUserCreationForm, EmailAuthenticationForm, UploadImageForm
from django.core.files.uploadedfile import SimpleUploadedFile

class CustomUserCreationFormTest(TestCase):
    def test_form_valid(self):
        form_data = {
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_password_in_use(self):
        # Create a user with the same password
        User.objects.create_user(username='user1', email='user1@example.com', password='testpassword123')
        form_data = {
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('This password is already in use. Please choose a different password.', form.errors['password1'])

class EmailAuthenticationFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test@example.com', email='test@example.com', password='testpassword123')

    def test_form_valid(self):
        form_data = {
            'username': 'test@example.com',
            'password': 'testpassword123'
        }
        form = EmailAuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid())

class UploadImageFormTest(TestCase):
    def test_form_valid_with_image(self):
        form_data = {}
        # Provide valid image content
        image_content = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff'
            b'\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        file_data = {'image': SimpleUploadedFile('test_image.gif', image_content, content_type='image/gif')}
        form = UploadImageForm(data=form_data, files=file_data)
        print("Form errors:", form.errors)
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_image(self):
        form_data = {}
        form = UploadImageForm(data=form_data)
        self.assertFalse(form.is_valid())