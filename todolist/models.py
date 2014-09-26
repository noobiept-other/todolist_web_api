from django.db import models
from django.contrib.auth.models import User

class Post( models.Model ):
    text = models.CharField( max_length= 200 )
    author = models.ForeignKey( User, related_name= 'posts' )
    date_created = models.DateTimeField( auto_now_add= True )
    last_updated = models.DateTimeField( auto_now_add= True )



