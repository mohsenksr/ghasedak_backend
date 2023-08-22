# Generated by Django 4.0.6 on 2023-08-21 13:17

from django.db import migrations, models
import ghasedak.storage_backends.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0005_alter_content_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='summary',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='video',
            field=models.FileField(blank=True, null=True, storage=ghasedak.storage_backends.media_storage.MediaStorage(location='media/posts/video'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='content',
            name='voice',
            field=models.FileField(blank=True, null=True, storage=ghasedak.storage_backends.media_storage.MediaStorage(location='media/posts/voice'), upload_to=''),
        ),
    ]