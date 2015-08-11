"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

import todolist.urls
import todolist.views
import accounts.urls
import todolist_web_api.views


urlpatterns = [

    url( '^$', todolist_web_api.views.show_help, name= 'home' ),
    url( '^test$', todolist_web_api.views.test, name= 'test' ),

    url( r'^', include( todolist.urls, namespace= 'todolist', app_name= 'todolist' ) ),
    url( r'^accounts/', include( accounts.urls, namespace= 'accounts', app_name= 'accounts' ) ),
    url( r'^admin/', include( admin.site.urls ) ),
]


    # Serve static files when debug false
if not settings.DEBUG:
    urlpatterns += [
        url( r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT } ),
    ]