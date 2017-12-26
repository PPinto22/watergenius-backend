from django.http import JsonResponse

from api.embeddedsys.models import EmbeddedSystem
from api.embeddedsys.serializers import EmbeddedSystemSerializer


def embeddedsystems(request):
    if request.method == 'GET':
        # print(request.META['QUERY_STRING'])
        # query = (request.META['QUERY_STRING']).split('=')
        # if query[0] == 'subspace':
        #    print('é isso evaristo')
        #    subspaceid = (query[1])
        #    dayplans = IrrigationTime.objects.filter(irrigation_time_sub=subspaceid)
        embedded = EmbeddedSystem.objects.all()
        serialize = EmbeddedSystemSerializer(embedded, many=True)
        return JsonResponse(serialize.data, status=200, safe=False)
    elif request.method == 'PUT':
        print('iii')

    return JsonResponse('error', status=400, safe=False)