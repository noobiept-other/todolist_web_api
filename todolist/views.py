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

    return HttpResponseRedirect( reverse( 'accounts:user_page', args= [ request.user.username ] ) )


def show_help( request ):

    context = {
        'domain': request.get_host()
    }

    return render( request, 'help.html', context )


@csrf_exempt
@post_only
def add_post( request ):

    user = _get_user( request )

    if not user:
        return JsonResponse( { 'reason': "Missing/invalid 'api_key' argument." }, status= 400 )

    try:
        text = request.POST[ 'text' ]

    except KeyError:
        return JsonResponse( { 'reason': "Need 'text' argument." }, status= 400 )


    post = Post( text= text, author= user )
    post.save()

    return JsonResponse( { 'id': post.pk }, status= 201 )



@csrf_exempt
@post_only
def all_posts( request ):

    user = _get_user( request )

    if not user:
        return JsonResponse( { 'reason': "Missing/invalid 'api_key' argument." }, status= 400 )

    posts = user.posts.all()

    data = post_serializer( posts )

    return JsonResponse( data, safe= False, status= 200 )


@csrf_exempt
@post_only
def single_post( request ):

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

    user = _get_user( request )

    if not user:
        return JsonResponse( { 'reason': "Missing/invalid 'api_key' argument." }, status= 400 )

    post = _get_post( request, user )

    if not post:
        return JsonResponse( { 'reason': "Missing/invalid 'id' argument." }, status= 400 )

    post.delete()

    return JsonResponse( {}, status= 200 )




def _get_user( request ):

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

    try:
        postId = request.POST[ 'id' ]

    except KeyError:
        return None

    try:
        post = user.posts.get( pk= postId )

    except Post.DoesNotExist:
        return None

    return post