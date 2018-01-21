# Generated by Django 2.0 on 2018-01-21 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20180121_2015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='read',
            name='read_type',
        ),
        migrations.RemoveField(
            model_name='sensortype',
            name='sensor_type_name',
        ),
        migrations.AddField(
            model_name='sensortype',
            name='sensor_type_name_eng',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='sensortype',
            name='sensor_type_name_por',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='sensortype',
            name='sensor_type_unit',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='sensor_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='sensortype',
            name='sensor_type_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name='ReadType',
        ),
    ]
