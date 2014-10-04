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


    def test_add(self):

        text = 'test'

        addResponse = self.make_request( self.add_url,
            {
                'text': text
            })

        getResponse = self.make_request( self.get_url,
            {
                'pk': addResponse[ 'pk' ]
            })

        self.assertEqual( getResponse[ 'text' ], text )


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
                'pk': addResponse[ 'pk' ]
            })

        getResponse = self.make_request( self.get_url,
            {
                'pk': addResponse[ 'pk' ]
            })

        self.assertEqual( getResponse[ 'text' ], updated_text )


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


    def test_delete(self):

        addResponse = self.make_request( self.add_url,
            {
                'text': 'test'
            })

        self.make_request( self.delete_url,
            {
                'pk': addResponse[ 'pk' ]
            })

        allResponse = self.make_request( self.all_url, {} )

        self.assertEqual( len( allResponse ), 0 )

