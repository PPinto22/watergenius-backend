from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from users.models import User,Property
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from users.serializers import UserSerializer,PropertySerializer
from urllib.parse import urlparse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login , logout
from watergenius_api.authbackend import SettingsBackend
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
                us = User.objects.get(user_email='pinto@gmail.com')
                user = SettingsBackend.authenticate(username=username, password=password)
                #print(user)
                print(us)
                login(request, us)
                return HttpResponse('success', status=200)

    return HttpResponse('xua')


#@login_required
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

#@login_required
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
        print('ao poste')
        print(user)
        print(serializer)
        print(serializer.is_valid())
        # assuming that serializer is valid. TODO 
        if serializer.data['user_email']==user.user_email:
            print('igualzinho crl')
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
    if request.method == 'GET':
        #data = JSONParser().parse(request)
        prop = Property.objects.all()
        serializer = PropertySerializer(prop, many=True)
        return JsonResponse(serializer.data , status=200 ,safe=False)

    elif request.method == 'PUT':
        print ('iii')

    return JsonResponse('error', status=400, safe=False)







