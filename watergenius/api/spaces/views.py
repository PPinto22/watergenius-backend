from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.parsers import JSONParser

from api.properties.models import Property
from api.spaces.models import Space, TimeRestrition
from api.spaces.serializers import SpaceSerializer, TimeRestritionSerializer


# FIXME - Remover metodo put de /spaces; por em /spaces/<id>
def spaces(request, spaceid=None):
    if request.method == 'GET':
        print(spaceid)
        if spaceid != None:
            # TODO get this user email with the pinto way
            props = Property.objects.filter(prop_owner_id=request.user.email)
            queryset = Space.objects.filter(space_property__in=props.values('prop_id'))
            print(list(queryset))
            spaces = SpaceSerializer(list(queryset), many=True)
            return JsonResponse(spaces.data, status=200, safe=False)
        else:
            queryset = Space.objects.all()
            spaces = SpaceSerializer(queryset, many=True)
            return JsonResponse(spaces.data, status=200, safe=False)

    elif request.method == 'POST':
        # edit resource
        data = JSONParser().parse(request)
        serializer = SpaceSerializer(data=data, partial=True)
        if serializer.is_valid():
            instance = Space.objects.get(pk=serializer.data['space_id'])
            print(instance)
            for attr, value in serializer.validated_data.items():
                print(attr)
                if attr != 'space_id':
                    setattr(instance, attr, value)
            print(type(instance))
            instance.save()
            return JsonResponse('OK', status=200, safe=False)

    elif request.method == 'PUT':
        print('put')
        if spaceid != None:
            try:
                space = Space.objects.get(space_id=spaceid)
            except ObjectDoesNotExist as e:
                # insert
                print('nao existe')
                instance = Space()
                data = JSONParser().parse(request)
                serializer = SpaceSerializer(data=data, partial=True)
                if serializer.is_valid():
                    for attr, value in serializer.validated_data.items():
                        if attr != 'space_id':
                            print(attr)
                            setattr(instance, attr, value)
                    try:
                        space1 = Space.objects.get(space_id=serializer.data['space_id'])
                    except ObjectDoesNotExist as e:
                        instance.save()
                        return JsonResponse('OK', status=200, safe=False)
                    else:
                        return JsonResponse(
                            'a space with that id already exists. if you want to edit it, use post method', status=200,
                            safe=False)
                return JsonResponse('Internal error', status=500, safe=False)
            else:
                # already exists , overwrite or ignore?? DISCUSS
                return JsonResponse('This space in url already exists. if you want to edit it, use post method',
                                    status=200, safe=False)

        else:
            instance = Space()
            data = JSONParser().parse(request)
            serializer = SpaceSerializer(data=data, partial=True)
            if serializer.is_valid():
                for attr, value in serializer.validated_data.items():
                    if attr != 'space_id':
                        print(attr)
                        setattr(instance, attr, value)
                instance.save()
                return JsonResponse('OK', status=200, safe=False)

            return JsonResponse('Internal error', status=500, safe=False)
    elif request.method == 'DELETE':
        if spaceid != None:
            try:
                space = Space.objects.get(space_id=spaceid)
            except ObjectDoesNotExist:
                return JsonResponse("That space doesn't even exist, fool", status=400, safe=False)
            space.delete()
            return JsonResponse('Space deleted', status=200, safe=False)
        else:
            return JsonResponse(' Especify space ID in url', status=400, safe=False)

    return JsonResponse('error', status=400, safe=False)


# FIXME - Remover metodo post de /spaces/<id>/restrictions/<id>; por em /spaces/<id>/restrictions
def spacesRes(request, spaceid, resid=None):
    if request.method == 'GET':
        if resid == None or resid == "":
            if spaceid == None:
                return JsonResponse(' Especify space ID in url', status=400, safe=False)
            timeRes = TimeRestrition.objects.filter(time_restrition_space=spaceid)
            serializer = TimeRestritionSerializer(list(timeRes), many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
        else:
            # resid is valid
            try:
                timeRes = TimeRestrition.objects.get(time_restrition_id=resid)
            except ObjectDoesNotExist as e:
                return JsonResponse(' the especified time restrition doesnt exist for that space', status=400,
                                    safe=False)

            serializer = TimeRestritionSerializer(timeRes, many=False)
            return JsonResponse(serializer.data, status=200, safe=False)

    elif request.method == 'PUT':
        instance = TimeRestrition()
        data = JSONParser().parse(request)
        serializer = TimeRestritionSerializer(data=data, partial=True)
        if serializer.is_valid():
            for attr, value in serializer.validated_data.items():
                if attr != 'time_restrition_id':
                    print(attr)
                    setattr(instance, attr, value)
            instance.save()
            return JsonResponse('OK', status=200, safe=False)
        else:
            return JsonResponse('Internal error or malformed json ', status=500, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TimeRestritionSerializer(data=data, partial=True)
        if serializer.is_valid():
            if resid == None or resid == "":
                resid = serializer.validated_data['time_restrition_id']
            try:
                instance = TimeRestrition.objects.get(time_restrition_id=resid)
            except Exception as e:
                return JsonResponse('Especify the correct restrition id', status=400, safe=False)
            for attr, value in serializer.validated_data.items():
                if attr != 'time_restrition_id':
                    print(attr)
                    setattr(instance, attr, value)
            instance.save()
            return JsonResponse('Time restrition edited with success', status=200, safe=False)
        else:
            return JsonResponse('Internal error or malformed json ', status=500, safe=False)

    elif request.method == 'DELETE':
        if resid != None and resid != "":
            try:
                time = TimeRestrition.objects.filter(time_restrition_id=resid, time_restrition_space=spaceid)
            except ObjectDoesNotExist:
                return JsonResponse("That restrition doesn't even exist, fool", status=400, safe=False)
            if len(time) > 0:
                time.delete()
                return JsonResponse('restrition deleted', status=200, safe=False)

            return JsonResponse("That restrition doesn't even exist for that space, fool", status=400, safe=False)
        else:
            return JsonResponse(' Especify space ID in url', status=400, safe=False)

    return JsonResponse('error' + str(spaceid) + str(resid), status=400, safe=False)
