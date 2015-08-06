from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def show_help( request ):
    """
        Show the API documentation.
    """
    context = {
        'domain': request.get_host()
    }

    return render( request, 'help.html', context )


@login_required
def test( request ):
    """
        Open a test page off the API.
    """
    context = {
        'api_key': request.user.api_key
    }

    return render( request, 'test.html', context )