from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

import json

from todolist import views

class TodolistTest( TestCase ):
    def setUp(self):

            # create a user
        userModel = get_user_model()

        self.user = userModel.objects.create_user( username= 'test', email= 'test@test.pt', password= 'test' )
        self.api_key = self.user.api_key

            # add a client
        self.client = Client()

            # get the api's urls
        self.add_url = reverse( views.add_post )
        self.all_url = reverse( views.all_posts )
        self.get_url = reverse( views.single_post )
        self.update_url = reverse( views.update_post )
        self.delete_url = reverse( views.delete_post )

    def make_request(self, url, arguments):

            # the api_key is needed for all requests
        arguments[ 'api_key' ] = self.api_key

        response = self.client.post( url, arguments )

        return json.loads( response.content.decode( encoding= 'utf-8' ) )


    def test_add_bad_request(self):
        """
            Call with missing/wrong arguments to test if it is returned with status code of 400 (bad request)
        """

            # no arguments
        response = self.client.post( self.add_url )

        self.assertEqual( response.status_code, 400 )

            # invalid 'api_key'
        response = self.client.post( self.add_url,
            {
                'api_key': 'random'
            })

        self.assertEqual( response.status_code, 400 )

            # missing 'text' argument
        response = self.client.post( self.add_url,
            {
                'api_key': self.api_key
            })

        self.assertEqual( response.status_code, 400 )


    def test_add(self):

        text = 'test'

        addResponse = self.make_request( self.add_url,
            {
                'text': text
            })

        getResponse = self.make_request( self.get_url,
            {
                'id': addResponse[ 'id' ]
            })

        self.assertEqual( getResponse[ 'text' ], text )


    def test_update_bad_request(self):

        addResponse = self.make_request( self.add_url,
            {
                'text': 'test'
            })
        postId = addResponse[ 'id' ]


            # no arguments
        response = self.client.post( self.update_url )

        self.assertEqual( response.status_code, 400 )

            # invalid 'api_key'
        response = self.client.post( self.update_url,
            {
                'api_key': 'random'
            })

        self.assertEqual( response.status_code, 400 )

            # missing 'id'

        response = self.client.post( self.update_url,
            {
                'api_key': self.api_key
            })

        self.assertEqual( response.status_code, 400 )

            # missing 'text'

        response = self.client.post( self.update_url,
            {
                'api_key': self.api_key,
                'id': postId
            })

        self.assertEqual( response.status_code, 400 )


    def test_update(self):

        text = 'test'
        updated_text = 'test2'

        addResponse = self.make_request( self.add_url,
            {
                'text': text
            })

        self.make_request( self.update_url,
            {
                'text': updated_text,
                'id': addResponse[ 'id' ]
            })

        getResponse = self.make_request( self.get_url,
            {
                'id': addResponse[ 'id' ]
            })

        self.assertEqual( getResponse[ 'text' ], updated_text )


    def test_all_bad_request(self):

            # missing 'api_key'
        response = self.client.post( self.all_url )

        self.assertEqual( response.status_code, 400 )

            # invalid 'api_key'
        response = self.client.post( self.all_url,
            {
                'api_key': 'random'
            })

        self.assertEqual( response.status_code, 400 )


    def test_all(self):

        allResponse = self.make_request( self.all_url, {} )

        self.assertEqual( len( allResponse ), 0 )

        count = 5

        for number in range( count ):
            self.make_request( self.add_url,
                {
                    'text': number
                })

        allResponse = self.make_request( self.all_url, {} )

        self.assertEqual( len( allResponse ), count )


    def test_delete_bad_request(self):

            # no arguments
        response = self.client.post( self.delete_url )

        self.assertEqual( response.status_code, 400 )

            # invalid 'api_key'
        response = self.client.post( self.delete_url,
            {
                'api_key': 'random'
            })

        self.assertEqual( response.status_code, 400 )

            # missing 'id'
        response = self.client.post( self.delete_url,
            {
                'api_key': self.api_key
            })

        self.assertEqual( response.status_code, 400 )


    def test_delete(self):

        addResponse = self.make_request( self.add_url,
            {
                'text': 'test'
            })

        self.make_request( self.delete_url,
            {
                'id': addResponse[ 'id' ]
            })

        allResponse = self.make_request( self.all_url, {} )

        self.assertEqual( len( allResponse ), 0 )

