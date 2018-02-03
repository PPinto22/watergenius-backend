from django.db import migrations


def forwards_func(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    DayPlan = apps.get_model("api", "DayPlan")
    plans = DayPlan.objects.using(db_alias).filter(dayplan_water_qty_unit='mm')
    for plan in plans:
        sub_area = plan.dayplan_sub.sub_area
        plan.dayplan_water_qty_unit = 'L'
        plan.dayplan_water_qty = plan.dayplan_water_qty * sub_area
        plan.save()

    IrrigationTime = apps.get_model("api", "IrrigationTime")
    irrigations = IrrigationTime.objects.using(db_alias).filter(irrigation_time_qty_unit='mm')
    for irr in irrigations:
        sub_area = irr.irrigation_time_sub.sub_area
        irr.irrigation_time_qty_unit = 'L'
        irr.irrigation_time_qty = irr.irrigation_time_qty * sub_area
        irr.save()


def reverse_func(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    DayPlan = apps.get_model("api", "DayPlan")
    plans = DayPlan.objects.using(db_alias).filter(dayplan_water_qty_unit='L')
    for plan in plans:
        sub_area = plan.dayplan_sub.sub_area
        plan.dayplan_water_qty_unit = 'mm'
        plan.dayplan_water_qty = plan.dayplan_water_qty / sub_area
        plan.save()

    IrrigationTime = apps.get_model("api", "IrrigationTime")
    irrigations = IrrigationTime.objects.using(db_alias).filter(irrigation_time_qty_unit='L')
    for irr in irrigations:
        sub_area = irr.irrigation_time_sub.sub_area
        irr.irrigation_time_qty_unit = 'mm'
        irr.irrigation_time_qty = irr.irrigation_time_qty / sub_area
        irr.save()


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0024_auto_20180203_2206')
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
