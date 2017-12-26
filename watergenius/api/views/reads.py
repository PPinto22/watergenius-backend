from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.parsers import JSONParser

from api.models.reads import Read
from api.serializers.reads import ReadSerializer


def reads(request, readid=None):
    if request.method == 'GET':
        if readid != None and readid != "":
            try:
                dayplans = Read.objects.get(read_id=readid)
            except ObjectDoesNotExist as e:
                return JsonResponse("That Read  doesn't even exist, fool", status=400, safe=False)
            serialize = ReadSerializer((dayplans), many=False)
            return JsonResponse(serialize.data, status=200, safe=False)
        print(request.META['QUERY_STRING'])
        query = (request.META['QUERY_STRING']).split('=')
        if query[0] == 'sensor':
            sensor = (query[1])
            dayplans = Read.objects.filter(read_sensor_id=sensor)
        else:
            if len(query) > 1:
                return JsonResponse('unknown query', status=400, safe=False)
            # nao sei se faz sentido seqer. devolver so as do user logaddo
            dayplans = Read.objects.all()
        serialize = ReadSerializer(dayplans, many=True)
        return JsonResponse(serialize.data, status=200, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ReadSerializer(data=data, partial=True)
        instance = Read()
        if serializer.is_valid():
            for attr, value in serializer.validated_data.items():
                if attr != 'read_id':
                    setattr(instance, attr, value)
            instance.save()
            return JsonResponse('OK', status=200, safe=False)
        else:
            return JsonResponse('Internal error or malformed JSON ', status=500, safe=False)

    elif request.method == 'PUT':
        # EDIT
        if readid == None or readid == "":
            return JsonResponse('Especify the Read id in url', status=400, safe=False)
        data = JSONParser().parse(request)
        serializer = ReadSerializer(data=data, partial=True)
        if serializer.is_valid():
            try:
                instance = Read.objects.get(read_id=readid)
            except Exception as e:
                return JsonResponse('Especify the correct read id', status=400, safe=False)
            for attr, value in serializer.validated_data.items():
                if attr != 'sensor_id':
                    print(attr)
                    setattr(instance, attr, value)
            instance.save()
            return JsonResponse('Read edited with success', status=200, safe=False)
        else:
            return JsonResponse('Internal error or malformed json ', status=500, safe=False)

    elif request.method == 'DELETE':
        # if readid!=None and readid!="":
        #    try:
        #        dayplans = Read.objects.get(read_id=readid)
        #    except ObjectDoesNotExist as e:
        #        return JsonResponse("That  Read doesn't even exist, fool" , status=400 ,safe=False)
        #    dayplans.delete()
        #    return JsonResponse( "Read deleted" , status=200 ,safe=False)
        # else:
        # return JsonResponse(' Especify Read ID in url' , status=400 ,safe=False)
        return JsonResponse('Not Implemented', status=400, safe=False)
    return JsonResponse('error', status=400, safe=False)
