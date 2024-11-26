# image_processing_app/tests/test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from image_processing_app.models import VideoQualityMetrics

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_index_view_get(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_profile_view_get(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_edit_profile_view_get(self):
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')

    def test_archive_view_get(self):
        response = self.client.get(reverse('archive'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'archive.html')

    def test_delete_metric_view_post(self):
        metric = VideoQualityMetrics.objects.create(
            user=self.user,
            image='test_image.jpg',
            name='test_image.jpg'
        )
        response = self.client.post(reverse('delete_metric', args=[metric.id]))
        self.assertRedirects(response, reverse('profile'))
        self.assertFalse(VideoQualityMetrics.objects.filter(id=metric.id).exists())