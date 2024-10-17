from django.db import models
from django.utils import timezone

class PDF(models.Model):
    name = models.CharField(max_length=255)
    source_link = models.URLField()

class Image(models.Model):
    title = models.CharField(max_length=255, default='Untitled')  # Provide a default title
    image = models.ImageField(upload_to='images/', default='images/default.jpg')  # Provide a default image path
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp when the object is created

    def __str__(self):
        return self.title

class Indicator(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    indicator_data = models.TextField()

class VQI(models.Model):
    frame = models.IntegerField()
    blockiness = models.FloatField()
    sa = models.FloatField()
    letterbox = models.FloatField()
    pillarbox = models.FloatField()
    blockloss = models.FloatField()
    blur = models.FloatField()
    ta = models.FloatField()
    blackout = models.IntegerField()
    freezing = models.IntegerField()
    exposure_bri = models.FloatField()
    contrast = models.FloatField()
    interlace = models.FloatField()
    noise = models.FloatField()
    slice = models.FloatField()
    flickering = models.FloatField()

    def __str__(self):
        return f"Frame {self.frame}"