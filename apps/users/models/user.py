from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db.models import CharField, DateTimeField, EmailField, BooleanField, ImageField

from root.settings import DEFAULT_USER_IMAGE
from shared.django.upload_images import upload_image
from shared.django.validators import username_validator


class User(AbstractUser):
    last_name = CharField(max_length=150, null=True, blank=True)
    bio = CharField(max_length=250, null=True, blank=True)
    email = EmailField(unique=True)
    image = ImageField(upload_to=upload_image, default=DEFAULT_USER_IMAGE)
    username = CharField(max_length=32, unique=True, validators=[username_validator, MinLengthValidator(5)])
    # bool
    is_active = BooleanField(default=False)
    # date
    updated_at = DateTimeField(auto_now=True, null=True)
    date_joined = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_full_name()
