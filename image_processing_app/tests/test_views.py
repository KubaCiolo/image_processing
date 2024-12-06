from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from image_processing_app.models import VideoQualityMetrics

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')


    def test_signup_view_get(self):
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/custom_signup.html')

    def test_signup_view_post(self):
        form_data = {
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        response = self.client.post(reverse('account_signup'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful signup

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/custom_login.html')

    def test_login_view_post(self):
        form_data = {
            'username': 'testuser@example.com',  # Use email if your login form uses email
            'password': 'testpassword'
        }
        response = self.client.post(reverse('login'), data=form_data)
        print("Login response content:", response.content)  # Debugging line
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_edit_profile_view_get(self):
        self.client.login(username='testuser', password='testpassword')  # Ensure the user is logged in
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_view_get(self):
        self.client.login(username='testuser', password='testpassword')  # Ensure the user is logged in
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_delete_metric_view_post(self):
        metric = VideoQualityMetrics.objects.create(
            user=self.user,
            image='test_image.jpg',
            name='test_image.jpg',
            frame=1,
            blockiness=0.0,
            sa=0.0,
            letterbox=0.0,
            pillarbox=0.0,
            blockloss=0.0,
            blur=0.0,
            ta=0.0,
            blackout=0.0,
            freezing=0.0,
            exposure_bri=0.0,
            contrast=0.0,
            interlace=0.0,
            noise=0.0,
            slice=0.0,
            flickering=0.0,
            colourfulness=0.0,
            upload_date='2024-12-06 15:25:43.446849+00'
        )
        self.client.login(username='testuser', password='testpassword')  # Ensure the user is logged in
        response = self.client.post(reverse('delete_metric', args=[metric.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(VideoQualityMetrics.objects.filter(id=metric.id).exists())