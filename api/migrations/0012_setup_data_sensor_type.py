from django.db import migrations


def forwards_func(apps, schema_editor):
    SensorType = apps.get_model("api", "SensorType")
    db_alias = schema_editor.connection.alias
    SensorType.objects.using(db_alias).bulk_create([
        SensorType(sensor_type_id="humidity",
                   sensor_type_name_eng="humidity",
                   sensor_type_name_por="humidade",
                   sensor_type_unit="ml")  # TODO - acertar unidade
    ])


def reverse_func(apps, schema_editor):
    # SensorType = apps.get_model("api", "SensorType")
    # db_alias = schema_editor.connection.alias
    # SensorType.objects.using(db_alias).filter(sensor_type_id="humidity").delete()

    # Na verdade, remover isto pode ser mau, pq faz cascade a todos os sensores
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0011_auto_20180121_2219')
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
