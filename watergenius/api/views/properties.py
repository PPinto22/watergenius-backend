from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.parsers import JSONParser

from api.models.properties import Property, CentralNode, UserManagesProperty
from api.serializers.properties import CentralNodeSerializer, PropertySerializer
from api.models.users import User
from api.serializers.users import UserSerializer

# /properties/{id}/managers
def propertiesManagers(request, propid=None, managerid=None):
    print(managerid)
    print(propid)
    if propid == None:
        return JsonResponse(' Please especify the property id', status=400, safe=False)
    if request.method == 'GET':
        if managerid == None or managerid=="":
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
        if managerid != None or managerid=="":
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
        if managerid != None or managerid=="":
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
        #EDIT
        try:
            node = CentralNode.objects.get(node_property_id=propid)
        except ObjectDoesNotExist as e:
            return JsonResponse("That property doesn't even exist", status=400, safe=False)
        else:
            data = JSONParser().parse(request)
            serializer = CentralNodeSerializer(data=data, partial=True)
            print(serializer)
            print(serializer.is_valid())
            if serializer.is_valid():
                try:
                    instance = node
                except ObjectDoesNotExist as e:
                    return JsonResponse('Especify the correct Property id', status=400, safe=False)
                for attr, value in serializer.validated_data.items():
                    if attr != 'node_property' and attr != 'node_id':
                        print(attr)
                        setattr(instance, attr, value)
                instance.save()
                return JsonResponse('Central Node edited with success', status=200, safe=False)
            return JsonResponse('Internal error or malformed JSON ', status=500, safe=False)
        
        #try:
        #    node = CentralNode.objects.get(node_property_id=propid)
        #except ObjectDoesNotExist as e:
        #    data = JSONParser().parse(request)
        #    serializer = CentralNodeSerializer(data=data, partial=True)
        #    if serializer.is_valid():
        #        serializer.node_id = -1
        #        serializer.save()
        #        return JsonResponse('Central Node created', status=200, safe=False)
        #else:
            # already exists, error
        #    return JsonResponse(
        #        'That property already has a central node. if you want to edit the central node, use post method',
        #        status=200, safe=False)
    elif request.method == 'POST':
        #CREATE
        try:
            node = CentralNode.objects.get(node_property_id=propid)
        except ObjectDoesNotExist as e:
            node = CentralNode()
            data = JSONParser().parse(request)
            print(data)
            serializer = CentralNodeSerializer(data=data, partial=True)
            print(serializer.is_valid())
            print(serializer)
            if serializer.is_valid():
                for attr, value in serializer.validated_data.items():
                    if attr != 'node_id':
                        setattr(node, attr, value)
                node.save()
                return JsonResponse('Central Node created', status=200, safe=False)
            return JsonResponse('Internal error or malformed JSON ', status=500, safe=False)
        else:
            return JsonResponse("That property already have a central node", status=404, safe=False)
        
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
        #if propid != None:
        #try:
        #    instance = Property.objects.get(prop_id=propid)
        #except ObjectDoesNotExist:
        #    return JsonResponse("That property doesn't even exist", status=400, safe=False)
        
        # NOTE : not inserting in api_usermanagesproperty DISCUSS
        data = JSONParser().parse(request)
        serializer = PropertySerializer(data=data, partial=True)
        if serializer.is_valid():
            for attr, value in serializer.validated_data.items():
                print(attr)
                #if attr != 'prop_id' and attr != 'prop_owner':
                if attr != 'prop_id':
                    setattr(instance, attr, value)
            print(type(instance))
            instance.save()
            return JsonResponse('Property created', status=200, safe=False)
        else:
            return JsonResponse('Internal error or malformed JSON', status=500, safe=False)
    elif request.method == 'PUT':
        #EDIT 
        if propid == None or propid == "":
            return JsonResponse('Especify the Property id in url', status=400, safe=False)
        data = JSONParser().parse(request)
        serializer = PropertySerializer(data=data, partial=True)
        if serializer.is_valid():
            try:
                instance = Property.objects.get(prop_id=propid)
            except ObjectDoesNotExist as e:
                return JsonResponse('Especify the correct Property id', status=400, safe=False)
            for attr, value in serializer.validated_data.items():
                if attr != 'prop_id':
                    print(attr)
                    setattr(instance, attr, value)
            instance.save()
            return JsonResponse('Property edited with success', status=200, safe=False)
        else:
            return JsonResponse('Internal error or malformed json ', status=500, safe=False)

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
