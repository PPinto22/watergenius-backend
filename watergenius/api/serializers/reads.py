from rest_framework import serializers

from api.models.reads import Read


class ReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Read
        fields = ('read_id', 'read_timestamp', 'read_value', 'read_sensor')
        validators = []  # Remove a default "unique together" constraint.
