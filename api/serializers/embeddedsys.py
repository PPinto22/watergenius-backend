from rest_framework import serializers

from api.models import Sensor
from api.models.embeddedsys import EmbeddedSystem
from api.serializers.sensors import SensorSerializer


class EmbeddedSystemSerializer(serializers.ModelSerializer):

    def __init__(self, *args, nest_level='embeddedsys', **kwargs):
        super(EmbeddedSystemSerializer, self).__init__(*args, **kwargs)

        self.nest_level = nest_level

        if nest_level in ['sensors']:
            self.fields['esys_sensors'] = serializers.SerializerMethodField()

    def get_esys_sensors(self, esys):
        sensors = Sensor.objects.filter(sensor_esys=esys.esys_id)
        return SensorSerializer(instance=sensors, many=True).data

    class Meta:
        model = EmbeddedSystem
        fields = (
        'esys_id', 'esys_local_long', 'esys_local_lat', 'esys_local_alt', 'esys_sub', 'esys_state', 'esys_name')
        validators = []  # Remove a default "unique together" constraint.
