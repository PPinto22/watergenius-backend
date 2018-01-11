from django.db import models

from api.models.plants import PlantType
from api.models.properties import Property

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


class TimeRestriction(models.Model):
    time_restriction_id = models.AutoField(primary_key=True)
    time_restriction_begin = models.DateTimeField()
    time_restriction_end = models.DurationField()
    time_restriction_space = models.ForeignKey(Space, related_name='belongs_to_spaceid', on_delete=models.CASCADE)
