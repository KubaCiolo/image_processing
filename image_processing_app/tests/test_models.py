# image_processing_app/tests/test_models.py
from django.test import TestCase
from django.contrib.auth.models import User
from image_processing_app.models import VideoQualityMetrics

class VideoQualityMetricsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_video_quality_metrics(self):
        metric = VideoQualityMetrics.objects.create(
            user=self.user,
            image='test_image.jpg',
            name='test_image.jpg',
            frame=1,
            blockiness=0.1,
            sa=0.2,
            letterbox=0.3,
            pillarbox=0.4,
            blockloss=0.5,
            blur=0.6,
            ta=0.7,
            blackout=0.8,
            freezing=0.9,
            exposure_bri=1.0,
            contrast=1.1,
            interlace=1.2,
            noise=1.3,
            slice=1.4,
            flickering=1.5,
            colourfulness=1.6
        )
        self.assertEqual(metric.user, self.user)
        self.assertEqual(metric.image, 'test_image.jpg')
        self.assertEqual(metric.name, 'test_image.jpg')
        self.assertEqual(metric.frame, 1)
        self.assertEqual(metric.blockiness, 0.1)
        self.assertEqual(metric.sa, 0.2)
        self.assertEqual(metric.letterbox, 0.3)
        self.assertEqual(metric.pillarbox, 0.4)
        self.assertEqual(metric.blockloss, 0.5)
        self.assertEqual(metric.blur, 0.6)
        self.assertEqual(metric.ta, 0.7)
        self.assertEqual(metric.blackout, 0.8)
        self.assertEqual(metric.freezing, 0.9)
        self.assertEqual(metric.exposure_bri, 1.0)
        self.assertEqual(metric.contrast, 1.1)
        self.assertEqual(metric.interlace, 1.2)
        self.assertEqual(metric.noise, 1.3)
        self.assertEqual(metric.slice, 1.4)
        self.assertEqual(metric.flickering, 1.5)
        self.assertEqual(metric.colourfulness, 1.6)