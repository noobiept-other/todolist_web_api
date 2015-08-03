from django.contrib import admin

from todolist.models import Post


class PostAdmin( admin.ModelAdmin ):

    list_display = ( 'pk', 'author', 'text', 'last_updated' )

admin.site.register( Post, PostAdmin )