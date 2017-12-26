from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.parsers import JSONParser

from api.models.subspaces import SubSpace
from api.serializers.subspaces import SubSpaceSerializer

def subspaces(request, subspaceid=None):
    if request.method == 'GET':
        if subspaceid != None:
            plants = SubSpace.objects.filter(sub=subspaceid)
            serialize = SubSpaceSerializer(plants, many=True)
            return JsonResponse(serialize.data, status=200, safe=False)
        else:
            # TODO get all subspaces of logged user
            plants = SubSpace.objects.all()
            serialize = SubSpaceSerializer(plants, many=True)
            return JsonResponse(serialize.data, status=200, safe=False)
    elif request.method == 'POST':  # create
        data = JSONParser().parse(request)
        serializer = SubSpaceSerializer(data=data, partial=True)
        instance = SubSpace()
        if serializer.is_valid():
            for attr, value in serializer.validated_data.items():
                if attr != 'sub':
                    setattr(instance, attr, value)
            instance.save()
            return JsonResponse('OK', status=200, safe=False)
        else:
            return JsonResponse('Internal error or malformed JSON ', status=500, safe=False)

    elif request.method == 'PUT':  # edit
        if subspaceid == None or subspaceid == "":
            return JsonResponse('Especify the subspace id', status=400, safe=False)
        data = JSONParser().parse(request)
        serializer = SubSpaceSerializer(data=data, partial=True)
        if serializer.is_valid():
            try:
                instance = SubSpace.objects.get(sub=subspaceid)
            except Exception as e:
                return JsonResponse('Especify the correct restrition id', status=400, safe=False)
            for attr, value in serializer.validated_data.items():
                if attr != 'sub':
                    print(attr)
                    setattr(instance, attr, value)
            instance.save()
            return JsonResponse('Subsapce edited with success', status=200, safe=False)
        else:
            return JsonResponse('Internal error or malformed json ', status=500, safe=False)

    elif request.method == 'DELETE':
        if subspaceid != None and subspaceid != "":
            try:
                space = SubSpace.objects.get(sub=subspaceid)
            except ObjectDoesNotExist:
                return JsonResponse("That subspace doesn't even exist, fool", status=400, safe=False)
            space.delete()
            return JsonResponse('SubSpace deleted', status=200, safe=False)
        else:
            return JsonResponse(' Especify subspace ID in url', status=400, safe=False)
    return JsonResponse('error', status=400, safe=False)
