from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.utils import timezone

from todolist.models import Post
from todolist.serializers import post_serializer
from todolist.decorators import post_only


@csrf_exempt
@post_only
def info( request ):
    """
        Return information about the account.

        Variables required in the POST request:
            - api_key : User identifier.

        returns = {
            'username': str,
            'post_count': int
        }
    """
    user = _get_user( request )

    if isinstance( user, HttpResponse ):
        return user

    response = {
        'username': user.username,
        'post_count': user.posts.count()
    }

    return JsonResponse( response, status= 200 )


@csrf_exempt
@post_only
def add( request ):
    """
        Add a single post to the list.

        Variables required in the POST request:
            - api_key : User identifier.
            - text    : The text string of a single post.

        returns = {
            'id': int,
            'text': str,
            'last_updated': str
        }
    """
    user = _get_user( request )

    if isinstance( user, HttpResponse ):
        return user

    text = _get_text( request )

    if isinstance( text, HttpResponse ):
        return text

    post = Post.objects.create( text= text, author= user )

    return JsonResponse( post_serializer( post ), status= 201 )


@csrf_exempt
@post_only
def add_multiple( request ):
    """
        Add multiple new posts.

        Variables required in the POST request:
            - api_key : User identifier.
            - text[]  : A list of strings, of the posts to be added.

        returns = {
            'post[]': [
                {
                    'id': int,
                    'text': str,
                    'last_updated': str
                },
                # (...)
            ]
        }
    """
    user = _get_user( request )

    if isinstance( user, HttpResponse ):
        return user

    textList = _get_text_list( request )

    if isinstance( textList, HttpResponse ):
        return textList

    posts = []

    for text in textList:
        post = Post.objects.create( text= text, author= user )

        posts.append( post )

    return JsonResponse( { 'post[]': post_serializer( posts ) }, status= 201 )


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
            'last_updated': str
        }
    """
    post = _get_post( request )

    if isinstance( post, HttpResponse ):
        return post

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
            'post[]': [
                {
                    'id': int,
                    'text': str,
                    'last_updated': str
                },
                # (...)
            ]
        }
    """
    posts = _get_post_list( request )

    if isinstance( posts, HttpResponse ):
        return posts

    data = post_serializer( posts )

    return JsonResponse( { 'post[]': data }, status= 200 )


@csrf_exempt
@post_only
def get_all( request ):
    """
        Get all the posts from the user.

        Variables required in the POST request:
            - api_key : User identifier.

        returns = {
            'post[]': [
                {
                    'id': int,
                    'text': str,
                    'last_updated': str
                },
                # (...)
            ]
        }
    """
    user = _get_user( request )

    if isinstance( user, HttpResponse ):
        return user

    posts = user.posts.all()
    data = post_serializer( posts )

    return JsonResponse( { 'post[]': data }, status= 200 )


@csrf_exempt
@post_only
def update( request ):
    """
        Update an existing post.

        Variables required in the POST request:
            - api_key : User identifier.
            - id      : Post identifier.
            - text    : The new text of the post.

        returns = {
            'id': int,
            'text': str,
            'last_updated': str
        }
    """
    post = _get_post( request )

    if isinstance( post, HttpResponse ):
        return post

    text = _get_text( request )

    if isinstance( text, HttpResponse ):
        return text

    post.last_updated = timezone.now()
    post.text = text
    post.save( update_fields= [ 'last_updated', 'text' ] )

    return JsonResponse( post_serializer( post ), status= 200 )


@csrf_exempt
@post_only
def update_multiple( request ):
    """
        Update several posts.

        Variables required in the POST request:
            - api_key : User identifier.
            - id[]    : A list with the posts identifiers.
            - text[]  : A list with the new text for each post. The text must have the same position as in the id list.

        returns = {
            'post[]': [
                {
                    'id': int,
                    'text': str,
                    'last_updated': str
                },
                # (...)
            ]
        }
    """
    posts = _get_post_list( request )

    if isinstance( posts, HttpResponse ):
        return posts

    texts = _get_text_list( request )

    if isinstance( texts, HttpResponse ):
        return texts

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

    return JsonResponse( { 'post[]': post_serializer( posts ) }, status= 200 )


@csrf_exempt
@post_only
def delete( request ):
    """
        Remove an existing post.

        Variables required in the POST request:
            - api_key : User identifier.
            - id      : Post identifier.
    """
    post = _get_post( request )

    if isinstance( post, HttpResponse ):
        return post

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
    posts = _get_post_list( request )

    if isinstance( posts, HttpResponse ):
        return posts

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

    if isinstance( user, HttpResponse ):
        return user

    user.posts.all().delete()

    return HttpResponse( status= 200 )


def _get_user( request ):
    """
        Get the corresponding user model, of the given 'api_key'.
        Returns an 'HttpResponseBadRequest' if something went wrong.
    """
    userModel = get_user_model()

    try:
        key = request.POST[ 'api_key' ]

    except KeyError:
        return HttpResponseBadRequest( "Missing 'api_key' argument." )

    try:
        user = userModel.objects.get( api_key= key )

    except (userModel.DoesNotExist, ValueError):
        return HttpResponseBadRequest( "Invalid 'api_key' argument." )

    return user


def _get_text( request ):
    """
        Get the 'text' variable from the POST request.
        Returns an 'HttpResponseBadRequest' if something went wrong.
    """
    text = request.POST.get( 'text' )

    if not text:
        return HttpResponseBadRequest( "Need 'text' argument." )

    return text


def _get_text_list( request ):
    """
        Get the 'text[]' list from the POST request.
        Returns an 'HttpResponseBadRequest' if something went wrong.
    """
    textList = request.POST.getlist( 'text[]' )

    if len( textList ) == 0:
        return HttpResponseBadRequest( "Need 'text[]' argument." )

    return textList


def _get_post( request ):
    """
        Get the post model object of the given 'id'.
        Returns an 'HttpResponseBadRequest' if something went wrong.
    """
    user = _get_user( request )

    if isinstance( user, HttpResponse ):
        return user

    postId = request.POST.get( 'id' )

    if not postId:
        return HttpResponseBadRequest( "Missing 'id' argument." )

    try:
        postId = int( postId )

    except ValueError:
        return HttpResponseBadRequest( "Invalid 'id' argument." )

    try:
        post = user.posts.get( pk= postId )

    except Post.DoesNotExist:
        return HttpResponseBadRequest( "Invalid 'id' argument." )

    return post


def _get_post_list( request ):
    """
        Get the posts model objects given a list of ids.
    """
    user = _get_user( request )

    if isinstance( user, HttpResponse ):
        return user

    ids = request.POST.getlist( 'id[]' )

    if len( ids ) == 0:
        return HttpResponseBadRequest( "Missing 'id[]' argument." )

    intIds = []

        # make sure its a list of integers
    for postId in ids:
        try:
            intIds.append( int( postId ) )

        except ValueError:
            return HttpResponseBadRequest( "Invalid 'id[]' argument." )

    posts = user.posts.filter( pk__in= intIds )

    if not posts:
        return HttpResponseBadRequest( "Invalid 'id[]' argument." )

    return posts
