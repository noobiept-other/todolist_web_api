from todolist.models import Post


def _post_model_to_dict( post ):

    return {
        'pk': post.pk,
        'text': post.text,
        'author': post.author.username,
        'last_updated': post.last_updated.strftime( '%d/%m/%Y %H:%M' )
    }


def post_serializer( posts ):
    """
        Converts a Post to a dictionary, or a QuerySet of Posts to a list of dictionaries, ready to be serialized.
        It doesn't convert to json (or other format), but its ready for that step (just json.dumps()).

    :param posts: Either a Post object, or a QuerySet of Post objects
    :return: dict or list of dicts
    """

        # single Post object
    if isinstance( posts, Post ):

        return _post_model_to_dict( posts )

        # a QuerySet of Post objects
    else:
        allPosts = []

        for post in posts:
            allPosts.append( _post_model_to_dict( post ) )

        return allPosts