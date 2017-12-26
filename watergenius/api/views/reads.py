from django.http import JsonResponse

from api.models.reads import Read
from api.serializers.reads import ReadSerializer


def reads(request):
    if request.method == 'GET':
        #print(request.META['QUERY_STRING'])
        #query = (request.META['QUERY_STRING']).split('=')
        #if query[0] == 'subspace':
        #    print('é isso evaristo')
        #    subspaceid = (query[1])
        #    dayplans = IrrigationTime.objects.filter(irrigation_time_sub=subspaceid)
        #data = JSONParser().parse(request)
        #serializer = SpaceSerializer(data=data,partial=True)
        #plants = SubSpace.objects.filter(sub_space_id=spaceid)
        reads = Read.objects.all()
        serialize = ReadSerializer(reads, many=True)
        return JsonResponse( serialize.data , status=200 ,safe=False)
    elif request.method == 'PUT':
        print ('iii')

    return JsonResponse('error', status=400, safe=False)