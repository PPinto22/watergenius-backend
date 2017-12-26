from django.db import models

from api.plants.models import PlantType
from api.properties.models import Property

class Space(models.Model):
    space_id = models.AutoField(primary_key=True)
    space_name = models.CharField(max_length=50)
    space_description = models.CharField(max_length=150)
    space_irrigation_hour = models.IntegerField()
    space_property = models.ForeignKey(Property, related_name='belongs_to_property', on_delete=models.CASCADE)
    space_plant_type = models.ForeignKey(PlantType, related_name='has_plant_type', on_delete=models.CASCADE)

    def __str__(self):
        return 'id -> ' + str(self.space_id) + \
               ' Name -> ' + self.space_name + \
               " description -> " + self.space_description + \
               ' irrigation_hour  ' + str(self.space_irrigation_hour)


class TimeRestrition(models.Model):
    time_restrition_id = models.AutoField(primary_key=True)
    time_begin = models.DateTimeField()
    time_duration = models.DurationField()
    time_restrition_space = models.ForeignKey(Space, related_name='belongs_to_spaceid', on_delete=models.CASCADE)
