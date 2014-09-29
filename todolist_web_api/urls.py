from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',

    url( '^$', 'todolist.views.home', name= 'home' ),
    url( r'^v1/post/add$', 'todolist.views.add_post', name= 'add_post' ),
    url( r'^v1/post/all$', 'todolist.views.all_posts', name= 'all_posts' ),
    url( r'^v1/post/get/(?P<pk>\d+)$', 'todolist.views.single_post', name= 'single_post' ),
    url( r'^v1/post/update/(?P<pk>\d+)$', 'todolist.views.update_post', name= 'update_post' ),
    url( r'^v1/post/delete/(?P<pk>\d+)$', 'todolist.views.delete_post', name= 'delete_post' ),


    url( r'^accounts/', include( 'accounts.urls', namespace= 'accounts', app_name= 'accounts' ) ),
    url( r'^admin/', include( admin.site.urls ) ),
)
