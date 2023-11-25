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
