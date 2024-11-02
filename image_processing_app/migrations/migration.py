# image_processing_app/migrations/0002_auto_<timestamp>.py
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('image_processing_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoqualitymetrics',
            name='vqis_filename',
            field=models.CharField(max_length=255, unique=True, default='default_vqis_filename'),
        ),
    ]