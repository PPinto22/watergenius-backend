from rest_framework import serializers

from api.models.sensors import Sensor


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('sensor_id', 'sensor_name', 'sensor_state', 'sensor_esys', 'sensor_timerate', 'sensor_depth', 'sensor_type')
        validators = []  # Remove a default "unique together" constraint.
