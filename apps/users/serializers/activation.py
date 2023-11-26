from rest_framework.serializers import Serializer, EmailField


class SendEmailLinkSerializer(Serializer):
    email = EmailField()
