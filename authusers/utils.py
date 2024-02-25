from django.contrib.auth.tokens import PasswordResetTokenGenerator

from authusers.models import AuthUser


# Token generators
#
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
        return str(user.pk) + user.password + str(login_timestamp) + str(timestamp) + str(user.is_active)


account_activation_token = AccountActivationTokenGenerator()
