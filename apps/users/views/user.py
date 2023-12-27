from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from shared.django.emails import send_email_link, get_one_time_link
from shared.tokens import reset_password_token, activate_token
from users.models import User
from users.serializers import UserModelSerializer, RegisterModelSerializer, UpdateModelSerializer, \
    ChangeUsernameSerializer, ChangePasswordSerializer, EmailSerializer
from users.serializers.user import SendEmailTestSerializer


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
        user register qilish

        ```
        """
        try:
            with transaction.atomic():
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                email = serializer.data.get('email')
                user = get_object_or_404(User, email=email)
                token = activate_token.make_token(user)
                link = get_one_time_link(request, user, 'activate', token)
                send_email_link(user.email, 'Activate email', link)
                return Response(serializer.data, status.HTTP_201_CREATED)
        except Exception as e:
            context = {
                'message': str(e)
            }
            return Response(context, status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, permission_classes=(IsAuthenticated,))
    def about(self, request):
        """
        user ma'lumotlarini olish uchun

        ```
        """
        user = User.objects.get(pk=request.user.id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(methods=['patch'], detail=False, permission_classes=(IsAuthenticated,),
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

    @action(methods=['post'], detail=False, permission_classes=(IsAuthenticated,),
            serializer_class=ChangeUsernameSerializer, url_path='change-username')
    def change_username(self, request):
        """
        username o'zgartirish

        ```
        {
            "username": "hello"
        }
        ```
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(pk=request.user.id)
            user.username = serializer.data['username']
            user.save()
            serializer = UserModelSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            context = {
                'message': str(e)
            }
            return Response(context, status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, permission_classes=(IsAuthenticated,),
            serializer_class=ChangePasswordSerializer, url_path='change-password')
    def change_password(self, request):
        """
        password ni o'zgartirish

        ```
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                user = User.objects.get(pk=request.user.id)
                user.password = serializer.data.get('new_password')
                user.save()
                context = {
                    'message': "Parol o'zgartirildi!"
                }
                return Response(context)
        except Exception as e:
            context = {
                'message': str(e)
            }
            return Response(context, status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, serializer_class=EmailSerializer, url_path='reset-password')
    def reset_password_send_link_email(self, request):
        """
        password ni qayta tiklash uchun emailga link yuborish

        ```
        {
            "email": "devmasters.uz@gmail.com"
        }
        ```
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, email=serializer.data['email'])
        token = reset_password_token.make_token(user)
        link = get_one_time_link(request, user, 'reset-password', token)
        try:
            send_email_link(user.email, 'Reset Password', link)
            context = {
                'message': 'Pochtaga parol qayta tiklash linki yuborildi',
                'link': link
            }
            return Response(context)
        except Exception as e:
            context = {
                'message': str(e),
                'link': link
            }
            return Response(context, status.HTTP_400_BAD_REQUEST)

    @action(['post'], False, 'send-email', serializer_class=SendEmailTestSerializer)
    def send_email_message_test(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, email=serializer.data['email'])
        token = reset_password_token.make_token(user)
        link = get_one_time_link(request, user, 'reset-password', token)
        send_email_link(user.email, 'Reset Password', link)
        context = {
            'message': 'Pochtaga parol qayta tiklash linki yuborildi',
            'link': link
        }
        return Response(context)
