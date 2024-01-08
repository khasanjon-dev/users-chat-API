from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin

from chats.filter import ChatFilter
from chats.models import ChatPersonal, BlockList
from chats.serializers.chat import ChatPersonalSerializer, ChatPersonalUpdateSerializer, BlockUserListModelSerializer
from shared.django.serializers import NoneSerializer
from shared.rest_framework.pagination import PageNumberPagination
from users.serializers.user import UserSerializer


class ChatPersonalViewSet(ViewSetMixin, RetrieveUpdateDestroyAPIView):
    queryset = ChatPersonal.objects.order_by('-created_at')
    serializer_class = ChatPersonalSerializer
    pagination_class = PageNumberPagination
    lookup_url_kwarg = 'pk'

    filter_backends = [DjangoFilterBackend]
    filterset_class = ChatFilter
    http_method_names = ('get', 'post', 'patch', 'delete')

    def retrieve(self, request, *args, **kwargs):
        '''
        Aynana 1 userga tegishli bo'lgan barcha xabarlarni olish

        ```
        '''
        pk = kwargs.get('pk')
        user = request.user
        queryset = ChatPersonal.objects.filter(
            Q(receiver=user) & Q(sender=pk) |
            Q(receiver=pk) & Q(sender=user)
        ).order_by('-created_at')

        queryset.update(is_read=True)

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        '''
        Xabarni tahrirlash uchun

        ```
        '''
        sender = request.user
        msg = ChatPersonal.objects.filter(sender=sender, pk=kwargs.get('pk')).first()
        if msg:
            msg.is_edited = True
            msg.save()
            return super().partial_update(request, *args, **kwargs)
        payload = {
            'message': 'Bu xabar boshqasiga tegishli !'
        }
        return Response(payload, status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        '''
        Xabarni o'chirish uchun

        ```
        '''
        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return ChatPersonalUpdateSerializer
        return self.serializer_class

    @action(['get'], False, 'user-chat-list')
    def user_list(self, request, *args, **kwargs):
        '''
        oldin yozishgan userlar ro'yxatini olish

        ```
        '''
        user = request.user
        chats = sorted(ChatPersonal.objects.filter(Q(receiver=user) | Q(sender=user)).distinct('sender', 'receiver'),
                       key=lambda i: i.created_at, reverse=True)
        user_list = []
        for chat in chats:
            if not (chat.sender in user_list or chat.receiver in user_list):
                if chat.sender != user:
                    user_list.append(chat.sender)
                else:
                    user_list.append(chat.receiver)
        serializer = UserSerializer(user_list, many=True, context={'request': request})
        return Response(serializer.data)

    @action(['get'], False, 'block-list', 'block_list', serializer_class=BlockUserListModelSerializer,
            filterset_class=None)
    def blocked_user_list(self, request):
        '''
        block qilgan userlar listi

        ```
        user1 -> user2
        is_block: user1
        user1 - user2 ni blocklaganini bildiradi
        ```
        '''
        block_users = request.user.blocker.all()
        serializer = self.serializer_class(block_users, many=True)
        return Response(serializer.data)

    @action(['post'], True, 'update-block', serializer_class=NoneSerializer, filterset_class=None)
    def update_block_user(self, request, pk):
        '''
        user block qilish yokida unblock qilish

        ```
        '''
        user, created = BlockList.objects.get_or_create(blocker=request.user, user_id=pk)
        if created:
            context = {'message': 'user is blocked'}
            return Response(context)
        else:
            user.delete()
            context = {'message': 'user is unblocked'}
            return Response(context)

    @action(['delete'], True, 'delete-chat-list', filterset_class=None)
    def delete_chat_list(self, request, pk):
        '''
        user ga tegishli barcha xabarlarni o'chirish

        ```
        '''
        user = request.user
        ChatPersonal.objects.filter(
            Q(receiver=user) & Q(sender=pk) |
            Q(receiver=pk) & Q(sender=user)
        ).delete()
        context = {'message': 'success'}
        return Response(context, status.HTTP_204_NO_CONTENT)
