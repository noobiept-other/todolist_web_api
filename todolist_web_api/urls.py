"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
"""
from django.conf.urls import include, url
from django.contrib import admin

import todolist.urls
import todolist.views
import accounts.urls


urlpatterns = [

    url( '^$', todolist.views.home, name= 'home' ),

    url( r'^', include( todolist.urls ) ),
    url( r'^accounts/', include( accounts.urls, namespace= 'accounts', app_name= 'accounts' ) ),
    url( r'^admin/', include( admin.site.urls ) ),
]

