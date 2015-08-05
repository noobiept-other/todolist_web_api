from django.conf.urls import url

import todolist.views


urlpatterns = [
    url( r'^v1/post/add$', todolist.views.add, name= 'add' ),
    url( r'^v1/post/all$', todolist.views.get_all, name= 'get_all' ),
    url( r'^v1/post/get$', todolist.views.get, name= 'get' ),
    url( r'^v1/post/update$', todolist.views.update, name= 'update' ),
    url( r'^v1/post/delete$', todolist.views.delete, name= 'delete' ),
    url( r'^v1/post/help$', todolist.views.show_help, name= 'help' ),
]