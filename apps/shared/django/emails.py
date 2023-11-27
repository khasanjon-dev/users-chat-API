from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode

from root import settings
from shared.token import account_activation_token


# def send_email_link(request, email: str, subject: str, message: str, url: str):
#     user = get_object_or_404(User, email=email)
#     domain = get_current_site(request)
#     from_email = EMAIL_HOST_USER
#     recipient_list = [email]
#     uid = urlsafe_base64_encode(force_bytes(str(user.pk)))
#     token = account_activation_token.make_token(user)
#     if request.is_secure():
#         protocol = 'https'
#     else:
#         protocol = 'http'
#     link = f'{protocol}://{domain}/api/user/activate/{uid}/{token}/'
#     context = {
#         'user': user,
#         'link': link,
#         'message': message
#     }
#     message = render_to_string('activate.html', context)
#     send_mail(subject, message, from_email, recipient_list)


def get_one_time_link(request, user, url):
    uid = urlsafe_base64_encode(force_bytes(str(user.pk)))
    token = account_activation_token.make_token(user)
    current_site = get_current_site(request)
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    base_url = f'{protocol}://{current_site}'
    link = f'{base_url}/api/user/{url}/{uid}/{token}/'
    return link


def send_email_link(email, subject, link):
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    context = {
        'link': link,
        'base_url': settings.BASE_URL
    }
    html_content = render_to_string('activation.html', context)
    html_text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, html_text_content, from_email, recipient_list)
    email.attach_alternative(html_content, 'text/html')
    email.send()
