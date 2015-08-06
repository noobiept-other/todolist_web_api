from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

import json


class TodolistTest( TestCase ):
    def setUp(self):

            # create a user
        userModel = get_user_model()

        self.user = userModel.objects.create_user( username= 'test', email= 'test@test.pt', password= 'test' )
        self.api_key = self.user.api_key

            # add a client
        self.client = Client()

            # get the api's urls
        self.info_url = reverse( 'todolist:info' )
        self.add_url = reverse( 'todolist:add' )
        self.add_multiple_url = reverse( 'todolist:add_multiple' )
        self.get_url = reverse( 'todolist:get' )
        self.get_multiple_url = reverse( 'todolist:get_multiple' )
        self.get_all_url = reverse( 'todolist:get_all' )
        self.update_url = reverse( 'todolist:update' )
        self.update_multiple_url = reverse( 'todolist:update_multiple' )
        self.delete_url = reverse( 'todolist:delete' )
        self.delete_multiple_url = reverse( 'todolist:delete_multiple' )
        self.delete_all_url = reverse( 'todolist:delete_all' )


    # -- Helper Functions -- #


    def _make_request(self, url, arguments= None):
        """
            Make a POST request and add the required 'api_key' to the arguments.
            Return the de-serialized JSON data from a response object.
        """
        if not arguments:
            arguments = {}

            # the api_key is needed for all requests
        arguments[ 'api_key' ] = self.api_key

        response = self.client.post( url, arguments )

        return json.loads( response.content.decode( encoding= 'utf-8' ) )


    def _bad_request(self, url, hasOtherArgs):
        """
            Test for missing/invalid 'api_key' argument in the POST request, and for other missing variables.
        """
            # not POST request
        response = self.client.get( url )
        self.assertEqual( response.status_code, 405 )

            # no arguments
        response = self.client.post( url )
        self.assertEqual( response.status_code, 400 )

            # invalid 'api_key'
        response = self.client.post( url, { 'api_key': 'random' } )
        self.assertEqual( response.status_code, 400 )

            # requires other arguments, so should still get a 400 code
        if hasOtherArgs:
            response = self.client.post( url, { 'api_key': self.api_key } )
            self.assertEqual( response.status_code, 400 )


    # -- Tests -- #


    def test_info_bad_request(self):
        self._bad_request( self.info_url, False )


    def test_info(self):
        info = self._make_request( self.info_url )

        self.assertEqual( info[ 'username' ], self.user.username )


    def test_add_bad_request(self):
        self._bad_request( self.add_url, True )


    def test_add(self):
        text = 'test'

        addResponse = self._make_request( self.add_url, { 'text': text })
        getResponse = self._make_request( self.get_url, { 'id': addResponse[ 'id' ] })

        self.assertEqual( getResponse[ 'text' ], text )


    def test_add_multiple_bad_request(self):
        self._bad_request( self.add_multiple_url, True )


    def test_add_multiple(self):
        text1 = 'one'
        text2 = 'two'

        add = self._make_request( self.add_multiple_url, { 'text[]': [ text1, text2 ] })

        response1 = self._make_request( self.get_url, { 'id': add[ 'id[]' ][ 0 ] })
        response2 = self._make_request( self.get_url, { 'id': add[ 'id[]' ][ 1 ] })

        self.assertEqual( response1[ 'text' ], text1 )
        self.assertEqual( response2[ 'text' ], text2 )


    def test_get_bad_request(self):
        self._bad_request( self.get_url, True )

            # test with an invalid 'id'
        get = self.client.post( self.get_url,
            {
                'api_key': self.api_key,
                'id': 'invalid'
            })
        self.assertEqual( get.status_code, 400 )

            # test with a non-existent 'id'
        get = self.client.post( self.get_url,
            {
                'api_key': self.api_key,
                'id': 0
            })
        self.assertEqual( get.status_code, 400 )


    def test_get(self):
        text = 'test'

        add = self._make_request( self.add_url, { 'text': text } )
        get = self._make_request( self.get_url, { 'id': add[ 'id' ] } )

        self.assertEqual( get[ 'text' ], text )


    def test_get_multiple_bad_request(self):
        self._bad_request( self.get_multiple_url, True )

            # test with an invalid 'id'
        get = self.client.post( self.get_url,
            {
                'api_key': self.api_key,
                'id[]': [ 0, 'invalid' ]
            })
        self.assertEqual( get.status_code, 400 )

            # test with a non-existent 'id'
        get = self.client.post( self.get_url,
            {
                'api_key': self.api_key,
                'id[]': [ 0, 1 ]
            })
        self.assertEqual( get.status_code, 400 )


    def test_get_multiple(self):
        text = [ 'one', 'two', 'three' ]

        add = self._make_request( self.add_multiple_url, { 'text[]': text } )
        get = self._make_request( self.get_multiple_url, { 'id[]': add[  'id[]' ] } )

        for position, post in enumerate( get[ 'post[]' ] ):
            self.assertEqual( text[ position ], post[ 'text' ] )


    def test_get_all_bad_request(self):
        self._bad_request( self.get_all_url, False )


    def test_get_all(self):
            # should be empty
        allResponse = self._make_request( self.get_all_url )
        self.assertEqual( len( allResponse[ 'post[]' ] ), 0 )

            # add some posts
        count = 5

        for number in range( count ):
            self._make_request( self.add_url, { 'text': number })

            # confirm that we get all the added posts
        allResponse = self._make_request( self.get_all_url )

        self.assertEqual( len( allResponse[ 'post[]' ] ), count )


    def test_update_bad_request(self):
        self._bad_request( self.update_url, True )

        addResponse = self._make_request( self.add_url, { 'text': 'test' })
        postId = addResponse[ 'id' ]

            # has the 'id' but missing the 'text'
        response = self.client.post( self.update_url,
            {
                'api_key': self.api_key,
                'id': postId
            })
        self.assertEqual( response.status_code, 400 )


    def test_update(self):

        text = 'test'
        updated_text = 'test2'

        addResponse = self._make_request( self.add_url, { 'text': text })

        self.client.post( self.update_url,
            {
                'api_key': self.api_key,
                'text': updated_text,
                'id': addResponse[ 'id' ]
            })

        getResponse = self._make_request( self.get_url, { 'id': addResponse[ 'id' ] })

        self.assertEqual( getResponse[ 'text' ], updated_text )


    def test_update_multiple_bad_request(self):
        self._bad_request( self.update_multiple_url, True )

        add = self._make_request( self.add_multiple_url, { 'text[]': [  'a' 'b' ] } )

            # has the 'id[]' but missing the 'text[]'
        update = self.client.post( self.update_multiple_url,
            {
                'api_key': self.api_key,
                'id[]': add[ 'id[]' ]
            })
        self.assertEqual( update.status_code, 400 )


    def test_update_multiple(self):
        text = [ 'one', 'two', 'three' ]
        text_updated = [ 'um', 'dois', 'três' ]

        add = self._make_request( self.add_multiple_url, { 'text[]': text } )
        update = self.client.post( self.update_multiple_url,
            {
                'api_key': self.api_key,
                'id[]': add[ 'id[]' ],
                'text[]': text_updated
            })
        get = self._make_request( self.get_all_url )

        for position, post in enumerate( get[ 'post[]' ] ):
            self.assertEqual( post[ 'text' ], text_updated[ position ] )


    def test_delete_bad_request(self):
        self._bad_request( self.delete_url, True )


    def test_delete(self):
        add = self._make_request( self.add_url, { 'text': 'test' })

            # confirm that it was added
        get = self._make_request( self.get_all_url )
        self.assertEqual( len( get[ 'post[]' ] ), 1 )

        delete = self.client.post( self.delete_url,
            {
                'api_key': self.api_key,
                'id': add[ 'id' ]
            })
        get = self._make_request( self.get_all_url )

            # confirm that it was deleted
        self.assertEqual( len( get[ 'post[]' ] ), 0 )


    def test_delete_multiple_bad_request(self):
        self._bad_request( self.delete_multiple_url, True )


    def test_delete_multiple(self):
        text = [ 'a', 'b', 'c', 'd' ]
        length = len( text )

        add = self._make_request( self.add_multiple_url, { 'text[]': text })

            # confirm that it was added
        get = self._make_request( self.get_all_url )
        self.assertEqual( len( get[ 'post[]' ] ), length )

        removeCount = 2
        delete = self.client.post( self.delete_multiple_url,
            {
                'api_key': self.api_key,
                'id[]': add[ 'id[]' ][ :removeCount ]
            })
        get = self._make_request( self.get_all_url )

            # confirm that it was deleted
        self.assertEqual( len( get[ 'post[]' ] ), length - removeCount )


    def test_delete_all_bad_request(self):
        self._bad_request( self.delete_all_url, False )


    def test_delete_all(self):
        text = [ 1, 2, 3, 4, 5 ]
        add = self._make_request( self.add_multiple_url, { 'text[]': text })

            # confirm that it was added
        get = self._make_request( self.get_all_url )
        self.assertEqual( len( get[ 'post[]' ] ), len( text ) )

        delete = self.client.post( self.delete_all_url, { 'api_key': self.api_key } )
        get = self._make_request( self.get_all_url )

            # confirm that it was deleted
        self.assertEqual( len( get[ 'post[]' ] ), 0 )