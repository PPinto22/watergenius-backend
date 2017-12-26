from rest_framework import serializers

from api.users.models import User, UserManagesProperty


class UserLoginSerializer(serializers.BaseSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=50)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'is_superuser')
        validators = []  # Remove a default "unique together" constraint.


# TODO - validar email com regex
class UserCreateSerializer(serializers.ModelSerializer):
    is_superuser = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'is_superuser')
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def create(self, validated_data):
        return User(**validated_data)


class UserManagesPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserManagesProperty
        fields = ('user_id', 'prop_id')
        validators = []  # Remove a default "unique together" constraint.
