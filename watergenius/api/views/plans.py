from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *

from api.models.plans import DayPlan
from api.serializers.plans import DayPlanSerializer

class PlansListView(APIView):
    def get(self, request):
        print(request.META['QUERY_STRING'])
        query = (request.META['QUERY_STRING']).split('=')
        if query[0] == 'subspace':
            subspaceid = (query[1])
            dayplans = DayPlan.objects.filter(dayplan_sub=subspaceid)
        else:
            if len(query) > 1:
                return Response('unknown query', HTTP_400_BAD_REQUEST)
            # nao sei se faz sentido seqer. devolver so as do user logaddo
            # dayplans = DayPlan.objects.filter()
            dayplans = DayPlan.objects.all()
        serialize = DayPlanSerializer(list(dayplans), many=True)
        return Response(serialize.data, HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = DayPlanSerializer(data=data, partial=True)
        instance = DayPlan()
        if serializer.is_valid():
            for attr, value in serializer.validated_data.items():
                if attr != 'dayplan_id':
                    setattr(instance, attr, value)
            instance.save()
            return Response('OK', HTTP_200_OK)
        else:
            return Response('Internal error or malformed JSON ', HTTP_400_BAD_REQUEST)

class PlanDetailView(APIView):
    def get(self, request, planid):
        try:
            dayplans = DayPlan.objects.get(dayplan_id=planid)
        except ObjectDoesNotExist as e:
            return Response("That subspace doesn't even exist, fool", HTTP_400_BAD_REQUEST)
        serialize = DayPlanSerializer(dayplans, many=False)
        return Response(serialize.data, HTTP_200_OK)

    def delete(self, request, planid):
        try:
            dayplans = DayPlan.objects.get(dayplan_id=planid)
        except ObjectDoesNotExist as e:
            return Response("That subspace doesn't even exist, fool", HTTP_400_BAD_REQUEST)
        dayplans.delete()
        return Response("Dayplan deleted", HTTP_204_NO_CONTENT)