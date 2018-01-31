from rest_framework import serializers

from api.models import DayPlan


class DayPlanSerializer(serializers.ModelSerializer):
    dayplan_water_qty_unit = serializers.CharField(max_length=6, read_only=True)
    dayplan_rain_unit = serializers.CharField(max_length=6, read_only=True)

    class Meta:
        model = DayPlan
        fields = ('dayplan_id', 'dayplan_gen_time', 'dayplan_time',
                  'dayplan_water_qty', 'dayplan_water_qty_unit',
                  'dayplan_rain', 'dayplan_rain_unit',
                  'dayplan_sub')
        validators = []  # Remove a default "unique together" constraint.
