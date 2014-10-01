from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from accounts.forms import MyUserCreationForm
import todolist_web_api.utilities as utilities


def new_account( request ):

    if request.method == 'POST':

        form = MyUserCreationForm( request.POST )

        if form.is_valid():

            form.save()
            return HttpResponseRedirect( reverse( 'accounts:login' ) )

    else:
        form = MyUserCreationForm()

    context = {
        'form': form
    }

    return render( request, 'accounts/new_account.html', context )


@login_required
def user_page( request, username ):

    if request.user.username != username:
        return HttpResponseForbidden( 'Can only open your own user page.' )

    context = {}

    utilities.get_message( request, context )

    return render( request, 'accounts/user_page.html', context )



def password_changed( request ):

    utilities.set_message( request, 'Password changed' )

    return HttpResponseRedirect( reverse( 'home' ) )


@login_required
def new_api_key( request ):

    request.user.new_api_key()

    return HttpResponseRedirect( reverse( 'accounts:user_page', args= [ request.user.username ] ) )