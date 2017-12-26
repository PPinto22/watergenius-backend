from rest_framework import serializers

from api.sensors.models import Sensor


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('sensor_id', 'sensor_state', 'sensor_sub', 'sensor_timerate' ,'sensor_depth','sensor_type')
        validators = [] # Remove a default "unique together" constraint.