# Generated by Django 5.0.6 on 2024-05-10 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_blogentrycomment_tripcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='currentTrip',
            field=models.BooleanField(default=False),
        ),
    ]
