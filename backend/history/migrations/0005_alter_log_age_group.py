# Generated by Django 4.0.5 on 2022-07-29 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0004_daylog_footprint_log_mac_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='age_group',
            field=models.CharField(choices=[(1, '10'), (2, '20'), (3, '30'), (4, '40'), (5, '50'), (6, '50 >= ')], db_column='AGE_GROUP', max_length=25),
        ),
    ]
