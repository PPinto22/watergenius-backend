from rest_framework import serializers

from api.models import Sensor
from api.models.embeddedsys import EmbeddedSystem
from api.serializers.sensors import SensorSerializer
from django.utils import timezone

class EmbeddedSystemSerializer(serializers.ModelSerializer):

    def __init__(self, *args, nest_level='embeddedsys', **kwargs):
        super(EmbeddedSystemSerializer, self).__init__(*args, **kwargs)

        self.nest_level = nest_level

        if nest_level in ['sensors']:
            self.fields['esys_sensors'] = serializers.SerializerMethodField()


        self.fields['esys_state'] = serializers.SerializerMethodField('check_state')
    
    def check_state(self, esys):
        res = ((timezone.now() - timezone.timedelta(minutes=15) <= esys.esys_last_read ) )
        if res:
            return 1 
        else:
            return 0

    def get_esys_sensors(self, esys):
        sensors = Sensor.objects.filter(sensor_esys=esys.esys_id)
        return SensorSerializer(instance=sensors, many=True).data

    class Meta:
        model = EmbeddedSystem
        fields = (
        'esys_id', 'esys_local_long', 'esys_local_lat', 'esys_local_alt', 'esys_sub' , 'esys_name')
        validators = []  # Remove a default "unique together" constraint.
