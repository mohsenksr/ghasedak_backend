# Generated by Django 4.0.6 on 2023-08-21 07:38

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0003_alter_membership_unique_together_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('channel_administration', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='channeladmin',
            unique_together={('admin', 'channel')},
        ),
    ]
