from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from root.settings import EMAIL_HOST_USER
from shared.token import account_activation_token
from users.models import User


def send_email_link(request, email: str, subject: str, message: str, url: str):
    user = get_object_or_404(User, email=email)
    domain = get_current_site(request)
    from_email = EMAIL_HOST_USER
    recipient_list = [email]
    uid = urlsafe_base64_encode(force_bytes(str(user.pk)))
    token = account_activation_token.make_token(user)
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    link = f'{protocol}://{domain}/api/user/activate/{uid}/{token}/'
    context = {
        'user': user,
        'link': link,
        'message': message
    }
    message = render_to_string('activate.html', context)
    send_mail(subject, message, from_email, recipient_list)
