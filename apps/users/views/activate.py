from django.http import HttpResponse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from shared.django.serializers import NoneSerializer
from shared.token import account_activation_token
from users.models import User


class ActivateViewSet(GenericViewSet):
    queryset = User.objects.all()

    @action(methods=['get'], detail=True, serializer_class=NoneSerializer, url_path='email')
    def activate_email(self, request, uid, token):
        try:
            pk = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=pk)
        except Exception as e:
            user = None
            return HttpResponse(str(e))
        if user is not None and account_activation_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse('Successfully activated!')
        return HttpResponse('Activate link is expired!')
