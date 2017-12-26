from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.parsers import JSONParser

from api.properties.models import Property, CentralNode
from api.properties.serializers import CentralNodeSerializer, PropertySerializer
from api.users.models import User, UserManagesProperty
# /properties/{id}/managers
from api.users.serializers import UserSerializer


def propertiesManagers(request, propid=None, managerid=None):
    print(managerid)
    print(propid)
    if propid == None:
        return JsonResponse(' Please especify the property id', status=400, safe=False)
    if request.method == 'GET':
        if managerid == None:
            # return all managers of that property
            managersOfProperty = UserManagesProperty.objects.filter(prop_has_id=propid)
            queryset = User.objects.filter(email__in=managersOfProperty.values('user_has_id'))
            print(list(queryset))
            serializer = UserSerializer(list(queryset), many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            managersOfProperty = UserManagesProperty.objects.filter(prop_has_id=propid)
            queryset = User.objects.filter(email__in=managersOfProperty.values('user_has_id'), )

    if request.method == 'PUT':
        if managerid != None:
            # NOTE: put = set user has manager??
            try:
                user = User.objects.get(email=managerid)
            except Exception as e:
                return JsonResponse(' Invalid user mail ', status=400, safe=False)
            manager = UserManagesProperty()
            manager.user_has_id = user
            manager.prop_has_id = Property.objects.get(prop_id=propid)
            try:
                manager.save()
            except Exception:
                return JsonResponse(managerid + ' is the manager already', status=200, safe=False)
            return JsonResponse('New Manager added', status=200, safe=False)
        else:
            return JsonResponse(' Please especify the property id', status=400, safe=False)

    if request.method == 'DELETE':
        if managerid != None:
            try:
                usp = UserManagesProperty.objects.get(user_has_id=managerid, prop_has_id=propid)
            except ObjectDoesNotExist:
                return JsonResponse("That manager doesn't manage this property", status=400, safe=False)
            usp.delete()
            return JsonResponse('OK', status=200, safe=False)
        else:
            return JsonResponse('Especify the property id', status=400, safe=False)

    return JsonResponse('Not supported' + str(propid) + str(), status=400, safe=False)


# /properties/{id}/node
def propertiesNode(request, propid=None):
    if propid == None:
        return JsonResponse(' Please especify the property id', status=400, safe=False)

    if request.method == 'GET':
        try:
            node = CentralNode.objects.get(node_property_id=propid)
        except ObjectDoesNotExist as e:
            return JsonResponse("That property doesn't have a central node", status=404, safe=False)

        serializer = CentralNodeSerializer(node, many=False)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        try:
            node = CentralNode.objects.get(node_property_id=propid)
        except ObjectDoesNotExist as e:
            data = JSONParser().parse(request)
            serializer = CentralNodeSerializer(data=data, partial=True)
            if serializer.is_valid():
                serializer.node_id = -1
                serializer.save()
                return JsonResponse('Central Node created', status=200, safe=False)
        else:
            # already exists, error
            return JsonResponse(
                'That property already has a central node. if you want to edit the central node, use post method',
                status=200, safe=False)
    elif request.method == 'POST':
        try:
            node = CentralNode.objects.get(node_property_id=propid)
        except ObjectDoesNotExist as e:
            return JsonResponse("That property doesn't have a central node", status=404, safe=False)
        data = JSONParser().parse(request)
        serializer = CentralNodeSerializer(data=data, partial=True)
        print(serializer.is_valid())
        print(serializer.data)
        if serializer.is_valid():
            for attr, value in serializer.validated_data.items():
                # NOTE: not allowing to change property id . DISCUSS
                if attr != 'node_id' and attr != 'node_property':
                    setattr(node, attr, value)
            node.save()
            return JsonResponse('Central Node updated', status=200, safe=False)
        else:
            return JsonResponse('Internal error', status=500, safe=False)
    return JsonResponse('NOT SUPPORTED' + str(propid), status=400, safe=False)


# Propertys/{id}
def properties(request, propid=None):
    if request.method == 'GET':
        # data = JSONParser().parse(request)
        if propid != None:
            # TODO  check authenticated user and get only the properties of that user
            prop = Property.objects.filter(prop_id=propid)
            print(prop)
            serializer = PropertySerializer(list(prop), many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
        else:
            owner = request.user
            print(owner)
            prop = Property.objects.filter(prop_owner_id=owner)
            serializer = PropertySerializer(prop, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)

    elif request.method == 'POST':
        print('ao poste')
        if propid != None:
            try:
                instance = Property.objects.get(prop_id=propid)
            except ObjectDoesNotExist:
                return JsonResponse("That property doesn't even exist", status=400, safe=False)
            data = JSONParser().parse(request)
            serializer = PropertySerializer(data=data, partial=True)
            if serializer.is_valid():
                for attr, value in serializer.validated_data.items():
                    print(attr)
                    if attr != 'prop_id' and attr != 'prop_owner':
                        setattr(instance, attr, value)
                print(type(instance))
                instance.save()
                return JsonResponse('Property updated', status=200, safe=False)
        else:
            return JsonResponse('Especify the property id', status=400, safe=False)
    elif request.method == 'PUT':
        # NOTE : not inserting in api_usermanagesproperty DISCUSS
        if propid != None:
            # especificou id no url ( makes sense? dunno)
            try:
                instance = Property.objects.get(prop_id=propid)
            except ObjectDoesNotExist:
                instance = None
            if instance != None:
                data = JSONParser().parse(request)
                serializer = PropertySerializer(data=data, partial=True)
                if serializer.is_valid():
                    if serializer.is_valid():
                        for attr, value in serializer.validated_data.items():
                            print(attr)
                            if attr != 'prop_id' or attr != 'prop_owner':
                                setattr(instance, attr, value)
                        instance.save()
                    return JsonResponse('Property updated', status=200, safe=False)
                else:
                    return JsonResponse('Internal error', status=500, safe=False)
            else:
                # doesn't exist, create
                data = JSONParser().parse(request)
                serializer = PropertySerializer(data=data, partial=True)
                if serializer.is_valid():
                    serializer.prop_id = -1
                    serializer.save()
                    return JsonResponse('New property created', status=200, safe=False)

        else:
            # create the resource with auto id
            data = JSONParser().parse(request)
            serializer = PropertySerializer(data=data, partial=True)
            if serializer.is_valid():
                serializer.prop_id = -1
                serializer.save()
                return JsonResponse('New property created', status=200, safe=False)
            else:
                return JsonResponse('Internal error', status=500, safe=False)

    elif request.method == 'DELETE':
        if propid != None:
            try:
                prop = Property.objects.get(prop_id=propid)
            except ObjectDoesNotExist:
                return JsonResponse("That property doesn't even exist", status=400, safe=False)
            prop.delete()
            return JsonResponse('OK', status=200, safe=False)
        else:
            return JsonResponse('Especify the property id', status=400, safe=False)

    return JsonResponse('error', status=501, safe=False)
