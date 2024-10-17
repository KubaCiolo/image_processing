from django.contrib import admin
from .models import VQI

@admin.register(VQI)
class VQIAdmin(admin.ModelAdmin):
    list_display = ('frame', 'blockiness', 'sa', 'letterbox', 'pillarbox', 'blockloss', 'blur', 'ta', 'blackout', 'freezing', 'exposure_bri', 'contrast', 'interlace', 'noise', 'slice', 'flickering')
    search_fields = ('frame', 'blockiness', 'sa')

# Alternatively, you can use:
# admin.site.register(VQI, VQIAdmin)