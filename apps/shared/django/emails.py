import sib_api_v3_sdk
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from sib_api_v3_sdk.rest import ApiException

from root import settings


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


def send_email_link(email, subject, link):
    email_send_message(email, subject, link)
    # from_email = None
    # recipient_list = [email]
    # context = {
    #     'link': link,
    #     'base_url': settings.BASE_URL
    # }
    # html_content = render_to_string('activation.html', context)
    # html_text_content = strip_tags(html_content)
    # email = EmailMultiAlternatives(subject, html_text_content, from_email, recipient_list)
    # email.attach_alternative(html_content, 'text/html')
    # email.send()


def email_send_message(email, subject, link):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.BREVO_API_KEY
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    def send_email(subject, html, email):
        sender = {
            "name": "DevMasters",
            "email": "devmasters.uz@gmail.com"
        }
        to = [{'email': email}]
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html, sender=sender, subject=subject)
        try:
            api_response = api_instance.send_transac_email(send_smtp_email)
            print(api_response)
            return {"message": "Email sent successfully!"}
        except ApiException as e:
            print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

    context = {
        'link': link,
        'base_url': settings.BASE_URL
    }
    html_content = render_to_string('activation.html', context)
    # html_text_content = strip_tags(html_content)
    print("Sending mail...")
    email_response = send_email(subject, html_content, email)
    print(email_response)
