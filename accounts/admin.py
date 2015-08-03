from django.contrib import admin

from accounts.models import Account


class AccountAdmin( admin.ModelAdmin ):

    list_display = ( 'username', 'email', 'is_staff', 'date_joined' )

admin.site.register( Account, AccountAdmin )
