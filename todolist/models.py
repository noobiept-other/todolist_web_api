from django.db import models
from django.utils import timezone

from accounts.models import Account

class Post( models.Model ):
    text = models.CharField( max_length= 200 )
    author = models.ForeignKey( Account, related_name= 'posts' )
    last_updated = models.DateTimeField( default= timezone.now )

    class Meta:
        ordering = [ '-last_updated' ]