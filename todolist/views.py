from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.utils import timezone

from todolist.models import Post
from todolist.serializers import post_serializer
from todolist.decorators import post_only


@login_required
def home( request ):
    """
        Redirect to the user page.
    """
    return HttpResponseRedirect( reverse( 'accounts:user_page', args= [ request.user.username ] ) )


def show_help( request ):
    """
        Show the API documentation.
    """
    context = {
        'domain': request.get_host()
    }

    return render( request, 'help.html', context )


@csrf_exempt
@post_only
def add( request ):
    """
        Add a single or multiple new posts.

        Variables required in the post request:
            - api_key : User identifier.
            - text    : The text string of a single post.
            - text[]  : A list of strings, of the posts to be added.
        Send either "text" (to add a single post) or "text[]" (multiple posts).

        return_single_post = { 'id': int }
        return_multiple_posts = { 'ids': int[] }
    """
    user = _get_user( request )

    if not user:
        return JsonResponse( { 'reason': "Missing/invalid 'api_key' argument." }, status= 400 )

    text = request.POST.get( 'text' )

    if text:
        post = Post.objects.create( text= text, author= user )

        return JsonResponse( { 'id': post.pk }, status= 201 )

    else:
        textList = request.POST.getlist( 'text[]' )

        if len( textList ) == 0:
            return JsonResponse( { 'reason': "Need 'text' or 'text[]' argument." }, status= 400 )

        ids = []

        for text in textList:
            post = Post.objects.create( text= text, author= user )

            ids.append( post.pk )

        return JsonResponse( { 'ids': ids }, status= 201 )


@csrf_exempt
@post_only
def all_posts( request ):
    """
        Get all the posts from the user.

        Requires the 'api_key' variable in the post request.
        returned = [
            {
                'id': int,
                'text': str,
                'author': str,
                'last_updated': str
            },
            # (...)
        ]
    """
    user = _get_user( request )

    if not user:
        return JsonResponse( { 'reason': "Missing/invalid 'api_key' argument." }, status= 400 )

    posts = user.posts.all()

    data = post_serializer( posts )

    return JsonResponse( data, safe= False, status= 200 )


@csrf_exempt
@post_only
def single_post( request ):
    """
        Get a post from a user.

        Requires an 'api_key' and an 'id' variable sent in the post request.
        returned = {
            'id': int,
            'text': str,
            'author': str,
            'last_updated': str
        }
    """
    user = _get_user( request )

    if not user:
        return JsonResponse( { 'reason': "Missing/invalid 'api_key' argument." }, status= 400 )

    post = _get_post( request, user )

    if not post:
        return JsonResponse( { 'reason': "Missing/invalid 'id' argument." }, status= 400 )

    data = post_serializer( post )

    return JsonResponse( data, status= 200 )


@csrf_exempt
@post_only
def update_post( request ):
    """
        Update an existing post.

        Requires an 'api_key', an 'id' and a 'text' variable sent in the post request.
        returned = {}
    """
    user = _get_user( request )

    if not user:
        return JsonResponse( { 'reason': "Missing/invalid 'api_key' argument." }, status= 400 )

    post = _get_post( request, user )

    if not post:
        return JsonResponse( { 'reason': "Missing/invalid 'id' argument." }, status= 400 )

    try:
        text = request.POST[ 'text' ]

    except KeyError:
        return JsonResponse( { 'reason': "Need a 'text' argument." }, status= 400 )

    post.last_updated = timezone.now()
    post.text = text
    post.save( update_fields= [ 'last_updated', 'text' ] )

    return JsonResponse( {}, status= 200 )


@csrf_exempt
@post_only
def delete_post( request ):
    """
        Remove an existing post.

        Requires an 'api_key' and an 'id' variable sent in the post request.
        returned = {}
    """
    user = _get_user( request )

    if not user:
        return JsonResponse( { 'reason': "Missing/invalid 'api_key' argument." }, status= 400 )

    post = _get_post( request, user )

    if not post:
        return JsonResponse( { 'reason': "Missing/invalid 'id' argument." }, status= 400 )

    post.delete()

    return JsonResponse( {}, status= 200 )


def _get_user( request ):
    """
        Get the corresponding user model, of the given 'api_key'.
    """
    userModel = get_user_model()

    try:
        key = request.POST[ 'api_key' ]

    except KeyError:
        return None

    try:
        user = userModel.objects.get( api_key= key )

    except (userModel.DoesNotExist, ValueError):
        return None

    return user


def _get_post( request, user ):
    """
        Get the post model of the given 'id'.
    """
    try:
        postId = request.POST[ 'id' ]

    except KeyError:
        return None

    try:
        post = user.posts.get( pk= postId )

    except Post.DoesNotExist:
        return None

    return post