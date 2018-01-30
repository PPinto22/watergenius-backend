from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *

from api.models import Property, User
from api.models.properties import UserManagesProperty
from api.models.spaces import Space, TimeRestriction
from api.serializers.spaces import SpaceSerializer, TimeRestrictionSerializer


def getSpacesOfUser(user):
    if user.is_superuser:
        return Space.objects.all()

    properties_managed = UserManagesProperty.objects.filter(user_id=user.email)
    props = Property.objects.filter(prop_id__in=properties_managed.values('prop_id'))
    spaces = Space.objects.filter(space_property__in=props.values('prop_id'))
    return spaces


class SpacesListView(APIView):
    def get(self, request):
        all_spaces = getSpacesOfUser(request.user)
        fullquery = (request.META['QUERY_STRING']).split('&')
        querylist = []
        for query in fullquery:
            querylist = querylist + (query.split('='))
        try:
            owner_index = querylist.index('ownerid')
            ownerid = querylist[owner_index + 1]
            props = Property.objects.filter(prop_owner_id=ownerid)
            all_spaces = all_spaces.filter(space_property_id__in=props.values('prop_id'))
        except Exception as e:
            pass
        try:
            manager_index = querylist.index('managerid')
            managerid = querylist[manager_index + 1]
            properties_managed = UserManagesProperty.objects.filter(user_id=managerid)
            all_spaces = all_spaces.filter(space_property_id__in=properties_managed.values('prop_id'))
        except Exception as e:
            pass

        try:
            property_index = querylist.index('propertyid')
            propertyid = querylist[property_index + 1]
            all_spaces = all_spaces.filter(space_property_id=propertyid)
        except Exception as e:
            pass
        spaces = SpaceSerializer(instance=all_spaces, nested_plant=True,
                                 nest_level=request.GET.get('nest_level', 'spaces'),
                                 many=True)
        return Response(spaces.data, status=HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = SpaceSerializer(data=data, partial=True)
        if serializer.is_valid():
            instance = serializer.create(serializer.validated_data)
            instance.save()
            spaces = SpaceSerializer(instance=instance, nested_plant=True, many=False)
            return Response(spaces.data, status=HTTP_200_OK)
        else:
            return Response('Internal error or malformed JSON', status=HTTP_400_BAD_REQUEST)


class SpaceDetailView(APIView):
    def get(self, request, spaceid):
        all_spaces = getSpacesOfUser(request.user)
        try:
            space = all_spaces.get(space_id=spaceid)
        except ObjectDoesNotExist as e:
            return Response("That space doesn't even exist, fool", status=HTTP_400_BAD_REQUEST)
        space = SpaceSerializer(instance=space, nested_plant=True,
                                nest_level=request.GET.get('nest_level', 'spaces'),
                                many=False)
        return Response(space.data, status=HTTP_200_OK)

    def put(self, request, spaceid):
        try:
            space = Space.objects.get(space_id=spaceid)
        except ObjectDoesNotExist as e:
            return Response("That space doesn't even exist, fool", status=HTTP_400_BAD_REQUEST)
        else:
            instance = space
            data = JSONParser().parse(request)
            serializer = SpaceSerializer(data=data, partial=True)
            if serializer.is_valid():
                for attr, value in serializer.validated_data.items():
                    if attr != 'space_id':
                        setattr(instance, attr, value)
                instance.save()
                space = SpaceSerializer(instance=instance, nested_plant=True, many=False)
                return Response(space.data, status=HTTP_200_OK)
            else:
                return Response('Internal error or malformed JSON', status=HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, spaceid):
        try:
            space = Space.objects.get(space_id=spaceid)
        except ObjectDoesNotExist:
            return Response("That space doesn't even exist, fool", status=HTTP_400_BAD_REQUEST)
        space.delete()
        return Response('Space deleted', status=HTTP_200_OK)


class SpaceRestrictionsListView(APIView):
    def get(self, request, spaceid):
        all_spaces = getSpacesOfUser(request.user)
        try:
            space = all_spaces.get(space_id=spaceid)
        except ObjectDoesNotExist as e:
            return Response("That space doesnt belong to you!", status=HTTP_400_BAD_REQUEST)

        timeRes = TimeRestriction.objects.filter(time_restriction_space=spaceid)
        serializer = TimeRestrictionSerializer(list(timeRes), many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request, spaceid):
        data = JSONParser().parse(request)
        serializer = TimeRestrictionSerializer(data=data, partial=True)
        if serializer.is_valid():
            instance = serializer.create(serializer.validated_data)
            instance.space_id = spaceid
            instance.save()
            spaces = TimeRestrictionSerializer(instance, many=False)
            return Response(spaces.data, status=HTTP_200_OK)
        else:
            return Response('Internal error or malformed json ', status=HTTP_500_INTERNAL_SERVER_ERROR)


class SpaceRestrictionDetailView(APIView):
    def get(self, request, spaceid, resid):
        try:
            timeRes = TimeRestriction.objects.get(time_restriction_id=resid)
        except ObjectDoesNotExist as e:
            return Response('The specified time restriction doesnt exist for that space', status=HTTP_400_BAD_REQUEST)
        serializer = TimeRestrictionSerializer(timeRes, many=False)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, spaceid, resid):
        data = JSONParser().parse(request)
        serializer = TimeRestrictionSerializer(data=data, partial=True)
        if serializer.is_valid():
            try:
                instance = TimeRestriction.objects.get(time_restriction_id=resid)
            except Exception as e:
                return Response('Especify the correct restriction id', status=HTTP_400_BAD_REQUEST)
            for attr, value in serializer.validated_data.items():
                if attr != 'time_restriction_id' and attr != 'space_id':
                    setattr(instance, attr, value)
            instance.save()
            spaces = TimeRestrictionSerializer(instance, many=False)
            return Response(spaces.data, status=HTTP_200_OK)
        else:
            return Response('Internal error or malformed json ', status=HTTP_400_BAD_REQUEST)

    def delete(self, request, spaceid, resid):
        try:
            time = TimeRestriction.objects.filter(time_restriction_id=resid, time_restriction_space=spaceid)
        except ObjectDoesNotExist:
            return Response("That restriction doesn't even exist, fool", status=HTTP_400_BAD_REQUEST)
        if len(time) > 0:
            time.delete()
            return Response('restriction deleted', status=HTTP_200_OK)
        return Response("That restriction doesn't even exist for that space, fool", status=HTTP_400_BAD_REQUEST)
