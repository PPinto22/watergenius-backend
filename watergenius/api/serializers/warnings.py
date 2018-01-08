from rest_framework import serializers

from api.models.warnings import Warning


class WarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warning
        fields = ( 'warning_id', 'warning_description', 'warning_property')
        validators = []  # Remove a default "unique together" constraint.