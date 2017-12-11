from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from users.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from users.serializers import UserSerializer


def usersNormal(request):
    print('normal \n \n ')
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        print(request)
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
    
    return JsonResponse(serializer.errors, status=400)


def usersMail(request):
    if request.method == 'GET':
        #data = JSONParser().parse(request)
        current_url = request.resolver_match.url_name
        print(current_url)
        return HttpResponse('tachoooo')
    return JsonResponse(serializer.errors, status=400)