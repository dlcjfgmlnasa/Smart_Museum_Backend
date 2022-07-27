# Generated by Django 4.0.5 on 2022-07-27 05:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('museum', '0002_innerexhibition_x_coordinate_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Beacon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('int_dt', models.DateTimeField(auto_now_add=True, db_column='INS_DT')),
                ('upt_dt', models.DateTimeField(auto_now=True, db_column='UPD_DT')),
                ('uuid', models.CharField(db_column='UUID', max_length=100)),
                ('recent_reception', models.DateTimeField(db_column='RECENT_RECEPTION', null=True)),
                ('inner_exhibition', models.ForeignKey(db_column='INNER_EXHIBITION_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='museum.innerexhibition')),
            ],
            options={
                'db_table': 'SM_BEACON',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('int_dt', models.DateTimeField(auto_now_add=True, db_column='INS_DT')),
                ('upt_dt', models.DateTimeField(auto_now=True, db_column='UPD_DT')),
                ('sex', models.CharField(choices=[(1, 'MALE'), (2, 'FEMALE')], db_column='SEX', max_length=25)),
                ('age_group', models.CharField(choices=[(1, '10'), (2, '20'), (3, '30'), (4, '40'), (5, '50')], db_column='AGE_GROUP', max_length=25)),
                ('beacon', models.ForeignKey(db_column='BEACON_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='beacon.beacon')),
            ],
            options={
                'db_table': 'SM_LOG',
                'ordering': ['pk'],
            },
        ),
    ]
