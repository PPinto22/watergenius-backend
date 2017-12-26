from django.http import JsonResponse

from api.plans.models import DayPlan
from api.reads.serializers import DayPlanSerializer


def plans(request):
    if request.method == 'GET':
        print(request.META['QUERY_STRING'])
        query = (request.META['QUERY_STRING']).split('=')
        if query[0] == 'subspace':
            subspaceid = (query[1])
            dayplans = DayPlan.objects.filter(dayplan_sub=subspaceid)
        # data = JSONParser().parse(request)
        # serializer = SpaceSerializer(data=data,partial=True)
        # plants = SubSpace.objects.filter(sub_space_id=spaceid)
        serialize = DayPlanSerializer(dayplans, many=True)
        return JsonResponse(serialize.data, status=200, safe=False)
    elif request.method == 'PUT':
        print('iii')
