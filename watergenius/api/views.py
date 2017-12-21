from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from api.models import User,Property, Space , PlantType , SubSpace , DayPlan
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from api.serializers import UserSerializer,PropertySerializer, SpaceSerializer , PlantTypeSerializer , SubSpaceSerializer, DayPlanSerializer
from urllib.parse import urlparse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login , logout
from watergenius.authbackend import SettingsBackend
import base64


def logout_view(request):
    auth = request.META['HTTP_AUTHORIZATION'].split()
    if len(auth) == 2:
        #x = User.create_user('pinto@gmail.com', 'pinto')
        #User.create_user(email='pinto@gmail.com', password='pinto' , username="pinto" )
        if auth[0].lower() == "basic":
            username, password = base64.b64decode(auth[1]).decode('utf-8').split(':', 1)
            passwd = base64.b64encode(base64.b64encode(password.encode('utf-8')))
            logout(request)
            return HttpResponse('success', status=200)



def login_view(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            #x = User.create_user('pinto@gmail.com', 'pinto')
            #User.create_user(email='pinto@gmail.com', password='pinto' , username="pinto" )
            if auth[0].lower() == "basic":
                username, password = base64.b64decode(auth[1]).decode('utf-8').split(':', 1)
                passwd = base64.b64encode(base64.b64encode(password.encode('utf-8')))
                print(passwd)
                print(username)
                print(password)
                us = User.objects.get(user_email=username)
                user = SettingsBackend.authenticate(username=username, password=password)
                #print(user)
                print(us)
                login(request, us)
                return HttpResponse('success', status=200)

    return HttpResponse('authentication needed', status=204)


@login_required
def usersNormal(request):
    print('normal \n \n ')
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        #inserir user
        print(request)
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
    
    return JsonResponse(serializer.errors, status=400)

@login_required
def usersMail(request, mail=None):
    if request.method == 'GET':
        #data = JSONParser().parse(request)
        user = User.objects.get(user_email=mail)
        serializer = UserSerializer(user, many=False)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        #editar user
        user = User.objects.get(user_email=mail)
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data,partial=True)
        print(serializer.is_valid())
        # assuming that serializer is valid. TODO 
        if serializer.data['user_email']==user.user_email:
            user.user_name = serializer.data['user_name']
            user.user_admin = serializer.data['user_admin']
            user.save()
            return JsonResponse(serializer.data, status=201)
    elif request.method == 'DELETE':
        user = User.objects.get(user_email=mail)
        print(user)
        if user:
            user.delete()
            return JsonResponse( 'OK', status=200, safe=False)


    return JsonResponse(serializer.errors, status=400)

@login_required
def properties(request):
    print (request.user)
    if request.user.is_authenticated:
        username = request.user.user_email
        print('ulha o user')
        print(username)
    if request.method == 'GET':
        #data = JSONParser().parse(request)
        prop = Property.objects.filter(prop_owner_id=username)
        serializer = PropertySerializer(prop, many=True)
        return JsonResponse(serializer.data , status=200 ,safe=False)

    elif request.method == 'PUT':
        print ('iii')

    return JsonResponse('error', status=400, safe=False)

@login_required
def spaces(request):
    if request.method == 'GET':
        props = Property.objects.filter(prop_owner_id=request.user.user_email)
        #serializer = PropertySerializer(prop, many=True)
        queryset = Space.objects.filter(space_property__in=props.values('prop_id'))
        print(list(queryset))
        spaces = SpaceSerializer(list(queryset), many=True)
        return JsonResponse( spaces.data, status=200 ,safe=False)
    elif request.method == 'PUT':
        print ('iii')


    return JsonResponse('error', status=400, safe=False)


@login_required
def plants(request):
    if request.method == 'GET':
        plants = PlantType.objects.all()
        serializer = PlantTypeSerializer(plants, many=True)
        return JsonResponse( serializer.data, status=200 ,safe=False)
    elif request.method == 'PUT':
        print ('iii')

    return JsonResponse('error', status=400, safe=False)

@login_required
def subspaces(request, spaceid=None):
    if request.method == 'GET':
        print(spaceid)
        #data = JSONParser().parse(request)
        #serializer = SpaceSerializer(data=data,partial=True)
        plants = SubSpace.objects.filter(sub_space_id=spaceid)
        serialize = SubSpaceSerializer(plants, many=True)
        return JsonResponse( serialize.data, status=200 ,safe=False)
    elif request.method == 'PUT':
        print ('iii')


    return JsonResponse('error', status=400, safe=False)

@login_required
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
        serialize = DayPlanSerializer(dayplans, many=True)
        return JsonResponse( serialize.data , status=200 ,safe=False)
    elif request.method == 'PUT':
        print ('iii')


    return JsonResponse('error', status=400, safe=False)









