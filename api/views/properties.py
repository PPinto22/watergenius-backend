from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.properties import Property, CentralNode, UserManagesProperty
from api.serializers.properties import CentralNodeSerializer, PropertySerializer
from api.models.users import User
from api.serializers.users import UserSerializer


def getPropertiesOfUser(user):
    if user.is_superuser:
        return Property.objects.all()

    properties_managed = UserManagesProperty.objects.filter(user_id=user.email)
    props = Property.objects.filter(prop_id__in=properties_managed.values('prop_id'))
    return props


class PropertiesListView(APIView):
    def get(self, request):
        # TODO  check authenticated user and get only the properties of that user
        prop = getPropertiesOfUser(request.user)
        fullquery = (request.META['QUERY_STRING']).split('&')
        querylist = []
        for query in fullquery:
            querylist = querylist + (query.split('='))
        try:
            owner_index = querylist.index('ownerid')
            ownerid = querylist[owner_index + 1]
            prop = prop.filter(prop_owner_id=ownerid)
        except Exception as e:
            pass
        try:
            manager_index = querylist.index('managerid')
            managerid = querylist[manager_index + 1]
            properties_managed = UserManagesProperty.objects.filter(user_id=managerid)
            prop = prop.filter(prop_id__in=properties_managed.values('prop_id'))
        except Exception as e:
            pass
        serializer = PropertySerializer(instance=prop,
                                        nested_node=request.GET.get('nested_node', False),
                                        nest_level=request.GET.get('nest_level', 'properties'),
                                        many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = PropertySerializer(data=data, partial=True)
        if serializer.is_valid():
            property = serializer.create(serializer.validated_data)
            property.save()
            # adiciona o owner como manager
            managers = UserManagesProperty()
            managers.prop_id = property.prop_id
            managers.user_id = property.prop_owner_id
            managers.save()
            # cria nodo vazio
            node = CentralNode()
            node.node_property = property
            node.save()
            serializer = PropertySerializer(property, many=False)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)


class PropertyDetailView(APIView):
    def get(self, request, propid):
        props = getPropertiesOfUser(request.user)
        print(props)
        try:
            prop = props.get(prop_id=propid)
        except Exception as e:
            return Response(status=HTTP_400_BAD_REQUEST)

        serializer = PropertySerializer(instance=prop,
                                        nested_node=request.GET.get('nested_node', False),
                                        nest_level=request.GET.get('nest_level', 'properties'),
                                        many=False)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, propid):
        data = JSONParser().parse(request)
        serializer = PropertySerializer(data=data, partial=True)
        if serializer.is_valid():
            try:
                instance = Property.objects.get(prop_id=propid)
            except ObjectDoesNotExist as e:
                return Response('Specify the correct Property id', status=HTTP_400_BAD_REQUEST)
            for attr, value in serializer.validated_data.items():
                if attr != 'prop_id':
                    setattr(instance, attr, value)
            instance.save()
            serializer = PropertySerializer(instance, many=False)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response('Internal error or malformed json ', status=HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, propid):
        if propid != None and propid != "":
            try:
                prop = Property.objects.get(prop_id=propid)
            except ObjectDoesNotExist:
                return Response("That property doesn't even exist", status=HTTP_400_BAD_REQUEST)
            prop.delete()
            return Response('OK', status=HTTP_200_OK)
        else:
            return Response('Especify the property id', status=HTTP_400_BAD_REQUEST)


class PropertyManagersListView(APIView):
    def get(self, request, propid):
        managersOfProperty = UserManagesProperty.objects.filter(prop_id=propid)
        queryset = User.objects.filter(email__in=managersOfProperty.values('user_id'))
        serializer = UserSerializer(list(queryset), many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class PropertyManagerDetailView(APIView):
    def post(self, request, propid, managerid):
        try:
            user = User.objects.get(email=managerid)
        except ObjectDoesNotExist as e:
            return Response(' Invalid user mail ', status=HTTP_400_BAD_REQUEST)
        manager = UserManagesProperty()
        manager.user = user
        manager.prop = Property.objects.get(prop_id=propid)
        try:
            manager.save()
        except Exception:
            return Response(managerid + ' is the manager already', status=HTTP_200_OK)
        return Response('New Manager added', status=HTTP_200_OK)

    def delete(self, request, propid, managerid):
        try:
            usp = UserManagesProperty.objects.get(user_id=managerid, prop_id=propid)
        except ObjectDoesNotExist:
            return Response("That manager doesn't manage this property", status=HTTP_400_BAD_REQUEST)
        usp.delete()
        return Response('OK', status=HTTP_200_OK)


class PropertyNodeView(APIView):
    def get(self, request, propid):
        try:
            node = CentralNode.objects.get(node_property_id=propid)
        except ObjectDoesNotExist as e:
            return Response("That property doesn't have a central node", status=HTTP_200_OK)
        serializer = CentralNodeSerializer(node, many=False)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, propid):
        try:
            node = CentralNode.objects.get(node_property_id=propid)
            data = JSONParser().parse(request)
            serializer = CentralNodeSerializer(data=data, partial=True)
            if serializer.is_valid():
                instance = node
                for attr, value in serializer.validated_data.items():
                    if attr != 'node_property':
                        setattr(instance, attr, value)
                instance.save()
                return Response(CentralNodeSerializer(instance).data, status=HTTP_200_OK)
            return Response('Internal error or malformed JSON ', status=HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            # Nodo nao existe; criar um novo
            data = JSONParser().parse(request)
            data['node_property'] = propid
            serializer = CentralNodeSerializer(data=data, partial=True)
            if serializer.is_valid():
                node = serializer.create(serializer.validated_data)
                node.save()
                return Response(CentralNodeSerializer(node).data, status=HTTP_200_OK)
            return Response('Internal error or malformed JSON ', status=HTTP_400_BAD_REQUEST)
