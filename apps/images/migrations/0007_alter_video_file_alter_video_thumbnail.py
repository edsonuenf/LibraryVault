# Generated by Django 5.1.7 on 2025-04-22 23:22

import apps.images.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0006_like_delete_imagegridconfig'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='file',
            field=models.FileField(upload_to=apps.images.models.Video.video_upload_to),
        ),
        migrations.AlterField(
            model_name='video',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=apps.images.models.Video.thumb_upload_to),
        ),
    ]
