# Generated by Django 4.2.4 on 2023-09-04 15:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0004_venue_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='attendees',
            field=models.ManyToManyField(blank=True, null=True, related_name='attendees', to=settings.AUTH_USER_MODEL),
        ),
    ]