# Generated by Django 4.0.5 on 2022-07-29 01:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('museum', '0002_innerexhibition_x_coordinate_and_more'),
        ('history', '0006_remove_daylog_footprint'),
    ]

    operations = [
        migrations.CreateModel(
            name='FootPrintLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('int_dt', models.DateTimeField(auto_now_add=True, db_column='INS_DT')),
                ('upt_dt', models.DateTimeField(auto_now=True, db_column='UPD_DT')),
                ('date', models.DateField(db_column='DATE')),
                ('foot_printing_count', models.JSONField(db_column='FOOT_PRINT_COUNT')),
                ('exhibition', models.ForeignKey(db_column='FOOT_PRINT_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='foot_print', to='museum.exhibition')),
            ],
            options={
                'db_table': 'SM_FOOT_PRINT_LOG',
                'ordering': ['pk'],
            },
        ),
    ]