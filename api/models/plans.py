from django.db import models

from api.models.subspaces import SubSpace


class DayPlan(models.Model):
    dayplan_id = models.AutoField(primary_key=True)
    dayplan_gen_time = models.DateTimeField(auto_now=True)
    dayplan_time = models.DateTimeField()
    dayplan_water_qty = models.FloatField()
    dayplan_water_qty_unit = models.CharField(max_length=6, default='mm')
    dayplan_rain = models.FloatField(default=0.0)
    dayplan_rain_unit = models.CharField(max_length=6, default='mm')
    dayplan_sub = models.ForeignKey(SubSpace, related_name='belongs_to_subspace', on_delete=models.CASCADE)