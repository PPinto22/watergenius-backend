from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *

from api.models import Property
from api.models.spaces import Space, TimeRestrition
from api.serializers.spaces import SpaceSerializer, TimeRestritionSerializer


class SpacesListView(APIView):
    def get(self, request):
        props = Property.objects.filter(prop_owner_id=request.user.email)
        queryset = Space.objects.filter(space_property__in=props.values('prop_id'))
        spaces = SpaceSerializer(queryset, many=True)
        return Response(spaces.data, status=HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = SpaceSerializer(data=data, partial=True)
        if serializer.is_valid():
            instance = serializer.create(serializer.validated_data)
            instance.save()
            return Response('Space created', status=HTTP_200_OK)
        else:
            return Response('Internal error or malformed JSON', status=HTTP_400_BAD_REQUEST)

class SpaceDetailView(APIView):
    def get(self, request, spaceid):
        try:
            space = Space.objects.get(space_id=spaceid)
        except ObjectDoesNotExist as e:
            return Response("That space doesn't even exist, fool", status=HTTP_400_BAD_REQUEST)
        spaces = SpaceSerializer(space, many=False)
        return Response(spaces.data, status=HTTP_200_OK)

    def put(self, request, spaceid):
        try:
            space = Space.objects.get(space_id=spaceid)
        except ObjectDoesNotExist as e:
            return Response("That space doesn't even exist, fool", status=HTTP_400_BAD_REQUEST)
        else:
            instance = Space()
            data = JSONParser().parse(request)
            serializer = SpaceSerializer(data=data, partial=True)
            if serializer.is_valid():
                for attr, value in serializer.validated_data.items():
                    if attr != 'space_id':
                        setattr(instance, attr, value)
                instance.save()
                return Response('Space updated', status=HTTP_200_OK)
            else:
                return Response('Internal error or malformed JSON', status=HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, spaceid):
        try:
            space = Space.objects.get(space_id=spaceid)
        except ObjectDoesNotExist:
            return Response("That space doesn't even exist, fool", status=HTTP_400_BAD_REQUEST)
        space.delete()
        return Response('Space deleted', status=HTTP_204_NO_CONTENT)

class SpaceRestrictionsListView(APIView):
    def get(self, request, spaceid):
        timeRes = TimeRestrition.objects.filter(time_restrition_space=spaceid)
        serializer = TimeRestritionSerializer(list(timeRes), many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request, spaceid):
        data = JSONParser().parse(request)
        serializer = TimeRestritionSerializer(data=data, partial=True)
        if serializer.is_valid():
            instance = serializer.create(serializer.validated_data)
            instance.space_id = spaceid
            instance.save()
            return Response('OK', status=HTTP_200_OK)
        else:
            return Response('Internal error or malformed json ', status=HTTP_500_INTERNAL_SERVER_ERROR)

class SpaceRestrictionDetailView(APIView):
    def get(self, request, spaceid, resid):
        try:
            timeRes = TimeRestrition.objects.get(time_restrition_id=resid)
        except ObjectDoesNotExist as e:
            return Response('The specified time restrition doesnt exist for that space', status=HTTP_400_BAD_REQUEST)
        serializer = TimeRestritionSerializer(timeRes, many=False)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, spaceid, resid):
        data = JSONParser().parse(request)
        serializer = TimeRestritionSerializer(data=data, partial=True)
        if serializer.is_valid():
            try:
                instance = TimeRestrition.objects.get(time_restrition_id=resid)
            except Exception as e:
                return Response('Especify the correct restrition id', status=HTTP_400_BAD_REQUEST)
            for attr, value in serializer.validated_data.items():
                if attr != 'time_restrition_id' and attr != 'space_id':
                    print(attr)
                    setattr(instance, attr, value)
            instance.save()
            return Response('Time restrition edited with success', status=HTTP_200_OK)
        else:
            return Response('Internal error or malformed json ', status=HTTP_400_BAD_REQUEST)

    def delete(self, request, spaceid, resid):
        try:
            time = TimeRestrition.objects.filter(time_restrition_id=resid, time_restrition_space=spaceid)
        except ObjectDoesNotExist:
            return Response("That restrition doesn't even exist, fool", status=HTTP_400_BAD_REQUEST)
        if len(time) > 0:
            time.delete()
            return Response('restrition deleted', status=HTTP_204_NO_CONTENT)
        return Response("That restrition doesn't even exist for that space, fool", status=HTTP_400_BAD_REQUEST)