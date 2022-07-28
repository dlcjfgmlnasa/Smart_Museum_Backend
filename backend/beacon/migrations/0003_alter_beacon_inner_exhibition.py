# Generated by Django 4.0.5 on 2022-07-28 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('museum', '0002_innerexhibition_x_coordinate_and_more'),
        ('beacon', '0002_remove_log_beacon_delete_daylog_delete_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beacon',
            name='inner_exhibition',
            field=models.ForeignKey(db_column='INNER_EXHIBITION_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='beacon', to='museum.innerexhibition'),
        ),
    ]
