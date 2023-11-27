from rest_framework.serializers import Serializer, EmailField


class EmailSerializer(Serializer):
    email = EmailField()
