# Generated by Django 4.0.6 on 2023-08-18 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
