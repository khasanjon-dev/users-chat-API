from rest_framework.serializers import ModelSerializer

from chats.models import ChatPersonal, BlockList
from users.serializers.user import UserChatInfoSerializer


class ChatPersonalSerializer(ModelSerializer):
    sender = UserChatInfoSerializer()
    receiver = UserChatInfoSerializer()

    class Meta:
        model = ChatPersonal
        fields = (
            'id',
            'sender',
            'receiver',
            'message',
            'is_read',
            'is_edited',
            'created_at'
        )


class ChatPersonalUpdateSerializer(ModelSerializer):
    class Meta:
        model = ChatPersonal
        fields = (
            'id',
            'message',
            'is_edited'
        )


class BlockUserListModelSerializer(ModelSerializer):
    class Meta:
        model = BlockList
        fields = (
            'id',
            'blocker',
            'user'
        )
