from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from api.models import *
from api.serializers.users import UserCreateSerializer, UserSerializer, UserUpdateSerializer


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
        return Response(UserSerializer(user).data, HTTP_200_OK)


class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserDetailView(APIView):
    def get(self, request, mail):
        user = User.objects.get(email=mail)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, mail):
        user = User.objects.get(email=mail)
        data = JSONParser().parse(request)
        serializer = UserUpdateSerializer(data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        if 'email' in serializer.validated_data and \
                user.email != serializer.validated_data['email']:
            return Response('Cannot change email', status=HTTP_400_BAD_REQUEST)
        for attr, value in serializer.validated_data.items():
            if attr == 'password':
                user.set_password(serializer.validated_data['password'])
            setattr(user, attr, value)
        user.save()
        out_serializer = UserSerializer(user)
        return Response(out_serializer.data, status=HTTP_200_OK)

    def delete(self, request, mail):
        user = User.objects.get(email=mail)
        print(user)
        if user:
            user.delete()
            return JsonResponse('OK', status=HTTP_200_OK, safe=False)
        return Response(status=HTTP_400_BAD_REQUEST)