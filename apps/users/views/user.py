from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.models import User
from users.serializers import UserModelSerializer, RegisterModelSerializer, UpdateModelSerializer


class UserViewSet(ListModelMixin, GenericViewSet):
    """
    userlar listini olish

    ```
    """
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    @action(methods=['post'], detail=False, serializer_class=RegisterModelSerializer)
    def register(self, request):
        """
        user register qilish uchun

        ```
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False, permission_classes=(IsAuthenticated,))
    def about(self, request):
        """
        user ma'lumotlarini olish uchun

        ```
        """
        user = User.objects.get(pk=request.user.id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(methods=['put'], detail=False, permission_classes=(IsAuthenticated,),
            serializer_class=UpdateModelSerializer, url_path='update')
    def update_user(self, request):
        """
        user ma'lumotlarini yangilash

        ```
        {
          "first_name": "John",
          "last_name": "Doe",
          "bio": "keep learning",
          "image": image_file
        }
        ```
        """
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                User.objects.filter(pk=request.user.id).update(**serializer.data)
                user = User.objects.get(pk=request.user.id)
                serializer = UserModelSerializer(user)
                return Response(serializer.data)
        except Exception as e:
            context = {
                'error': str(e)
            }
            return Response(context, status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], detail=False, permission_classes=(IsAuthenticated,))
    def change_username(self, request):
        """
        username o'zgartirish

        ```
        """
        pass
