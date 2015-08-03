from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


def must_be_staff( function ):
    """
        Check if the user is a staff member.
    """
    @login_required
    def func_wrapper( request, *args, **kwargs ):
        if not request.user.is_staff:
            return HttpResponseForbidden( "Not a staff member." )

        return function( request, *args, **kwargs )

    return func_wrapper
