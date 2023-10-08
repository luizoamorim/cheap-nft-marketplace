"""
This module contains tests for the 'marketplace' app.

Here, you can add unit tests, integration tests, and other tests to ensure the functionality 
and correctness of the 'marketplace' app.
"""

import json
from django.test import TestCase, Client

# Create your tests here.
class ListNFTTest(TestCase):
    """
    Test cases for the list_nft view in the marketplace app.
    """

    def setUp(self):
        self.client = Client()

    def test_list_nft_get(self):
        """
        Test the GET method of the list_nft view.
        Ensure it returns a 200 status code for successful retrieval.
        """
        response = self.client.get("/list/")
        self.assertEqual(response.status_code, 200)

    def test_list_nft_post_valid_data(self):
        """
        Test the POST method of the list_nft view with valid data.
        Ensure it returns a 201 status code for successful creation.
        """
        data = {
          'collectionAddress': 'some_address',
          'tokenId': 123,
          'price': 100.5,
          'isAuction': True
        }
        response = self.client.post("/list/", json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)  # Assuming you return 201 for created

    def test_list_nft_post_invalid_data(self):
        """
        Test the POST method of the list_nft view with missing required fields.
        Ensure it returns a 400 status code for bad request.
        """
        data = {
            'collectionAddress': 'some_address',
            # Missing tokenId and price
            'isAuction': True
        }
        response = self.client.post('/list/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_list_nft_disallowed_method(self):
        """
        Test using an unsupported method (PUT) for the list_nft view.
        Ensure it returns a 405 status code for method not allowed.
        """
        response = self.client.put('/list/')  # Trying PUT method, which should be disallowed
        self.assertEqual(response.status_code, 405)
