# Generated by Django 5.0.6 on 2024-06-17 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_usersubscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
