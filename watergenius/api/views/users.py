from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.users import User, UserCreateSerializer, UserSerializer


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
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


def userByMail(request, mail=None):
    if request.method == 'GET':
        # data = JSONParser().parse(request)
        user = User.objects.get(email=mail)
        serializer = UserSerializer(user, many=False)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        # editar user
        user = User.objects.get(email=mail)
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data, partial=True)
        print(serializer.is_valid())
        # assuming that serializer is valid. TODO
        if serializer.data['email'] == user.email:
            user.name = serializer.data['name']
            user.admin = serializer.data['admin']
            user.save()
            return JsonResponse(serializer.data, status=201)
    elif request.method == 'DELETE':
        user = User.objects.get(email=mail)
        print(user)
        if user:
            user.delete()
            return JsonResponse('OK', status=200, safe=False)

    return JsonResponse(serializer.errors, status=400)