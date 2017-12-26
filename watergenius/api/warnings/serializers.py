from rest_framework import serializers

from api.warnings.models import Warnings


class WarningsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warnings
        fields = ( 'warning_id', 'warning_description')
        validators = []  # Remove a default "unique together" constraint.