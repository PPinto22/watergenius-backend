from django.conf import settings
from django.contrib.auth.hashers import check_password
from api.models import User

class SettingsBackend(object):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'pbkdf2_sha256$30000$Vo0VlMnkR4Bk$qEvtdyZRWTcOsCnI/oQ7fVOu1XAURIZYoOZ3iq8Dr4M='
    """

    def authenticate( username=None, password=None):
        try:
            user = User.objects.get(user_email=username)
        except User.DoesNotExist:
                # Create a new user. There's no need to set a password
                # because only the password from settings.py is checked.
            return None
        pwd_valid = check_password(password, user.password)
        if pwd_valid:
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(user_email=user_id)
        except User.DoesNotExist:
            return None