from rest_framework import serializers

from api.models.sensors import Sensor, SensorType


class SensorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorType
        fields = ('sensor_type_name_eng', 'sensor_type_name_por', 'sensor_type_unit')


class SensorSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(SensorSerializer, self).__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields['sensor_type'] = SensorTypeSerializer()

    class Meta:
        model = Sensor
        fields = ('sensor_id', 'sensor_name', 'sensor_state', 'sensor_esys',
                  'sensor_timerate', 'sensor_timerate_unit',
                  'sensor_depth', 'sensor_depth_unit', 'sensor_type')