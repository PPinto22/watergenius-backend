# Generated by Django 2.0 on 2018-02-03 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_auto_20180131_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayplan',
            name='dayplan_water_qty_unit',
            field=models.CharField(default='L', max_length=6),
        ),
        migrations.AlterField(
            model_name='irrigationtime',
            name='irrigation_time_qty_unit',
            field=models.CharField(default='L', max_length=10),
        ),
    ]
