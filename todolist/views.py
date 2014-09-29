from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from todolist.models import Post
from todolist.serializers import post_serializer


@login_required
def home( request ):

    return HttpResponseRedirect( reverse( 'accounts:user_page', args= [ request.user.username ] ) )


@csrf_exempt
def add_post( request ):

    if request.method == 'POST':

        userModel = get_user_model()

        text = request.POST.get( 'text', '' )
        author = userModel.objects.get( pk= 1 )  #HERE

        post = Post( text= text, author= author )
        post.save()

        return JsonResponse( {}, status= 201 )

    else:
        return JsonResponse( { 'reason': 'POST requests only.' }, status= 405 )


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


@csrf_exempt
def update_post( request, pk ):

    if request.method != 'POST':
        return JsonResponse( { 'reason': 'POST requests only.' }, status= 405 )

    try:
        post = Post.objects.get( pk= pk )

    except Post.DoesNotExist:
        raise Http404

    else:
        try:
            text = request.POST[ 'text' ]

        except KeyError:
            return JsonResponse( { 'reason': "Need a 'text' argument." }, status= 400 )

        post.text = text
        post.save()

        return JsonResponse( {}, status= 200 )



def delete_post( request, pk ):

    try:
        post = Post.objects.get( pk= pk )

    except Post.DoesNotExist:
        raise Http404

    post.delete()

    return JsonResponse( {}, status= 204 )


