# encoding: utf-8
from django.contrib.auth.models import User

# This is an authentication backend, that allows email addresses to be used as usernames,
# which the default auth backend doesn't.
class EmailOrUsernameModelBackend(object):
    def authenticate(self, username=None, password=None):  
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
            
        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None