from rest_framework import serializers

from api.irrigations.models import IrrigationTime


class IrrigationTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IrrigationTime
        fields = ('irrigation_time_id', 'irrigation_time_date', 'irrigation_time_qtd', 'irrigation_time_sub')
        validators = []  # Remove a default "unique together" constraint.