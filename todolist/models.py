from django.db import models
from django.utils import timezone

from accounts.models import Account


TEXT_MAX_LENGTH = 200


class Post( models.Model ):
    text = models.CharField( max_length= TEXT_MAX_LENGTH )
    author = models.ForeignKey( Account, related_name= 'posts' )
    last_updated = models.DateTimeField( default= timezone.now )

    class Meta:
        ordering = [ '-last_updated' ]