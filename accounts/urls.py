from django.conf.urls import url
import django.contrib.auth.views

import accounts.views


urlpatterns = [

    url( r'^new_account$', accounts.views.new_account, name= 'new_account' ),
    url( r'^login$', accounts.views.login, name= 'login' ),
    url( r'^logout$', django.contrib.auth.views.logout, name= 'logout' ),
    url( r'^user/(?P<username>\w+)$', accounts.views.user_page, name= 'user_page' ),

        # Remove Account
    url( r'^remove/confirm/(?P<username>\w+)$', accounts.views.remove_user_confirm, name= 'remove_confirm' ),
    url( r'^remove/(?P<username>\w+)$', accounts.views.remove_user, name= 'remove' ),

        # Disable Account
    url( r'^disable/confirm/(?P<username>\w+)$', accounts.views.disable_user_confirm, name= 'disable_confirm' ),
    url( r'^disable/(?P<username>\w+)$', accounts.views.disable_user, name= 'disable' ),

        # Change Password
    url( r'^change_password$', django.contrib.auth.views.password_change, { 'template_name': 'accounts/change_password.html', 'post_change_redirect': 'accounts:password_changed' }, name= 'change_password' ),
    url( r'^password_changed$', accounts.views.password_changed, name= 'password_changed' ),

        # Api Key
    url( r'^new_api_key$', 'accounts.views.new_api_key', name= 'new_api_key' ),
]
