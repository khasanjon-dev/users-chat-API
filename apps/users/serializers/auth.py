from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer

from users.models import User


class RegisterModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'email',
            'username',
            'password'
        )

    def validate(self, attrs):
        password = make_password(attrs['password'])
        attrs['password'] = password
        return attrs
