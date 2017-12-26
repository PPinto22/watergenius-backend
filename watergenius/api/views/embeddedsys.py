from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.parsers import JSONParser

from api.models.embeddedsys import EmbeddedSystem
from api.serializers.embeddedsys import EmbeddedSystemSerializer


def embeddedsystems(request, sysid=None):
    if request.method == 'GET':
        if sysid != None and sysid != "":
            try:
                dayplans = EmbeddedSystem.objects.get(esys_id=sysid)
            except ObjectDoesNotExist as e:
                return JsonResponse("That EmbeddedSystem  doesn't even exist, fool", status=400, safe=False)
            serialize = EmbeddedSystemSerializer((dayplans), many=False)
            return JsonResponse(serialize.data, status=200, safe=False)
        print(request.META['QUERY_STRING'])
        query = (request.META['QUERY_STRING']).split('=')
        if query[0] == 'subspace':
            subspaceid = (query[1])
            dayplans = EmbeddedSystem.objects.filter(esys_id=subspaceid)
        else:
            if len(query) > 1:
                return JsonResponse('unknown query', status=400, safe=False)
            # nao sei se faz sentido seqer. devolver so as do user logaddo
            dayplans = EmbeddedSystem.objects.all()
        serialize = EmbeddedSystemSerializer(dayplans, many=True)
        return JsonResponse(serialize.data, status=200, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EmbeddedSystemSerializer(data=data, partial=True)
        instance = EmbeddedSystem()
        if serializer.is_valid():
            for attr, value in serializer.validated_data.items():
                if attr != 'esys_id':
                    setattr(instance, attr, value)
            instance.save()
            return JsonResponse('OK', status=200, safe=False)
        else:
            return JsonResponse('Internal error or malformed JSON ', status=500, safe=False)

    elif request.method == 'PUT':
        # EDIT
        if sysid == None or sysid == "":
            return JsonResponse('Especify the EmbeddedSystem id in url', status=400, safe=False)
        data = JSONParser().parse(request)
        serializer = EmbeddedSystemSerializer(data=data, partial=True)
        if serializer.is_valid():
            try:
                instance = EmbeddedSystem.objects.get(esys_id=sysid)
            except Exception as e:
                return JsonResponse('Especify the correct EmbeddedSystem id', status=400, safe=False)
            for attr, value in serializer.validated_data.items():
                if attr != 'esys_id':
                    print(attr)
                    setattr(instance, attr, value)
            instance.save()
            return JsonResponse('EmbeddedSystem edited with success', status=200, safe=False)
        else:
            return JsonResponse('Internal error or malformed json ', status=500, safe=False)

    elif request.method == 'DELETE':
        if sysid != None and sysid != "":
            try:
                dayplans = EmbeddedSystem.objects.get(esys_id=sysid)
            except ObjectDoesNotExist as e:
                return JsonResponse("That  EmbeddedSystem doesn't even exist, fool", status=400, safe=False)
            dayplans.delete()
            return JsonResponse("EmbeddedSystem deleted", status=200, safe=False)
        else:
            return JsonResponse(' Especify EmbeddedSystem ID in url', status=400, safe=False)

    return JsonResponse('error', status=400, safe=False)
