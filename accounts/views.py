from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as django_login

from accounts.forms import MyUserCreationForm
from accounts.decorators import must_be_staff

from todolist_web_api import utilities


def new_account( request ):
    """
        Create a new user account.
    """
    if request.method == 'POST':

        form = MyUserCreationForm( request.POST )

        if form.is_valid():

            form.save()
            utilities.set_message( request, "User '{}' created!".format(  form.cleaned_data[ 'username' ] ) )

            return HttpResponseRedirect( reverse( 'accounts:login' ) )

    else:
        form = MyUserCreationForm()

    context = {
        'form': form
    }

    return render( request, 'accounts/new_account.html', context )


def login( request ):
    """
        Login an account.
    """
    context = {}
    utilities.get_message( request, context )

    return django_login( request, 'accounts/login.html', extra_context= context )


@login_required
def user_page( request, username ):
    """
        The user page has information about an user account.
        Also where you can change some settings (like the password).
    """
    if request.user.username != username and not request.user.is_staff:
        return HttpResponseForbidden( "Not allowed." )

    userModel = get_user_model()

    try:
        user = userModel.objects.get( username= username )

    except userModel.DoesNotExist:
        raise Http404( "User doesn't exist." )

    context = {
        'pageUser': user,
    }

    utilities.get_message( request, context )

    return render( request, 'accounts/user_page.html', context )


def password_changed( request ):
    """
        Inform that the password has been changed, and redirect to home.
    """
    utilities.set_message( request, 'Password changed!' )

    return HttpResponseRedirect( reverse( 'home' ) )


@must_be_staff
def remove_user_confirm( request, username ):
    """
        Confirm an user removal.
    """
    userModel = get_user_model()

    try:
        user = userModel.objects.get( username= username )

    except userModel.DoesNotExist:
        raise Http404( "User doesn't exist." )

    context = {
        'user_to_remove': user
    }

    return render( request, 'accounts/remove_user.html', context )


@must_be_staff
def remove_user( request, username ):
    """
        Remove an user account (also removes everything associated with it).
    """
    userModel = get_user_model()

    try:
        user = userModel.objects.get( username= username )

    except userModel.DoesNotExist:
        raise Http404( "User doesn't exist." )

    else:
        utilities.set_message( request, "'{}' user removed!".format( user ) )
        user.delete()

        return HttpResponseRedirect( reverse( 'home' ) )


@must_be_staff
def disable_user_confirm( request, username ):
    """
        Confirm the enabling/disabling of an user account.
    """
    userModel = get_user_model()

    try:
        user = userModel.objects.get( username= username )

    except userModel.DoesNotExist:
        raise Http404( "User doesn't exist." )

    else:
        context = {
            'user_to_disable': user
        }

        return render( request, 'accounts/disable_user.html', context )


@must_be_staff
def disable_user( request, username ):
    """
        Enable/disable an user account.
        If the account is disabled, the user won't be able to login.
    """
    userModel = get_user_model()

    try:
        user = userModel.objects.get( username= username )

    except userModel.DoesNotExist:
        raise Http404( "User doesn't exist." )

    else:
        value = not user.is_active

            # only other staff users can enable/disable staff users
        if user.is_staff:
            if request.user.is_staff:
                user.is_active = value
                user.save()

            else:
                return HttpResponseForbidden( "Can't disable a staff member." )

        else:
            user.is_active = value
            user.save()


        if value:
            message = "'{}' account is now active.".format( user )

        else:
            message = "'{}' account is now disabled.".format( user )

        utilities.set_message( request, message )

        return HttpResponseRedirect( user.get_url() )


@login_required
def new_api_key( request ):
    """
        Get a new API key.
    """
    request.user.new_api_key()
    utilities.set_message( request, 'New API key set!' )

    return HttpResponseRedirect( reverse( 'accounts:user_page', args= [ request.user.username ] ) )