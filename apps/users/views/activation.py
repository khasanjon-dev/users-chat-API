from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from shared.django.email import send_email_
from shared.token import account_activation_token
from users.models import User
from users.serializers import SendEmailLinkSerializer


class ActivateEmail(APIView):
    @swagger_auto_schema(auto_schema=None)
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


class SendEmailLink(APIView):
    def post(self, request):
        """
        email ga activate link yuborish

        ```
        {
            "email": "devmasters.uz@gmail.com"
        }
        ```
        """
        try:
            serializer = SendEmailLinkSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = get_object_or_404(User, email=serializer.data.get('email'))
            # if user.is_active:
            #     context = {
            #         'message': 'Already activate user'
            #     }
            #     return Response(context)
            send_email_(request, user.email, 'Activation link', 'here your activation link', 'activate')
            context = {
                'message': 'Successfully send link'
            }
            return Response(context)
        except Exception as e:
            context = {
                'message': str(e)
            }
            return Response(context, status.HTTP_400_BAD_REQUEST)
