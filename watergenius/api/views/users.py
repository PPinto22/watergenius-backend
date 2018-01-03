from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from api.models import *
from api.serializers.users import UserCreateSerializer, UserSerializer


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
        serializer = UserSerializer(data=data, partial=True)
        print(serializer.is_valid())
        # assuming that serializer is valid. TODO
        # TODO - Acertar isto
        if serializer.data['email'] == user.email:
            user.first_name = serializer.data['first_name']
            user.last_name = serializer.data['last_name']
            user.is_superuser = serializer.data['is_superuser']
            user.save()
            return Response(serializer.data, status=HTTP_202_ACCEPTED)

    def delete(self, request, mail):
        user = User.objects.get(email=mail)
        print(user)
        if user:
            user.delete()
            return JsonResponse('OK', status=HTTP_204_NO_CONTENT, safe=False)
        return Response(status=HTTP_400_BAD_REQUEST)