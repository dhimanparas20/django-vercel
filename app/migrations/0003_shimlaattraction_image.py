# Generated by Django 5.1.3 on 2024-11-29 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_shimlaattraction_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='shimlaattraction',
            name='image',
            field=models.URLField(default='https://image.com'),
        ),
    ]
