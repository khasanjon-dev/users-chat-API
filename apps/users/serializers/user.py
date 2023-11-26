from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from shared.django.upload_images import upload_image
from users.models import User


class MainSerializer(Serializer):
    @staticmethod
    def get_user_by_username(username: str):
        user = User.objects.get(username=username)
        return user


class UserModelSerializer(ModelSerializer):
    image = serializers.URLField()

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


class UpdateModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'bio',
            'image'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context['request']
        if image := request.data.get('image', None):
            image_url = upload_image(image.read())
            data['image'] = image_url
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data
