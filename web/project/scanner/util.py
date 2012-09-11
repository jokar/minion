from django.contrib.auth.models import User
from django.conf import settings
from project import scanner
import logging
import commonware

log = commonware.log.getLogger('playdoh')

#Function called from settings page which prevents user account creation if email not from accepted domain
def create_user(email):
    domain = email.rsplit('@', 1)[1]
    if domain in settings.ACCEPTED_USER_DOMAINS:
            return User.objects.create_user(email, email)
            #log.debug("WOULD HAVE added user from " + domain)