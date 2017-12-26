from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.parsers import JSONParser

from api.models.irrigations import IrrigationTime
from api.serializers.irrigations import IrrigationTimeSerializer


def irrigations(request, irrigationid=None):
    if request.method == 'GET':
        if irrigationid != None and irrigationid != "":
            try:
                dayplans = IrrigationTime.objects.get(irrigation_time_id=irrigationid)
            except ObjectDoesNotExist as e:
                return JsonResponse("That Irrigation action doesn't even exist, fool", status=400, safe=False)
            serialize = IrrigationTimeSerializer((dayplans), many=False)
            return JsonResponse(serialize.data, status=200, safe=False)
        print(request.META['QUERY_STRING'])
        query = (request.META['QUERY_STRING']).split('=')
        if query[0] == 'subspace':
            print('é isso evaristo')
            subspaceid = (query[1])
            dayplans = IrrigationTime.objects.filter(irrigation_time_sub=subspaceid)
        else:
            if len(query) > 1:
                return JsonResponse('unknown query', status=400, safe=False)
            # nao sei se faz sentido seqer. devolver so as do user logaddo
            # dayplans = Irrigation.objects.filter()
            dayplans = IrrigationTime.objects.all()
        serialize = IrrigationTimeSerializer(dayplans, many=True)
        return JsonResponse(serialize.data, status=200, safe=False)
    elif request.method == 'POST':
        # inserir
        data = JSONParser().parse(request)
        serializer = IrrigationTimeSerializer(data=data, partial=True)
        instance = IrrigationTime()
        if serializer.is_valid():
            for attr, value in serializer.validated_data.items():
                if attr != 'irrigation_time_id':
                    setattr(instance, attr, value)
            instance.save()
            return JsonResponse('OK', status=200, safe=False)
        else:
            return JsonResponse('Internal error or malformed JSON ', status=500, safe=False)

    elif request.method == 'PUT':
        # EDIT
        if irrigationid == None or irrigationid == "":
            return JsonResponse('Especify the Irrigation id', status=400, safe=False)
        data = JSONParser().parse(request)
        serializer = IrrigationTimeSerializer(data=data, partial=True)
        if serializer.is_valid():
            try:
                instance = IrrigationTime.objects.get(irrigation_time_id=irrigationid)
            except Exception as e:
                return JsonResponse('Especify the correct restrition id', status=400, safe=False)
            for attr, value in serializer.validated_data.items():
                if attr != 'irrigation_time_id':
                    print(attr)
                    setattr(instance, attr, value)
            instance.save()
            return JsonResponse('IrrigationTime edited with success', status=200, safe=False)
        else:
            return JsonResponse('Internal error or malformed json ', status=500, safe=False)

    elif request.method == 'DELETE':
        if irrigationid != None and irrigationid != "":
            try:
                dayplans = IrrigationTime.objects.get(irrigation_time_id=irrigationid)
            except ObjectDoesNotExist as e:
                return JsonResponse("That Irrigation time doesn't even exist, fool", status=400, safe=False)
            dayplans.delete()
            return JsonResponse("IrrigationTime deleted", status=200, safe=False)
        else:
            return JsonResponse(' Especify Irrigation ID in url', status=400, safe=False)

    return JsonResponse('error', status=400, safe=False)
