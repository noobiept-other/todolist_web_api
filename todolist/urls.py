from django.conf.urls import url

import todolist.views


urlpatterns = [
    url( r'^v1/info$', todolist.views.info, name= 'info' ),

    url( r'^v1/post/add$', todolist.views.add, name= 'add' ),
    url( r'^v1/post/add_multiple$', todolist.views.add_multiple, name= 'add_multiple' ),

    url( r'^v1/post/get$', todolist.views.get, name= 'get' ),
    url( r'^v1/post/get_multiple$', todolist.views.get_multiple, name= 'get_multiple' ),
    url( r'^v1/post/get_all', todolist.views.get_all, name= 'get_all' ),

    url( r'^v1/post/update$', todolist.views.update, name= 'update' ),
    url( r'^v1/post/update_multiple$', todolist.views.update_multiple, name= 'update_multiple' ),

    url( r'^v1/post/delete$', todolist.views.delete, name= 'delete' ),
    url( r'^v1/post/delete_multiple$', todolist.views.delete_multiple, name= 'delete_multiple' ),
    url( r'^v1/post/delete_all$', todolist.views.delete_all, name= 'delete_all' ),

    url( r'^v1/post/help$', todolist.views.show_help, name= 'help' ),
]