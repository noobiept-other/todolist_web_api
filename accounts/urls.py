from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url( r'^new_account$', 'accounts.views.new_account', name= 'new_account' ),
    url( r'^login$', 'django.contrib.auth.views.login', { 'template_name': 'accounts/login.html' }, name= 'login' ),
    url( r'^logout$', 'django.contrib.auth.views.logout', { 'next_page': '/' }, name= 'logout' ),
    url( r'^change_password$', 'django.contrib.auth.views.password_change', { 'template_name': 'accounts/change_password.html', 'post_change_redirect': 'accounts:password_changed' }, name= 'change_password' ),
    url( r'^password_changed$', 'accounts.views.password_changed', name= 'password_changed' ),
    url( r'^user/(?P<username>\w+)$', 'accounts.views.user_page', name= 'user_page' ),
    url( r'^new_api_key$', 'accounts.views.new_api_key', name= 'new_api_key' ),
)
