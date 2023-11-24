from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, DateTimeField, ImageField


class User(AbstractUser):
    last_name = CharField(max_length=150, null=True, blank=True)
    bio = CharField(max_length=250, null=True, blank=True)
    # date
    updated_at = DateTimeField(auto_now=True, null=True)
    date_joined = DateTimeField(auto_now_add=True)
    # file
    image = ImageField(upload_to='users/images/', default='users/images/default.jpg')

    def __str__(self):
        return self.get_full_name()
