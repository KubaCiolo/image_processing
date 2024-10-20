# image_processing_app/models.py
from django.db import models

class VideoQualityMetrics(models.Model):
    vqis_filename = models.CharField(max_length=255, unique=True, default='default_vqis_filename')
    doc_filename = models.CharField(max_length=255, default='default_doc_filename')
    doc_headline = models.TextField(default='default_doc_headline')
    doc_url = models.URLField(default='http://example.com')
    frame = models.IntegerField(default=0)
    blockiness = models.FloatField(default=0.0)
    sa = models.FloatField(default=0.0)
    letterbox = models.FloatField(default=0.0)
    pillarbox = models.FloatField(default=0.0)
    blockloss = models.FloatField(default=0.0)
    blur = models.FloatField(default=0.0)
    ta = models.FloatField(default=0.0)
    blackout = models.IntegerField(default=0)
    freezing = models.IntegerField(default=0)
    exposure_bri = models.FloatField(db_column='Exposure(bri)', default=0.0)  # Use db_column to match the exact column name
    contrast = models.FloatField(default=0.0)
    interlace = models.FloatField(default=0.0)
    noise = models.FloatField(default=0.0)
    slice = models.FloatField(default=0.0)
    flickering = models.FloatField(default=0.0)
    colourfulness = models.FloatField(default=0.0)

    def __str__(self):
        return f"Frame {self.frame}"