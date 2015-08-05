from django.http import HttpResponseNotAllowed

def post_only( function ):

    def func_wrapper( request, *args, **kwargs ):
        if request.method != 'POST':
            return HttpResponseNotAllowed( [ 'POST' ] )

        return function( request, *args, **kwargs )

    return func_wrapper