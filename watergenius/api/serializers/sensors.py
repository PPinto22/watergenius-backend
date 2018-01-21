from rest_framework import serializers

from api.models.sensors import Sensor, SensorType


class SensorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('sensor_id', 'sensor_name', 'sensor_state', 'sensor_esys', 'sensor_timerate', 'sensor_depth', 'sensor_type')
        validators = []  # Remove a default "unique together" constraint.


class SensorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorType
        fields = ('sensor_type_name_eng', 'sensor_type_name_por', 'sensor_type_unit')


class SensorSerializer(serializers.ModelSerializer):

    sensor_type = SensorTypeSerializer()

    class Meta:
        model = Sensor
        fields = ('sensor_id', 'sensor_name', 'sensor_state', 'sensor_esys', 'sensor_timerate', 'sensor_depth', 'sensor_type')