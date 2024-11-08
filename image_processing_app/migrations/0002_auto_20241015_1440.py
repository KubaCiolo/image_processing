# Generated by Django 3.2.25 on 2024-10-15 14:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('image_processing_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='file_path',
        ),
        migrations.RemoveField(
            model_name='image',
            name='pdf',
        ),
        migrations.AddField(
            model_name='image',
            name='image',
            field=models.ImageField(default='images/default.jpg', upload_to='images/'),
        ),
        migrations.AddField(
            model_name='image',
            name='title',
            field=models.CharField(default='Untitled', max_length=255),
        ),
        migrations.AddField(
            model_name='image',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 10, 15, 14, 40, 25, 123532, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
