from django.http import HttpResponse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.views import APIView

from shared.token import account_activation_token
from users.models import User


class ActivateEmail(APIView):
    def get(self, request, uid: str, token: str):
        try:
            pk = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=pk)
        except Exception as e:
            return HttpResponse(str(e))
        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            message = 'Successfully activated!'
            return HttpResponse(message)
        return HttpResponse('Activate link is expired')
