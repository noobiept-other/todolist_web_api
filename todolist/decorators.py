from django.http import JsonResponse

def post_only( function ):

    def func_wrapper( request, *args, **kwargs ):
        if request.method != 'POST':
            return JsonResponse( { 'reason': 'POST requests only.' }, status= 405 )

        return function( request, *args, **kwargs )

    return func_wrapper