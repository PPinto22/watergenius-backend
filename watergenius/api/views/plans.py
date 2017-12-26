from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.parsers import JSONParser

from api.models.plans import DayPlan
from api.serializers.plans import DayPlanSerializer


def plans(request, planid=None):
    if request.method == 'GET':
        if planid != None and planid != "":
            try:
                dayplans = DayPlan.objects.get(dayplan_id=planid)
            except ObjectDoesNotExist as e:
                return JsonResponse("That subspace doesn't even exist, fool", status=400, safe=False)
            serialize = DayPlanSerializer((dayplans), many=False)
            return JsonResponse(serialize.data, status=200, safe=False)

        print(request.META['QUERY_STRING'])
        query = (request.META['QUERY_STRING']).split('=')
        if query[0] == 'subspace':
            subspaceid = (query[1])
            dayplans = DayPlan.objects.filter(dayplan_sub=subspaceid)
        else:
            if len(query) > 1:
                return JsonResponse('unknown query', status=400, safe=False)
            # nao sei se faz sentido seqer. devolver so as do user logaddo
            # dayplans = DayPlan.objects.filter()
            dayplans = DayPlan.objects.all()
        serialize = DayPlanSerializer(list(dayplans), many=True)
        return JsonResponse(serialize.data, status=200, safe=False)
    elif request.method == 'POST':
        # inserir
        data = JSONParser().parse(request)
        serializer = DayPlanSerializer(data=data, partial=True)
        instance = DayPlan()
        if serializer.is_valid():
            for attr, value in serializer.validated_data.items():
                if attr != 'dayplan_id':
                    setattr(instance, attr, value)
            instance.save()
            return JsonResponse('OK', status=200, safe=False)
        else:
            return JsonResponse('Internal error or malformed JSON ', status=500, safe=False)

    elif request.method == 'DELETE':
        if planid != None and planid != "":
            try:
                dayplans = DayPlan.objects.get(dayplan_id=planid)
            except ObjectDoesNotExist as e:
                return JsonResponse("That subspace doesn't even exist, fool", status=400, safe=False)
            dayplans.delete()
            return JsonResponse("Dayplan deleted", status=200, safe=False)
        else:
            return JsonResponse(' Especify dayplan ID in url', status=400, safe=False)

    return JsonResponse('error', status=400, safe=False)
