from django.db.models import ForeignKey, CASCADE, TextField, BooleanField

from shared.django.models import BaseModel
from users.models import User


class BlockList(BaseModel):
    # relationships
    blocker = ForeignKey(User, CASCADE, 'blocker')
    user = ForeignKey(User, CASCADE, 'user')


class ChatPersonal(BaseModel):
    message = TextField()
    # relationships
    sender = ForeignKey(User, CASCADE, 'sender')
    receiver = ForeignKey(User, CASCADE, 'receiver')
    # bool
    is_read = BooleanField(default=False)
    is_edited = BooleanField(default=False)

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chatlar'  # noqa

    def __str__(self):
        return f'{self.sender.first_name} {self.receiver.first_name} {self.message}'
