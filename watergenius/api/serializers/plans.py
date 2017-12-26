from rest_framework import serializers

from api.models import DayPlan


class DayPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayPlan
        fields = ('dayplan_id', 'dayplan_gen_time', 'dayplan_time','dayplan_water_qtd', 'dayplan_sub')
        validators = [] # Remove a default "unique together" constraint.