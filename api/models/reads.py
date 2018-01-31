from django.db import models
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError

from api.models.sensors import Sensor


def validate_read(value):
    if value > 100 or value < 0:
        raise ValidationError('Read value must be in the range [0, 100].')


class Read(models.Model):
    read_id = models.AutoField(primary_key=True)
    read_timestamp = models.DateTimeField(default=now)
    read_value = models.FloatField(validators=[validate_read])
    read_sensor = models.ForeignKey(Sensor, related_name='belongs_to_sensor', on_delete=models.CASCADE)
