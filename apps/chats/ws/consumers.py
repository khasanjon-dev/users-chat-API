from datetime import datetime

import ujson
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.db.models import Q
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

from chats.models import ChatPersonal, BlockList
from users.models import User


class BaseAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
    @classmethod
    async def decode_json(cls, text_data):
        return ujson.loads(text_data)

    @classmethod
    async def encode_json(cls, content):
        return ujson.dumps(content)

    async def receive(self, text_data=None, bytes_data=None, **kwargs) -> dict | None:
        try:
            return await self.receive_json(await self.decode_json(text_data))
        except Exception as e:
            print(e)
            context = {
                'message': "Json malumotni to'g'ri yuboring"
            }
            await self.send_json(context)
            return


class ChatConsumer(BaseAsyncJsonWebsocketConsumer):
    room_group_name = 'group'
    __format_data = '%Y-%m-%d %H-%M-%S'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.file_id = None
        self.from_user = None

    async def user_update_notify(self, from_user, is_notify: bool) -> None:
        await self.update_user_status(from_user, is_notify)
        await self.notify_user_status(is_notify)

    @database_sync_to_async
    def update_message_status(self, chat_id) -> None:
        if isinstance(chat_id, list):
            ChatPersonal.objects.filter(id=chat_id).update(is_read=True)
        else:
            ChatPersonal.objects.filter(id=chat_id).update(is_read=True)

    @database_sync_to_async
    def is_blocked(self, blocker, user) -> bool:
        return BlockList.objects.filter(blocker=blocker, user=user).exists()

    @database_sync_to_async
    def check_user_chat(self, to_user, from_id) -> bool:
        return ChatPersonal.objects.filter(
            Q(receiver=to_user) & Q(sender=from_id) | Q(receiver=from_id) & Q(sender=to_user)
        ).exists()

    @database_sync_to_async
    def update_user_status(self, user, is_online=False) -> None:
        user.is_online = is_online
        user.save()
        print(f"{user.first_name} -- {'online' if is_online else 'offline'}")

    @database_sync_to_async
    def get_name(self, from_user_id: int, to_user_id: int, msg: str) -> tuple:
        if not User.objects.filter(pk=to_user_id).exists():
            return None, True
        try:
            data = {
                'sender_id': from_user_id,
                'receiver_id': to_user_id,
                'message': msg
            }
            chat = ChatPersonal.objects.create(**data)
        except Exception as e:
            print('Xatolik', str(e))
            return None, True
        return chat, False

    async def connect(self) -> None:
        self.from_user = self.scope['user']
        self.file_id = None

        if not self.from_user.pk:
            await self.accept()
            context = {
                'message': 'JWT bilan kiring'
            }
            await self.send_json(context)
            return
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.user_update_notify(self.from_user, True)

    async def notify_user_status(self, is_online: bool) -> None:
        context = {
            'type': 'chat.change.status',
            'user_id': self.from_user.id,
            'is_online': is_online,
            'sender_channel_name': self.channel_name
        }
        await self.channel_layer.group_send(
            self.room_group_name,
            context
        )

    async def disconnect(self, close_code) -> None:
        if self.from_user.is_authenticated:
            await self.user_update_notify(self.from_user, False)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def chat_change_status(self, event) -> None:
        if self.from_user.pk != event['user_id'] and await self.check_user_chat(self.from_user.id, event['user_id']):
            data = {
                'type': 'status',
                'is_online': event['is_online'],
                'user_id': event['user_id']
            }
            await self.send_json(data)
            return

    async def receive_json(self, text_data_json) -> None:
        if not text_data_json.get('type'):
            context = {
                'message': 'type is required!'
            }
            await self.send_json(context)
            return
        if (msg_type := text_data_json.get('type')) == 'message':
            message = text_data_json.get('message')
            to_user_id = text_data_json.get('chat_id')
            if not to_user_id:
                context = {
                    'message': 'xabar borishi kerak bolgan userni kiriting'
                }
                await self.send_json(context)
                return
            self.file_id = text_data_json.get('file_id')

            # if sender equal to receiver then return
            if self.from_user.pk == to_user_id:
                return

            # if sender equal to receiver then return
            if await self.is_blocked(self.from_user.pk, to_user_id):
                context = {
                    'status': 'blocked',
                    'message': 'Xabar yubora olmaysiz!'
                }
                await self.send_json(context)
                return
            chat, error = await self.get_name(self.from_user.id, to_user_id, message)
            if error:
                context = {
                    'message': 'user xato'
                }
                await self.send_json(context)
                return
            created_date = datetime.strftime(chat.created_at, self.__format_data)

            data = {
                'type': 'chat.message',
                'message': message,
                'message_id': chat.id,
                'from_user_id': self.from_user.id,
                'chat_id': chat.id,
                'to_user_id': to_user_id,
                'file_id': self.file_id,
                'created_date': created_date,
                'sender_channel_name': self.channel_name
            }
            await self.channel_layer.group_send(
                self.room_group_name,
                data
            )
        elif msg_type == 'read_message':
            message_id = text_data_json['read_message_id']
            await self.update_message_status(message_id)

    async def chat_message(self, event):
        if self.from_user.pk == event['to_user_id'] or self.from_user.pk == event['from_user_id']:
            data = {
                'type': 'message',
                'from_chat_id': event['from_user_id'],
                'message_id': event['message_id'],
                'message': event['message'],
                'created_date': event['created_date']
            }
            if file_id := event.get('file_id'):
                data['file_id'] = file_id
            await self.send_json(data)
            if self.from_user.pk == event['to_user_id']:
                await self.send_message_notification(self.from_user.pk, event['message'])
            return

    @database_sync_to_async
    def send_message_notification(self, user_id: int, msg: str):
        device = FCMDevice.objects.filter(user_id=user_id).first()
        if device:
            device.send_message(Message(
                notification=Notification(title='Websocket chatdan xabar', body=msg)
            ))
