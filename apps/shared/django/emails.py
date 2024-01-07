from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode

from root import settings
from shared.tokens import activate_token
from users.models import User


def get_one_time_link(request, user, url, token: str):
    uid = urlsafe_base64_encode(force_bytes(str(user.pk)))
    current_site = get_current_site(request)
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    base_url = f'{protocol}://{current_site}'
    link = f'{base_url}/api/user/{url}/{uid}/{token}/'
    return link


def send_email_link(request, email: str, subject: str, message: str, url: str):
    user = get_object_or_404(User, email=email)
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    token = activate_token.make_token(user)
    link = get_one_time_link(request, user, url, token)
    context = {
        'link': link,
        'base_url': settings.BASE_URL,
        'type_request': 'confirmation',
        'logo': settings.EMAIL_LOGO,
        'message': message,
        'title': subject
    }
    html_content = render_to_string('activation.html', context)
    html_text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, html_text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def test_send_email():
    from django.core.mail import EmailMultiAlternatives
    subject, from_email, to = "hello", "khasanjon.eng@gmail.com", "khasanjon.dev@gmail.com"
    link = 'current'
    context = {
        'link': link,
        'base_url': settings.BASE_URL,
        'type_request': 'confirmation',
        'logo': settings.EMAIL_LOGO
    }
    html_content = render_to_string('activation.html', context)
    html_text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, html_text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
