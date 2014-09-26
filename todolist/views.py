from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from todolist.models import Post
from todolist.serializers import post_serializer

def login( request ):
    pass


@csrf_exempt
def add_post( request ):

    if request.method == 'POST':

        text = request.POST.get( 'text', '' )
        author = User.objects.get( pk= 1 )  #HERE

        post = Post( text= text, author= author )
        post.save()

        return JsonResponse( {}, status= 201 )

    else:
        return JsonResponse( { 'reason': 'POST requests only.' }, status= 400 )


def all_posts( request ):

    posts = Post.objects.all()

    data = post_serializer( posts )

    return JsonResponse( data, safe= False )


def single_post( request, pk ):

    try:
        post = Post.objects.get( pk= pk )

    except Post.DoesNotExist:
        raise Http404

    else:
        data = post_serializer( post )

        return JsonResponse( data )


def update_post( request, pk ):
    pass


def delete_post( request, pk ):
    pass


