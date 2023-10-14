"""
This module contains tests for the 'marketplace' app.

Here, you can add unit tests, integration tests, and other tests to ensure the functionality
and correctness of the 'marketplace' app.
"""

import json
from unittest.mock import patch
from django.test import TestCase, Client, SimpleTestCase
from .views import find_listing
from eth_account.messages import encode_defunct
from web3 import Web3, EthereumTesterProvider

# Create your tests here.

listings = []


class ListNFTTest(TestCase):
    """Test cases for the list_nft view in the marketplace app."""

    def setUp(self):
        self.client = Client()

    def test_list_nft_get(self):
        """Test the GET method of the list_nft view."""
        response = self.client.get("/list/")
        self.assertEqual(response.status_code, 200)

    @patch('marketplace.contracts.ERC721Contract.is_token_owner')
    def test_list_nft_post_valid_data(self, mock_is_token_owner):
        """Test the POST method of the list_nft view with valid data."""
        mock_is_token_owner.return_value = True

        data = {
            'nftCollectionAddress': 'some_address',
            'tokenId': 123,
            'erc20Address': 'some_erc20_address',
            'erc20Amount': 100.5,
            'isAuction': True,
            'ownerAddress': 'some_ethereum_address'
        }
        response = self.client.post(
            "/list/", json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_list_nft_post_invalid_data(self):
        """Test the POST method with missing required fields."""
        data = {
            'nftCollectionAddress': 'some_address',
            'isAuction': True
        }
        response = self.client.post(
            "/list/", json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_list_nft_post_not_owner(self):
        """Test POST when someone who isn't the owner tries to list."""
        data = {
            'nftCollectionAddress': 'some_address',
            'tokenId': 123,
            'erc20Address': 'some_erc20_address',
            'erc20Amount': 100.5,
            'isAuction': True,
            'ownerAddress': 'wrong_ethereum_address'
        }
        response = self.client.post(
            "/list/", json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_list_nft_disallowed_method(self):
        """Test using an unsupported method (PUT)."""
        response = self.client.put("/list/")
        self.assertEqual(response.status_code, 405)


class TestFindListingFunction(SimpleTestCase):
    """
    Test cases for the `find_listing` function.
    """

    def setUp(self):
        """Set up common resources for testing."""
        self.listings = [
            {
                "saleId": 1,
                "collectionAddress": "address_1",
                "tokenId": 123,
                "price": 100.5,
                "isAuction": True,
                "ownerAddress": "owner_1"
            },
            {
                "saleId": 2,
                "collectionAddress": "address_2",
                "tokenId": 456,
                "price": 200.5,
                "isAuction": False,
                "ownerAddress": "owner_2"
            }
        ]

    def test_find_listing_found(self):
        """Test the case when the listing is successfully found."""
        with patch('marketplace.views.listings', new=self.listings):
            # Assuming 1 is the sale_id of the first listing
            result = find_listing(1)
        self.assertEqual(result, self.listings[0])

    def test_find_listing_not_found(self):
        """Test the case when the listing is not found."""
        result = find_listing(999)  # Using an unexisting sale_id
        self.assertIsNone(result)

    def test_find_listing_empty_list(self):
        """Test the case when the listings list is empty."""
        with patch('marketplace.views.listings', new=[]):  # Empty the list
            result = find_listing(1)
        self.assertIsNone(result)


class PurchaseOrderTestCase(TestCase):

    def setUp(self):
        """Set up common resources for testing."""
        self.listings = [{"saleId": 1,
                          "nftCollectionAddress": "0xFCE9b92eC11680898c7FE57C4dDCea83AeabA3ff",
                          "tokenId": 123,
                          "erc20Address": "0xbd65c58D6F46d5c682Bf2f36306D461e3561C747",
                          "erc20_amount": 10000000000000000,
                          "isAuction": False,
                          "ownerAddress": "0x929A4DfC610963246644b1A7f6D1aed40a27dD2f",
                          "purchaseAt": ""},
                         ]

        self.valid_data = {
            'nftCollectionAddress': '0xFCE9b92eC11680898c7FE57C4dDCea83AeabA3ff',
            'tokenId': 1,
            'erc20Address': '0xbd65c58D6F46d5c682Bf2f36306D461e3561C747',
            'erc20Amount': 10000000000000000,
            'bidderSig': '',
            'buyerAddress': '0x929A4DfC610963246644b1A7f6D1aed40a27dD2f',
            "saleId": 1,
        }

    def test_valid_purchase(self, ):
        with patch('marketplace.views.listings', new=self.listings):
            w3 = Web3(EthereumTesterProvider())
            acct = w3.eth.account.create()
            private_key = acct.key
            address = acct.address

            message = w3.solidity_keccak(['address',
                                          'address',
                                          'uint256',
                                          'uint256'],
                                         [self.valid_data.get('nftCollectionAddress'),
                                          self.valid_data.get('erc20Address'),
                                          self.valid_data.get('tokenId'),
                                          self.valid_data.get('erc20Amount')])

            signable_message = encode_defunct(hexstr=message.hex())
            signature = w3.eth.account.sign_message(
                signable_message, private_key=private_key)

            self.valid_data.update({'bidderSig': signature.signature.hex()})
            self.valid_data.update({'buyerAddress': address})

            print("self.valid_data: ", self.valid_data)
            response = self.client.post(
                '/purchaseOrder/',
                json.dumps(self.valid_data),
                content_type='application/json')

            self.assertEqual(response.status_code, 200)
            self.assertIn("Purchase initiated", response.json()["message"])


class SettlePurchaseOrderTestCase(TestCase):

    def setUp(self):
        """Set up common resources for testing."""
        self.valid_data = {
            'nftCollectionAddress': '0xFCE9b92eC11680898c7FE57C4dDCea83AeabA3ff',
            'tokenId': 1,
            'erc20Address': '0xbd65c58D6F46d5c682Bf2f36306D461e3561C747',
            'erc20Amount': 10000000000000000,
            'bidderSig': '',
            'buyerAddress': '0x929A4DfC610963246644b1A7f6D1aed40a27dD2f',
            "saleId": 1,
        }

        self.w3 = Web3(EthereumTesterProvider())
        self.buyer_acct = self.w3.eth.account.create()
        self.buyer_private_key = self.buyer_acct.key
        self.buyer_address = self.buyer_acct.address

        self.artist_acct = self.w3.eth.account.create()
        self.artist_private_key = self.artist_acct.key
        self.artist_address = self.artist_acct.address

        self.message = self.w3.solidity_keccak(['address',
                                                'address',
                                                'uint256',
                                                'uint256'],
                                               [self.valid_data.get('nftCollectionAddress'),
                                                self.valid_data.get('erc20Address'),
                                                self.valid_data.get('tokenId'),
                                                self.valid_data.get('erc20Amount')])

        self.signable_message = encode_defunct(hexstr=self.message.hex())
        self.buyer_signature = self.w3.eth.account.sign_message(
            self.signable_message, private_key=self.buyer_private_key)

        self.purchasesIntents = [
            {
                "saleId": 1,
                "nftCollectionAddress": "0xFCE9b92eC11680898c7FE57C4dDCea83AeabA3ff",
                "tokenId": 1,
                "erc20Address": "0xbd65c58D6F46d5c682Bf2f36306D461e3561C747",
                "erc20_amount": 10000000000000000,
                "buyerSig": self.buyer_signature.signature.hex(),
                "buyerAddress": self.buyer_address},
        ]

    def test_valid_purchase(self, ):
        with patch('marketplace.views.purchase_intents', new=self.purchasesIntents):
            self.buyer_signature_hash = self.w3.solidity_keccak(
                ['bytes'], [self.buyer_signature.signature.hex()])

            self.signable_buyer_signature_hash = encode_defunct(
                hexstr=self.buyer_signature_hash.hex())
            self.artist_signature = self.w3.eth.account.sign_message(
                self.signable_buyer_signature_hash, private_key=self.artist_private_key)

            self.body_data = {
                "sale_id": 1,
                "owner_approval_sig": self.artist_signature.signature.hex(),
                "owner_address": self.artist_address
            }

            response = self.client.post(
                '/settlePurchaseOrder/',
                json.dumps(self.body_data),
                content_type='application/json')

            self.assertIn(
                "Transaction successful created.",
                response.json()["message"])
            self.assertEqual(response.status_code, 200)


class BidOrderTestCase(TestCase):

    def setUp(self):
        """Set up common resources for testing."""
        self.listings = [{
            "saleId": 1,
            "nftCollectionAddress": "0xFCE9b92eC11680898c7FE57C4dDCea83AeabA3ff",
            "tokenId": 123,
            "erc20Address": "0xbd65c58D6F46d5c682Bf2f36306D461e3561C747",
            "erc20_amount": 10000000000000000,
            "isAuction": True,
            "ownerAddress": "0x929A4DfC610963246644b1A7f6D1aed40a27dD2f",
            "purchaseAt": ""
        }]

        self.valid_bid_data = {
            'nftCollectionAddress': '0xFCE9b92eC11680898c7FE57C4dDCea83AeabA3ff',
            'tokenId': 123,
            'erc20Address': '0xbd65c58D6F46d5c682Bf2f36306D461e3561C747',
            'erc20Amount': 10500000000000000,  # slightly higher than the listing
            'bidderSig': '0xa27c14e79bc6bd9841a88baf96f05cc3c60dd3f53dca8f11276487c624491c88304730150886c9601efbe1b507eb459405de36472fd3c72a89903e9fd9a7db761b',
            'buyerAddress': '0x929A4DfC610963246644b1A7f6D1aed40a27dD2f',
            "saleId": 1,
        }

    def test_valid_bid(self, ):
        with patch('marketplace.views.listings', new=self.listings):
            w3 = Web3(EthereumTesterProvider())
            acct = w3.eth.account.create()
            private_key = acct.key
            address = acct.address

            message = w3.solidity_keccak(['address',
                                          'address',
                                          'uint256',
                                          'uint256'],
                                         [self.valid_bid_data.get('nftCollectionAddress'),
                                          self.valid_bid_data.get('erc20Address'),
                                          self.valid_bid_data.get('tokenId'),
                                          self.valid_bid_data.get('erc20Amount')])

            signable_message = encode_defunct(hexstr=message.hex())
            signature = w3.eth.account.sign_message(
                signable_message, private_key=private_key)

            self.valid_bid_data.update(
                {'bidderSig': signature.signature.hex()})
            self.valid_bid_data.update({'buyerAddress': address})

            print("self.valid_bid_data: ", self.valid_bid_data)
            response = self.client.post(
                '/bidOrder/',  # Assuming this is the correct endpoint
                json.dumps(self.valid_bid_data),
                content_type='application/json')

            self.assertEqual(response.status_code, 200)
            self.assertIn("Bid placed", response.json()["message"])

    def test_missing_fields(self):
        del self.valid_bid_data['tokenId']
        response = self.client.post(
            '/bidOrder/',
            json.dumps(self.valid_bid_data),
            content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_listing_not_found(self):
        with patch('marketplace.views.listings', new=self.listings):
            self.valid_bid_data.update({'saleId': 2})
            response = self.client.post(
                '/bidOrder/',
                json.dumps(self.valid_bid_data),
                content_type='application/json')
            self.assertEqual(response.json()["error"], "Listing not found")
            self.assertEqual(response.status_code, 404)

    def test_auction_already_settled(self):
        with patch('marketplace.views.listings', new=self.listings):
            self.listings[0].update({'purchaseAt': "2023-01-01"})
            response = self.client.post(
                '/bidOrder/',
                json.dumps(self.valid_bid_data),
                content_type='application/json')
            self.assertEqual(
                response.json()["error"],
                "Auction already settled")
            self.assertEqual(response.status_code, 400)

    def test_listing_not_for_auction(self):
        with patch('marketplace.views.listings', new=self.listings):
            self.listings[0].update({'isAuction': False})
            response = self.client.post(
                '/bidOrder/',
                json.dumps(self.valid_bid_data),
                content_type='application/json')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json()["error"],
                "Listing is not for auction.")

    def test_bid_must_be_higher_than_current_bid(self):
        # Mock the listing
        mocked_bid = self.valid_bid_data
        mocked_bid.update({'erc20Amount': 10300000000000000})

        mocked_bid_intents = {}

        mocked_bid_intents.setdefault(self.valid_bid_data.get(
            "saleId"), []).append(self.valid_bid_data)

        with patch('marketplace.views.bid_intents', new=mocked_bid_intents), \
                patch('marketplace.views.listings', new=self.listings):

            response = self.client.post(
                '/bidOrder/',
                json.dumps(mocked_bid),
                content_type='application/json'
            )
            print("mocked_bid_intents:::::::", mocked_bid_intents)
            self.assertEqual(
                response.json()["error"],
                "Bid must be higher than the current bid"
            )
            self.assertEqual(response.status_code, 400)

    def test_bid_must_be_higher_than_current_bid(self):
        # Mock the listing
        mocked_bid = {
            'nftCollectionAddress': '0xFCE9b92eC11680898c7FE57C4dDCea83AeabA3ff',
            'tokenId': 123,
            'erc20Address': '0xbd65c58D6F46d5c682Bf2f36306D461e3561C747',
            'erc20Amount': 10700000000000000,  # slightly higher than the listing
            'bidderSig': '',
            'buyerAddress': '',
            "saleId": 1,
        }

        w3 = Web3(EthereumTesterProvider())
        acct = w3.eth.account.create()
        private_key = acct.key
        address = acct.address

        message = w3.solidity_keccak(['address',
                                      'address',
                                      'uint256',
                                      'uint256'],
                                     [mocked_bid.get('nftCollectionAddress'),
                                         mocked_bid.get('erc20Address'),
                                         mocked_bid.get('tokenId'),
                                         mocked_bid.get('erc20Amount')])

        signable_message = encode_defunct(hexstr=message.hex())
        signature = w3.eth.account.sign_message(
            signable_message, private_key=private_key)

        mocked_bid.update(
            {'bidderSig': signature.signature.hex()})
        mocked_bid.update({'buyerAddress': address})

        mocked_bid_intents = {}

        mocked_bid_intents.setdefault(self.valid_bid_data.get(
            "saleId"), []).append(self.valid_bid_data)

        with patch('marketplace.views.bid_intents', new=mocked_bid_intents), \
                patch('marketplace.views.listings', new=self.listings):

            self.assertEqual(len(mocked_bid_intents[self.valid_bid_data.get(
                "saleId")]), 1)
            response = self.client.post(
                '/bidOrder/',
                json.dumps(mocked_bid),
                content_type='application/json'
            )
            print("mocked_bid_intents:::::::", mocked_bid_intents)
            self.assertEqual(len(mocked_bid_intents[self.valid_bid_data.get(
                "saleId")]), 2)
            self.assertIn("Bid placed", response.json()["message"])
            self.assertEqual(response.status_code, 200)

class SettleAuctionOrderTestCase(TestCase):

    def setUp(self):
        """Set up common resources for testing."""
        self.valid_data = {
            'nftCollectionAddress': '0xFCE9b92eC11680898c7FE57C4dDCea83AeabA3ff',
            'tokenId': 1,
            'erc20Address': '0xbd65c58D6F46d5c682Bf2f36306D461e3561C747',
            'erc20Amount': 10000000000000000,
            'bidderSig': '',
            'buyerAddress': '0x929A4DfC610963246644b1A7f6D1aed40a27dD2f',
            "saleId": 1,
        }

        self.w3 = Web3(EthereumTesterProvider())
        self.bidder_acct = self.w3.eth.account.create()
        self.bidder_private_key = self.bidder_acct.key
        self.bidder_address = self.bidder_acct.address

        self.owner_acct = self.w3.eth.account.create()
        self.owner_private_key = self.owner_acct.key
        self.owner_address = self.owner_acct.address

        self.message = self.w3.solidity_keccak(['address',
                                                'address',
                                                'uint256',
                                                'uint256'],
                                               [self.valid_data.get('nftCollectionAddress'),
                                                self.valid_data.get('erc20Address'),
                                                self.valid_data.get('tokenId'),
                                                self.valid_data.get('erc20Amount')])

        self.signable_message = encode_defunct(hexstr=self.message.hex())
        self.bidder_signature = self.w3.eth.account.sign_message(
            self.signable_message, private_key=self.bidder_private_key)

        self.bid_intents = [
            {
                "saleId": 1,
                "nftCollectionAddress": "0xFCE9b92eC11680898c7FE57C4dDCea83AeabA3ff",
                "tokenId": 1,
                "erc20Address": "0xbd65c58D6F46d5c682Bf2f36306D461e3561C747",
                "erc20Amount": 10000000000000000,
                "bidderSig": self.bidder_signature.signature.hex(),
                "bidderAddress": self.bidder_address
            },
        ]

    def test_valid_auction_settlement(self):
        with patch('marketplace.views.bid_intents', new=self.bid_intents):
            self.bidder_signature_hash = self.w3.solidity_keccak(
                ['bytes'], [self.bidder_signature.signature.hex()])

            self.signable_bidder_signature_hash = encode_defunct(
                hexstr=self.bidder_signature_hash.hex())
            self.owner_signature = self.w3.eth.account.sign_message(
                self.signable_bidder_signature_hash, private_key=self.owner_private_key)

            self.body_data = {
                "sale_id": 1,
                "owner_approval_sig": self.owner_signature.signature.hex(),
                "owner_address": self.owner_address
            }

            response = self.client.post(
                '/settleAuctionOrder/',  # Assuming this is the correct endpoint
                json.dumps(self.body_data),
                content_type='application/json')

            self.assertIn(
                "Transaction successfully created.",
                response.json()["message"])
            self.assertEqual(response.status_code, 200)