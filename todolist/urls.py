from django.conf.urls import url

import todolist.views


urlpatterns = [
    url( r'^v1/post/add$', todolist.views.add_post, name= 'add_post' ),
    url( r'^v1/post/all$', todolist.views.all_posts, name= 'all_posts' ),
    url( r'^v1/post/get$', todolist.views.single_post, name= 'single_post' ),
    url( r'^v1/post/update$', todolist.views.update_post, name= 'update_post' ),
    url( r'^v1/post/delete$', todolist.views.delete_post, name= 'delete_post' ),
    url( r'^v1/post/help$', todolist.views.show_help, name= 'help' ),
]