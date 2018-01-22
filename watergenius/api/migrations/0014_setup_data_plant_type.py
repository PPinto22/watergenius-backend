from django.db import migrations


def forwards_func(apps, schema_editor):
    PlantType = apps.get_model("api", "PlantType")
    db_alias = schema_editor.connection.alias
    PlantType.objects.using(db_alias).bulk_create([
        PlantType(plant_type_id="grass",
                  plant_type_name_eng="grass",
                  plant_type_name_por="relva")
    ])


def reverse_func(apps, schema_editor):
    # PlantType = apps.get_model("api", "PlantType")
    # db_alias = schema_editor.connection.alias
    # PlantType.objects.using(db_alias).filter(plant_type_id="grass").delete()

    pass


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0013_auto_20180121_2352')
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
