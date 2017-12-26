from django.http import JsonResponse

from api.subspaces.models import SubSpace
from api.subspaces.serializers import SubSpaceSerializer


def subspaces(request, spaceid=None):
    if request.method == 'GET':
        print(spaceid)
        if spaceid != None:
            # data = JSONParser().parse(request)
            # serializer = SpaceSerializer(data=data,partial=True)
            plants = SubSpace.objects.filter(sub_space_id=spaceid)
            serialize = SubSpaceSerializer(plants, many=True)
            return JsonResponse(serialize.data, status=200, safe=False)
        else:
            plants = SubSpace.objects.all()
            serialize = SubSpaceSerializer(plants, many=True)
            return JsonResponse(serialize.data, status=200, safe=False)
    elif request.method == 'PUT':
        print('iii')
    return JsonResponse('error', status=400, safe=False)