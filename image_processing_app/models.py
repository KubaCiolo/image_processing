from django.db import models
from django.conf import settings

class VideoQualityMetrics(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    name = models.CharField(max_length=255, unique=True)  # Add unique constraint
    source_url = models.URLField(blank=True, null=True)
    doc_headline = models.CharField(max_length=1024, blank=True, null=True)  # Extended length
    upload_date = models.DateTimeField(auto_now_add=True)
    frame = models.IntegerField()
    blockiness = models.FloatField()
    sa = models.FloatField()
    letterbox = models.FloatField()
    pillarbox = models.FloatField()
    blockloss = models.FloatField()
    blur = models.FloatField()
    ta = models.FloatField()
    blackout = models.FloatField()
    freezing = models.FloatField()
    exposure_bri = models.FloatField()
    contrast = models.FloatField()
    interlace = models.FloatField()
    noise = models.FloatField()
    slice = models.FloatField()
    flickering = models.FloatField()
    colourfulness = models.FloatField()

    def __str__(self):
        return self.name