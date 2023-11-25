from rest_framework.serializers import ModelSerializer

from users.models import User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'last_login',
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',
            'updated_at',
            'date_joined',
            'image'
        )
