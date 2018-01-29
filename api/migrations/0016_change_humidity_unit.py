from django.db import migrations


def forwards_func(apps, schema_editor):
    SensorType = apps.get_model("api", "SensorType")
    db_alias = schema_editor.connection.alias
    humidity = SensorType.objects.using(db_alias).get(sensor_type_id="humidity")
    humidity.sensor_type_unit = "%"
    humidity.save()


def reverse_func(apps, schema_editor):
    SensorType = apps.get_model("api", "SensorType")
    db_alias = schema_editor.connection.alias
    humidity = SensorType.objects.using(db_alias).get(sensor_type_id="humidity")
    humidity.sensor_type_unit = "ml"
    humidity.save()
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0015_auto_20180124_1125')
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
