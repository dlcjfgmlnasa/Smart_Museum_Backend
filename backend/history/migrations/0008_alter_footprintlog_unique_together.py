# Generated by Django 4.0.5 on 2022-07-29 01:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museum', '0002_innerexhibition_x_coordinate_and_more'),
        ('history', '0007_footprintlog'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='footprintlog',
            unique_together={('date', 'exhibition')},
        ),
    ]
