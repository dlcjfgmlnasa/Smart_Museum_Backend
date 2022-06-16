# Generated by Django 4.0.5 on 2022-06-16 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('museum', '0003_remove_innerexhibition_beacon'),
        ('beacon', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='beacon',
            options={'ordering': ['pk']},
        ),
        migrations.AddField(
            model_name='beacon',
            name='inner_exhibition',
            field=models.ForeignKey(db_column='INNER_EXHIBITION_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='museum.innerexhibition'),
        ),
        migrations.AlterField(
            model_name='beacon',
            name='recent_reception',
            field=models.DateTimeField(db_column='REACT_RECEPTION', null=True),
        ),
        migrations.AlterModelTable(
            name='beacon',
            table='SM_BEACON',
        ),
    ]
