from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

import api.serializers
from api.serializers import *


class RegisterView(APIView):
    # TODO - Registar admin: verificar se is_admin = True
    permission_classes = [AllowAny]
    def post(self, request):
        data = JSONParser().parse(request)
        user_ser = UserCreateSerializer(data=data)
        # Email unico validado aqui
        user_ser.is_valid(raise_exception=True)
        user = user_ser.create(user_ser.validated_data)
        user.set_password(user.password)
        user.save()
        return Response(UserSerializer(user).data)


class UserView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = api.serializers.UserSerializer(users, many=True)
        return Response(serializer.data)


# TODO - Testar se tudo daqui para baixo ainda funciona depois de eu ter andado a mexer na autenticacao.
# TODO - Passar para class views ?
def usersMail(request, mail=None):
    if request.method == 'GET':
        #data = JSONParser().parse(request)
        user = User.objects.get(user_email=mail)
        serializer = api.serializers.UserSerializer(user, many=False)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        #editar user
        user = User.objects.get(user_email=mail)
        data = JSONParser().parse(request)
        serializer = api.serializers.UserSerializer(data=data, partial=True)
        print(serializer.is_valid())
        # assuming that serializer is valid. TODO 
        if serializer.data['user_email']==user.email:
            user.name = serializer.data['user_name']
            user.admin = serializer.data['user_admin']
            user.save()
            return JsonResponse(serializer.data, status=201)
    elif request.method == 'DELETE':
        user = User.objects.get(user_email=mail)
        print(user)
        if user:
            user.delete()
            return JsonResponse( 'OK', status=200, safe=False)


    return JsonResponse(serializer.errors, status=400)

def properties(request):
    print (request.user)
    if request.user.is_authenticated:
        username = request.user.email
        print('ulha o user')
        print(username)
    if request.method == 'GET':
        #data = JSONParser().parse(request)
        prop = Property.objects.filter(prop_owner_id=username)
        serializer = api.serializers.PropertySerializer(prop, many=True)
        return JsonResponse(serializer.data , status=200 ,safe=False)

    elif request.method == 'PUT':
        print ('iii')

    return JsonResponse('error', status=400, safe=False)

def spaces(request):
    if request.method == 'GET':
        props = Property.objects.filter(prop_owner_id=request.user.email)
        #serializer = PropertySerializer(prop, many=True)
        queryset = Space.objects.filter(space_property__in=props.values('prop_id'))
        print(list(queryset))
        spaces = api.serializers.SpaceSerializer(list(queryset), many=True)
        return JsonResponse( spaces.data, status=200 ,safe=False)
    elif request.method == 'PUT':
        print ('iii')

    return JsonResponse('error', status=400, safe=False)


def plants(request):
    if request.method == 'GET':
        plants = PlantType.objects.all()
        serializer = api.serializers.PlantTypeSerializer(plants, many=True)
        return JsonResponse( serializer.data, status=200 ,safe=False)
    elif request.method == 'PUT':
        print ('iii')

    return JsonResponse('error', status=400, safe=False)

def subspaces(request, spaceid=None):
    if request.method == 'GET':
        print(spaceid)
        #data = JSONParser().parse(request)
        #serializer = SpaceSerializer(data=data,partial=True)
        plants = SubSpace.objects.filter(sub_space_id=spaceid)
        serialize = api.serializers.SubSpaceSerializer(plants, many=True)
        return JsonResponse( serialize.data, status=200 ,safe=False)
    elif request.method == 'PUT':
        print ('iii')


    return JsonResponse('error', status=400, safe=False)

def plans(request):
    if request.method == 'GET':
        print(request.META['QUERY_STRING'])
        query = (request.META['QUERY_STRING']).split('=')
        if query[0] == 'subspace':
            subspaceid = (query[1])
            dayplans = DayPlan.objects.filter(dayplan_sub=subspaceid)
        #data = JSONParser().parse(request)
        #serializer = SpaceSerializer(data=data,partial=True)
        #plants = SubSpace.objects.filter(sub_space_id=spaceid)
        serialize = api.serializers.DayPlanSerializer(dayplans, many=True)
        return JsonResponse( serialize.data , status=200 ,safe=False)
    elif request.method == 'PUT':
        print ('iii')


    return JsonResponse('error', status=400, safe=False)









