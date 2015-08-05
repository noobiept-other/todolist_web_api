from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.utils import timezone

from todolist.models import Post
from todolist.serializers import post_serializer
from todolist.decorators import post_only


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
        Add a single post to the list.

        Variables required in the POST request:
            - api_key : User identifier.
            - text    : The text string of a single post.

        returns = { 'id': int }
    """
    user = _get_user( request )

    if not user:
        return HttpResponseBadRequest( "Missing/invalid 'api_key' argument." )

    text = request.POST.get( 'text' )

    if not text:
        return HttpResponseBadRequest( "Need 'text' argument." )

    post = Post.objects.create( text= text, author= user )

    return JsonResponse( { 'id': post.pk }, status= 201 )


@csrf_exempt
@post_only
def add_multiple( request ):
    """
        Add multiple new posts.

        Variables required in the POST request:
            - api_key : User identifier.
            - text[]  : A list of strings, of the posts to be added.

        returns = { 'ids': int[] }
    """
    user = _get_user( request )

    if not user:
        return HttpResponseBadRequest( "Missing/invalid 'api_key' argument." )

    textList = request.POST.getlist( 'text[]' )

    if len( textList ) == 0:
        return HttpResponseBadRequest( "Need 'text[]' argument." )

    ids = []

    for text in textList:
        post = Post.objects.create( text= text, author= user )

        ids.append( post.pk )

    return JsonResponse( { 'ids': ids }, status= 201 )


@csrf_exempt
@post_only
def get( request ):
    """
        Get a post from an user.

        Variables required in the POST request:
            - api_key : User identifier.
            - id      : Post identifier.

        returns = {
            'id': int,
            'text': str,
            'author': str,
            'last_updated': str
        }
    """
    user = _get_user( request )

    if not user:
        return HttpResponseBadRequest( "Missing/invalid 'api_key' argument." )

    post = _get_post( request, user )

    if not post:
        return HttpResponseBadRequest( "Missing/invalid 'id' argument." )

    data = post_serializer( post )

    return JsonResponse( data, status= 200 )


@csrf_exempt
@post_only
def get_multiple( request ):
    """
        Get several posts from an user.

        Variables required in the POST request:
            - api_key : User identifier.
            - id[]    : A list of the post ids to retrieve.

        returns = {
            'posts': [
                {
                    'id': int,
                    'text': str,
                    'author': str,
                    'last_updated': str
                },
                # (...)
            ]
        }
    """
    user = _get_user( request )

    if not user:
        return HttpResponseBadRequest( "Missing/invalid 'api_key' argument." )

    posts = _get_posts( request, user )

    if not posts:
        return HttpResponseBadRequest( "Missing/invalid 'id[]' argument." )

    data = post_serializer( posts )

    return JsonResponse( { 'posts': data }, status= 200 )


@csrf_exempt
@post_only
def get_all( request ):
    """
        Get all the posts from the user.

        Variables required in the POST request:
            - api_key : User identifier.

        returns = {
            'posts': [
                {
                    'id': int,
                    'text': str,
                    'author': str,
                    'last_updated': str
                },
                # (...)
            ]
        }
    """
    user = _get_user( request )

    if not user:
        return HttpResponseBadRequest( "Missing/invalid 'api_key' argument." )

    posts = user.posts.all()
    data = post_serializer( posts )

    return JsonResponse( { 'posts': data }, status= 200 )


@csrf_exempt
@post_only
def update( request ):
    """
        Update an existing post.

        Variables required in the POST request:
            - api_key : User identifier.
            - id      : Post identifier.
            - text    : The new text of the post.
    """
    user = _get_user( request )

    if not user:
        return HttpResponseBadRequest( "Missing/invalid 'api_key' argument." )

    post = _get_post( request, user )

    if not post:
        return HttpResponseBadRequest( "Missing/invalid 'id' argument." )

    try:
        text = request.POST[ 'text' ]

    except KeyError:
        return HttpResponseBadRequest( "Need a 'text' argument." )

    post.last_updated = timezone.now()
    post.text = text
    post.save( update_fields= [ 'last_updated', 'text' ] )

    return HttpResponse( status= 200 )


@csrf_exempt
@post_only
def update_multiple( request ):
    """
        Update several posts.

        Variables required in the POST request:
            - api_key : User identifier.
            - id[]    : A list with the posts identifiers.
            - text[]  : A list with the new text for each post. The text must have the same position as in the id list.
    """
    user = _get_user( request )

    if not user:
        return HttpResponseBadRequest( "Missing/invalid 'api_key' argument." )

    posts = _get_posts( request, user )

    if not posts:
        return HttpResponseBadRequest( "Missing/invalid 'id[]' argument." )

    texts = request.POST.getlist( 'text[]' )

    if len( texts ) == 0:
        return HttpResponseBadRequest( "Missing/invalid 'text[]' argument." )

    now = timezone.now()

    for position, post in enumerate( posts ):
        try:
            text = texts[ position ]

        except IndexError:
            continue

        else:
            post.last_updated = now
            post.text = text
            post.save( update_fields= [ 'last_updated', 'text' ] )

    return HttpResponse( status= 200 )


@csrf_exempt
@post_only
def delete( request ):
    """
        Remove an existing post.

        Variables required in the POST request:
            - api_key : User identifier.
            - id      : Post identifier.
    """
    user = _get_user( request )

    if not user:
        return HttpResponseBadRequest( "Missing/invalid 'api_key' argument." )

    post = _get_post( request, user )

    if not post:
        return HttpResponseBadRequest( "Missing/invalid 'id' argument." )

    post.delete()

    return HttpResponse( status= 200 )


@csrf_exempt
@post_only
def delete_multiple( request ):
    """
        Delete multiple posts.

        Variables required in the POST request:
            - api_key : User identifier.
            - id[]    : A list with the posts identifiers.
    """
    user = _get_user( request )

    if not user:
        return HttpResponseBadRequest( "Missing/invalid 'api_key' argument." )

    posts = _get_posts( request, user )

    if not posts:
        return HttpResponseBadRequest( "Missing/invalid 'id[]' argument." )

    posts.delete()

    return HttpResponse( status= 200 )


@csrf_exempt
@post_only
def delete_all( request ):
    """
        Remove all the posts of a user.

        Variables required in the POST request:
            - api_key : User identifier.
    """
    user = _get_user( request )

    if not user:
        return HttpResponseBadRequest( "Missing/invalid 'api_key' argument." )

    user.posts.all().delete()

    return HttpResponse( status= 200 )


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
        Get the post model object of the given 'id'.
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


def _get_posts( request, user ):
    """
        Get the posts model objects given a list of ids.
    """
    ids = request.POST.getlist( 'id[]' )

    if len( ids ) == 0:
        return None

    posts = user.posts.filter( pk__in= ids )

    if not posts:
        return None

    return posts
