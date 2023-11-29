from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import Form


class ResetPasswordForm(Form):
    def clean_password(self):
        new_password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        password = make_password(new_password)
        if new_password != confirm_password:
            raise ValidationError('Passwords did not match')
        return password
