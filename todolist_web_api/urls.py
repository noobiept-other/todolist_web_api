from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',

    url( '^$', 'todolist.views.home', name= 'home' ),

    url( r'^', include( 'todolist.urls' ) ),
    url( r'^accounts/', include( 'accounts.urls', namespace= 'accounts', app_name= 'accounts' ) ),
    url( r'^admin/', include( admin.site.urls ) ),
)

