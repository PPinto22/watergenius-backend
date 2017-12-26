from rest_framework import serializers

from api.models.embeddedsys import EmbeddedSystem


class EmbeddedSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmbeddedSystem
        fields = ('esys_id', 'esys_local', 'esys_sub', 'esys_state')
        validators = []  # Remove a default "unique together" constraint.