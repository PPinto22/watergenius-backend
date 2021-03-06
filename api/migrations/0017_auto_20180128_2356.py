# Generated by Django 2.0 on 2018-01-28 23:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_change_humidity_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='centralnode',
            name='node_ip',
            field=models.GenericIPAddressField(default='0.0.0.0'),
        ),
        migrations.AlterField(
            model_name='read',
            name='read_timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='sensor_timerate',
            field=models.IntegerField(default=30),
        ),
    ]
