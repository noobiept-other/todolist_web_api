from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse

import uuid


class Account( AbstractUser ):

    api_key = models.UUIDField( unique= True, default= uuid.uuid4 )

    def get_url(self):
        return reverse( 'accounts:user_page', args= [ self.username ] )

    def new_api_key(self):
        key = uuid.uuid4()

        self.api_key = key
        self.save( update_fields= [ 'api_key' ] )

        return key

    def __str__(self):
        return self.username
