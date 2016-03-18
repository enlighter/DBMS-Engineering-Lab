from django import forms
import logging

from .models import MyUser

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('site.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

class MyBackend(object):
    def authenticate(self, username=None, password=None):
        # Check the username/password and return a User.
        if username != None and password != None:
            # Get the user
            try:
                user = MyUser.objects.get(email=username)
            except MyUser.DoesNotExist:
                logger.error("User by this email ({0}) doesn't exist!".format(username))
                raise forms.ValidationError('Invalid login details')

            if user and user.check_password(password):
                logger.info('User is authenticated, logging user in')
                return user
            else:
                logger.error("User by this password doesn't exist!")
                raise forms.ValidationError('Invalid login details')
        return None

    def get_user(self, email):
        try:
            return MyUser.objects.get(email=email)
        except MyUser.DoesNotExist:
           return None