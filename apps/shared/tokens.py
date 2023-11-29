import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class ActivateTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )


class ResetPasswordTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp),
        )


activate_token = ActivateTokenGenerator()
reset_password_token = PasswordResetTokenGenerator()
