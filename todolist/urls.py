from django.conf.urls import url

import todolist.views


urlpatterns = [
    url( r'^v1/list/info$', todolist.views.info, name= 'info' ),

    url( r'^v1/list/add$', todolist.views.add, name= 'add' ),
    url( r'^v1/list/add_multiple$', todolist.views.add_multiple, name= 'add_multiple' ),

    url( r'^v1/list/get$', todolist.views.get, name= 'get' ),
    url( r'^v1/list/get_multiple$', todolist.views.get_multiple, name= 'get_multiple' ),
    url( r'^v1/list/get_all', todolist.views.get_all, name= 'get_all' ),

    url( r'^v1/list/update$', todolist.views.update, name= 'update' ),
    url( r'^v1/list/update_multiple$', todolist.views.update_multiple, name= 'update_multiple' ),

    url( r'^v1/list/delete$', todolist.views.delete, name= 'delete' ),
    url( r'^v1/list/delete_multiple$', todolist.views.delete_multiple, name= 'delete_multiple' ),
    url( r'^v1/list/delete_all$', todolist.views.delete_all, name= 'delete_all' ),
]