from django.db import models


class PlantType(models.Model):
    plant_type_id = models.AutoField(primary_key=True)
    plant_type_name = models.CharField(max_length=50)
