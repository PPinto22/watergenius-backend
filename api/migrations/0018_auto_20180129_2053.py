# Generated by Django 2.0 on 2018-01-29 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20180128_2356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='embeddedsystem',
            name='esys_state',
        ),
        migrations.AddField(
            model_name='embeddedsystem',
            name='esys_last_read',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
