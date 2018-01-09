from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from api.models.properties import Property , UserManagesProperty
from api.models.spaces import Space
from api.models.subspaces import SubSpace
from api.serializers.subspaces import SubSpaceSerializer



def getSubspacesByEmail(email):
    properties_managed = UserManagesProperty.objects.filter(user_id=email)
    spaces_managed = Space.objects.filter(space_property_id__in=properties_managed.values('prop_id'))
    subspaces_of_user = SubSpace.objects.filter(sub_space_id_id__in=spaces_managed.values('space_id'))
    return subspaces_of_user

class SubspacesListView(APIView):
    def get(self, request):
        subspaces = getSubspacesByEmail(request.user.email)
        print(subspaces)
        fullquery = (request.META['QUERY_STRING']).split('&')
        querylist = []
        for query in fullquery :
            querylist = querylist + (query.split('='))
        try:
            property_index = querylist.index('propertyid')
            propertyid = querylist[property_index+1]
            props = Property.objects.get(prop_id=propertyid)
            spaces = Space.objects.filter(space_property_id = props.prop_id)
            subspaces = subspaces.filter(sub_space_id_id__in=spaces.values('space_id'))
        except Exception as e:
            print( e)
            pass
        try:
            space_index = querylist.index('spaceid')
            spaceid = querylist[space_index+1]
            #spaces = Space.objects.get(space_id = props.values(space_id))
            subspaces = subspaces.filter(sub_space_id_id=spaceid)
        except Exception as e:
            print( e)
            pass
        serialize = SubSpaceSerializer(subspaces, many=True)
        return Response(serialize.data, HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = SubSpaceSerializer(data=data, partial=True)
        if serializer.is_valid():
            instance = serializer.create(serializer.validated_data)
            instance.save()
            serialize = SubSpaceSerializer(instance, many=False)
            return Response(serialize.data, HTTP_200_OK)
        else:
            return Response('Internal error or malformed JSON ', HTTP_400_BAD_REQUEST)

class SubspaceDetailView(APIView):
    def get(self, request, subspaceid):
        subspaces = getSubspacesByEmail(request.user.email)
        plants = subspaces.filter(sub=subspaceid)
        serialize = SubSpaceSerializer(plants, many=True)
        return Response(serialize.data, HTTP_200_OK)

    def put(self, request, subspaceid):
        data = JSONParser().parse(request)
        serializer = SubSpaceSerializer(data=data, partial=True)
        if serializer.is_valid():
            try:
                instance = SubSpace.objects.get(sub=subspaceid)
            except Exception as e:
                return Response('Especify the correct restrition id', HTTP_400_BAD_REQUEST)
            for attr, value in serializer.validated_data.items():
                if attr != 'sub':
                    print(attr)
                    setattr(instance, attr, value)
            instance.save()
            serialize = SubSpaceSerializer(instance, many=False)
            return Response(serialize.data, HTTP_200_OK)
        else:
            return Response('Internal error or malformed json ', HTTP_400_BAD_REQUEST)

    def delete(self, request, subspaceid):
        try:
            subspaces = getSubspacesByEmail(request.user.email)
            space = subspaces.objects.get(sub=subspaceid)
        except ObjectDoesNotExist:
            return Response("That subspace doesn't even exist or isn't yours, fool", HTTP_400_BAD_REQUEST)
        space.delete()
        return Response('SubSpace deleted', HTTP_204_NO_CONTENT)
