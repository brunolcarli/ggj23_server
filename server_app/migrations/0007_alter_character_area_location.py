# Generated by Django 3.2.6 on 2023-02-11 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server_app', '0006_spawnedenemy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='area_location',
            field=models.CharField(default='citadel_central_area', max_length=25),
        ),
    ]
