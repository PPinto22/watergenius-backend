# Generated by Django 2.0 on 2018-01-11 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20180111_1058'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sensor',
            old_name='sensor_sub',
            new_name='sensor_esys',
        ),
    ]
