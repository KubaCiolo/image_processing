# image_processing_app/tests/test_forms.py
from django.test import TestCase
from image_processing_app.forms import UploadImageForm

class UploadImageFormTest(TestCase):
    def test_form_valid_with_image(self):
        form_data = {}
        file_data = {'image': 'test_image.jpg'}
        form = UploadImageForm(data=form_data, files=file_data)
        self.assertTrue(form.is_valid())

    def test_form_valid_with_image_url(self):
        form_data = {'image_url': 'http://example.com/test_image.jpg'}
        form = UploadImageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_image_or_image_url(self):
        form_data = {}
        form = UploadImageForm(data=form_data)
        self.assertFalse(form.is_valid())