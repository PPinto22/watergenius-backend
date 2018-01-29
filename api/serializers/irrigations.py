from rest_framework import serializers

from api.models.irrigations import IrrigationTime


class IrrigationTimeSerializer(serializers.ModelSerializer):
    irrigation_time_qty_unit = serializers.CharField(max_length=10, read_only=True)

    class Meta:
        model = IrrigationTime
        fields = ('irrigation_time_id', 'irrigation_time_date',
                  'irrigation_time_qty', 'irrigation_time_qty_unit',
                  'irrigation_time_sub')
        validators = []  # Remove a default "unique together" constraint.
