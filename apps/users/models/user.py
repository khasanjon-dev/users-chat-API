from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, DateTimeField


class User(AbstractUser):
    last_name = CharField(max_length=150, null=True, blank=True)
    # date
    updated_at = DateTimeField(auto_now=True, null=True)
    date_joined = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_full_name()
