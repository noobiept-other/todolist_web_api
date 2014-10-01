from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse

import uuid

class Account( AbstractUser ):

    is_moderator = models.BooleanField( default= False )
    api_key = models.CharField( max_length= 36, unique= True, default= uuid.uuid4 )

    def get_url(self):
        return reverse( 'accounts:user_page', args= [ self.username ] )

    def new_api_key(self):
        key = uuid.uuid4()

        self.api_key = key
        self.save()

        return key

class PrivateMessage( models.Model ):

    receiver = models.ForeignKey( settings.AUTH_USER_MODEL )
    sender = models.ForeignKey( settings.AUTH_USER_MODEL, related_name= 'sender' )
    title = models.TextField( max_length= 100 )
    content = models.TextField( max_length= 500 )
    date_created = models.DateTimeField( help_text= 'Date Created', default= lambda: timezone.localtime( timezone.now() ) )

    def __unicode__(self):
        return self.title

    def get_url(self):
        return reverse( 'accounts:open_message', args= [ self.id ] )