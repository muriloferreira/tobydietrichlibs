from django.conf import settings

# can new users register. Does not affect registration via admin interface
CAREER_MODULE_REGISTER_ALLOW_REGISTRATION = getattr(settings, 'CAREER_MODULE_REGISTER_ALLOW_REGISTRATION', True)


# the max email length, set by email_usernames or the system
CAREER_MODULE_REGISTER_MAX_EMAIL_LENGTH = getattr(settings, 'CAREER_MODULE_REGISTER_MAX_EMAIL_LENGTH', 75)