from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.parsers import JSONParser

from api.models.sensors import Sensor
from api.serializers.sensors import SensorSerializer


def sensors(request, sensid=None):
    if request.method == 'GET':
        if sensid != None and sensid != "":
            try:
                dayplans = Sensor.objects.get(sensor_id=sensid)
            except ObjectDoesNotExist as e:
                return JsonResponse("That Sensor  doesn't even exist, fool", status=400, safe=False)
            serialize = SensorSerializer((dayplans), many=False)
            return JsonResponse(serialize.data, status=200, safe=False)
        print(request.META['QUERY_STRING'])
        query = (request.META['QUERY_STRING']).split('=')
        if query[0] == 'embeddedsys':
            embeddedsys = (query[1])
            dayplans = Sensor.objects.filter(sensor_sub_id=embeddedsys)
        else:
            if len(query) > 1:
                return JsonResponse('unknown query', status=400, safe=False)
            # nao sei se faz sentido seqer. devolver so as do user logaddo
            dayplans = Sensor.objects.all()
        serialize = SensorSerializer(dayplans, many=True)
        return JsonResponse(serialize.data, status=200, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SensorSerializer(data=data, partial=True)
        instance = Sensor()
        if serializer.is_valid():
            for attr, value in serializer.validated_data.items():
                if attr != 'sensor_id':
                    setattr(instance, attr, value)
            instance.save()
            return JsonResponse('OK', status=200, safe=False)
        else:
            return JsonResponse('Internal error or malformed JSON ', status=500, safe=False)

    elif request.method == 'PUT':
        # EDIT
        if sensid == None or sensid == "":
            return JsonResponse('Especify the Sensor id in url', status=400, safe=False)
        data = JSONParser().parse(request)
        serializer = SensorSerializer(data=data, partial=True)
        if serializer.is_valid():
            try:
                instance = Sensor.objects.get(sensor_id=sensid)
            except Exception as e:
                return JsonResponse('Especify the correct Sensor id', status=400, safe=False)
            for attr, value in serializer.validated_data.items():
                if attr != 'sensor_id':
                    print(attr)
                    setattr(instance, attr, value)
            instance.save()
            return JsonResponse('Sensor edited with success', status=200, safe=False)
        else:
            return JsonResponse('Internal error or malformed json ', status=500, safe=False)

    elif request.method == 'DELETE':
        if sensid != None and sensid != "":
            try:
                dayplans = Sensor.objects.get(sensor_id=sensid)
            except ObjectDoesNotExist as e:
                return JsonResponse("That  Sensor doesn't even exist, fool", status=400, safe=False)
            dayplans.delete()
            return JsonResponse("Sensor deleted", status=200, safe=False)
        else:
            return JsonResponse(' Especify Sensor ID in url', status=400, safe=False)

    return JsonResponse('error', status=400, safe=False)
