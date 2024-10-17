# Generated by Django 3.2.25 on 2024-10-15 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_processing_app', '0002_auto_20241015_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='VQI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frame', models.IntegerField()),
                ('blockiness', models.FloatField()),
                ('sa', models.FloatField()),
                ('letterbox', models.FloatField()),
                ('pillarbox', models.FloatField()),
                ('blockloss', models.FloatField()),
                ('blur', models.FloatField()),
                ('ta', models.FloatField()),
                ('blackout', models.IntegerField()),
                ('freezing', models.IntegerField()),
                ('exposure_bri', models.FloatField()),
                ('contrast', models.FloatField()),
                ('interlace', models.FloatField()),
                ('noise', models.FloatField()),
                ('slice', models.FloatField()),
                ('flickering', models.FloatField()),
            ],
        ),
    ]
