from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode

from root.settings import EMAIL_HOST_USER
from shared.token import account_activation_token
from users.models import User


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


def send_email_link(request, user, subject, url):
    domain = get_current_site(request)
    from_email = EMAIL_HOST_USER
    recipient_list = [user.email]
    uid = urlsafe_base64_encode(force_bytes(str(user.pk)))
    token = account_activation_token.make_token(user)
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    base_url = f'{protocol}://{domain}'
    link = f'{base_url}/api/user/{url}/{uid}/{token}/'
    context = {
        'link': link,
        'base_url': base_url
    }
    html_content = render_to_string('activation.html', context)
    plain_text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject,
        plain_text_content,
        from_email,
        recipient_list
    )
    email.attach_alternative(html_content, 'text/html')
    email.send()
