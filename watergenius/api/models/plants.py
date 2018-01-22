from django.db import models


class PlantType(models.Model):
    plant_type_id = models.CharField(primary_key=True, max_length=65)
    plant_type_name_eng = models.CharField(max_length=65, default="")
    plant_type_name_por = models.CharField(max_length=65, default="")
