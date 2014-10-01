from django.db import models
from django.contrib.auth.models import AbstractUser
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
