# Generated by Django 4.0.5 on 2022-12-23 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0009_alter_footprintlog_exhibition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='mac_address',
            field=models.CharField(db_column='MAC_ADDRESS', max_length=100),
        ),
    ]
