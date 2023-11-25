from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.models import User
from users.serializers import UserModelSerializer, RegisterModelSerializer


class UserViewSet(ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    @action(methods=['post'], detail=False, serializer_class=RegisterModelSerializer)
    def register(self, request):
        """
        userlarni register qilish uchun

        ```
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status.HTTP_201_CREATED)
