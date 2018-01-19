from django.db import models

from api.models.subspaces import SubSpace


class DayPlan(models.Model):
    dayplan_id = models.AutoField(primary_key=True)
    dayplan_gen_time = models.DateTimeField(auto_now=True)
    dayplan_time = models.DateTimeField()
    dayplan_water_qtd = models.FloatField()
    dayplan_sub = models.ForeignKey(SubSpace, related_name='belongs_to_subspace', on_delete=models.CASCADE)