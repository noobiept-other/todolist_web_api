def get_message( request, context ):
    """
        Checks the session to see if there's a message, and if so adds to the context object (don't forget, it changes the object from where its called).
    """
    message = request.session.get( 'MESSAGE' )

    if message:

        context[ 'MESSAGE' ] = message
        del request.session[ 'MESSAGE' ]


def set_message( request, message ):
    """
        Add a message to the session (will be displayed in the next page loaded).
    """
    request.session[ 'MESSAGE' ] = message
