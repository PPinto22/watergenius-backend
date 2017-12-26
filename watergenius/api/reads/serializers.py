from rest_framework import serializers

from api.reads.models import Read


class ReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Read
        fields = ('read_id', 'read_timestamp', 'read_value', 'read_sensor' ,'read_dayplan','read_type')
        validators = [] # Remove a default "unique together" constraint.