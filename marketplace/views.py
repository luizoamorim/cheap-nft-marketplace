"""
This module contains views for the NFT marketplace.

It provides endpoints for listing NFTs, retrieving listed NFTs, and other related functionalities.
"""

import json
import os

from datetime import datetime
from decouple import config
from eth_account.messages import encode_defunct
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pydantic import ValidationError
from web3 import Web3

from .contracts import ERC721Contract
from .contracts import MarketplaceContract
from .models import NFTListing, NFTPurchaseIntent, NFTSettle

# In-memory data structure
sales = 0
listings = []
purchase_intents = []
bid_intents = {}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def find_listing(sale_id):
    """
    Find a specific NFT listing based on the sale ID.

    Args:
    - sale_id (int): The listing identifier.

    Returns:
    - dict: The details of the NFT listing if found. Otherwise, returns None.
    """
    for listing in listings:
        if listing.get("sale_id") == sale_id:
            return listing
    return None


def find_purchase_intents(sale_id):
    """
    Find a specific NFT listing based on the sale ID.

    Args:
    - sale_id (int): The listing identifier.

    Returns:
    - dict: The details of the NFT listing if found. Otherwise, returns None.
    """
    for purchase_intent in purchase_intents:
        if purchase_intent.get("sale_id") == sale_id:
            return purchase_intent
    return None

# Create your views here.


@csrf_exempt
def list_nft(request):
    """
    Handle the listing of NFTs.

    If the request method is POST, it expects a JSON body with details about the NFT
    to be listed, such as collectionAddress, tokenId, price, and isAuction.
    The NFT details are then added to an in-memory listing.

    If the request method is GET, it returns a JSON response with all the current NFT listings.

    Args:
    - request (HttpRequest): The Django request object.

    Returns:
    - JsonResponse: A JSON response containing either a success message and status code
      or an error message and status code.
    """
    global sales

    if request.method == "POST":
        data = json.loads(request.body)

        try:
            validated_data = NFTListing(**data)
            # Extracting details from the received data
            nft_collection_address = validated_data.nft_collection_address
            token_id = validated_data.tokenId
            erc20_address = validated_data.erc20Address
            erc20_amount = validated_data.erc20_amount
            is_auction = validated_data.isAuction
            owner_address = validated_data.ownerAddress

            # If validation passes, add the data to your in-memory listings

            # Check if all required details are provided
            if not all([nft_collection_address, token_id,
                       erc20_address, erc20_amount, owner_address]):
                return JsonResponse(
                    {"error": "Missing required fields"}, status=400)

            # Assuming you have a function `is_token_owner` to check if the NFT owner matches
            # the given Ethereum address
            erc721 = ERC721Contract()

            if not erc721.is_token_owner(owner_address, token_id):
                return JsonResponse(
                    {"error": "Not the token owner"}, status=400)

            sales += 1

            # Add to our in-memory listings
            listings.append(
                {
                    "sale_id": sales,
                    "nft_collection_address": nft_collection_address,
                    "tokenId": token_id,
                    "erc20Address": erc20_address,
                    "erc20_amount": erc20_amount,
                    "isAuction": is_auction,
                    "ownerAddress": owner_address,
                    "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "purchaseAt": ""
                }
            )

            return JsonResponse(
                {"message": "Listing added successfully", "sale_id": sales}, status=201)

        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == "GET":
        return JsonResponse(listings, safe=False)

    else:
        return HttpResponse(status=405)


@csrf_exempt
def purchase_order(request):
    """
    Handle the purchase of NFT.
    """
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            validated_data = NFTPurchaseIntent(**data)

            nft_collection_address = validated_data.nft_collection_address
            token_id = validated_data.tokenId
            erc20_address = validated_data.erc20Address
            erc20_amount = validated_data.erc20_amount
            bidder_sig = validated_data.bidderSig
            buyer_address = validated_data.buyerAddress
            sale_id = validated_data.sale_id

            # Check if all required details are provided
            if not all([nft_collection_address,
                        token_id,
                        erc20_address,
                        erc20_amount,
                        bidder_sig,
                        buyer_address,
                        sale_id]):
                return JsonResponse(
                    {"error": "Missing required fields"}, status=400)

            # Ensure the listing exists
            listing = find_listing(sale_id)

            if not listing:
                return JsonResponse({"error": "Listing not found"}, status=404)

            if listing["isAuction"]:
                # Ensure the listing is an auction
                return JsonResponse(
                    {"error": "Listing is not a traditional purchase"}, status=400)

            # should not be able to add a new purchase if already exist an
            # intent with the sale_id
            for intent in purchase_intents:
                if intent["sale_id"] == sale_id:
                    return JsonResponse(
                        {"error": "Purchase intent already exist"}, status=400)

            # The purchase intent amount must be equal to the listing price
            if listing["erc20_amount"] != erc20_amount:
                return JsonResponse(
                    {"error":
                     "Purchase intent amount must be equal to the listing price"
                     },
                    status=400
                )

            # Create a web3 instance
            w3_instance = Web3(Web3.HTTPProvider(config("PROVIDER_URL")))

            # Recreate the message hash
            message = w3_instance.solidity_keccak(
                ['address', 'address', 'uint256', 'uint256'],
                [nft_collection_address, erc20_address, token_id, int(
                    erc20_amount)]
            )

            # Encode the message and recover the buyer signature
            signable_message = encode_defunct(hexstr=message.hex())
            recovered_bidder_address = w3_instance.eth.account.recover_message(
                signable_message,
                signature=bidder_sig
            )

            # Ensure recovered address matches provided buyer address
            if recovered_bidder_address != buyer_address:
                return JsonResponse(
                    {"error": "Signature does not match the provided buyer address."}, status=400)

            # Construct purchase data
            purchase_intent = {
                "sale_id": sale_id,
                "nft_collection_address": listing["nft_collection_address"],
                "tokenId": listing["tokenId"],
                "erc20Address": listing["erc20Address"],
                "erc20_amount": erc20_amount,
                "buyerSig": bidder_sig,
                "buyerAddress": buyer_address,
                "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            purchase_intents.append(purchase_intent)

            return JsonResponse({"message": "Purchase initiated"}, status=200)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

    else:
        return HttpResponse(status=405)


def bid_order(request):
    """
    Handle the bidding of NFT.
    """
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            validated_data = NFTPurchaseIntent(**data)

            nft_collection_address = validated_data.nft_collection_address
            token_id = validated_data.tokenId
            erc20_address = validated_data.erc20Address
            erc20_amount = validated_data.erc20_amount
            bidder_sig = validated_data.bidderSig
            buyer_address = validated_data.buyerAddress
            sale_id = validated_data.sale_id

            # Check if all required details are provided
            if not all([nft_collection_address,
                        token_id,
                        erc20_address,
                        erc20_amount,
                        bidder_sig,
                        buyer_address,
                        sale_id]):
                return JsonResponse(
                    {"error": "Missing required fields"}, status=400)

            # Ensure the listing exists
            listing = find_listing(sale_id)

            if not listing:
                # Ensure the listing exists
                return JsonResponse({"error": "Listing not found"}, status=404)

            if listing["purchaseAt"]:
                # Ensure the auction was not settled
                return JsonResponse(
                    {"error": "Auction already settled"}, status=400)

            if not listing["isAuction"]:
                # Ensure the listing is an auction
                return JsonResponse(
                    {"error": "Listing is not for auction."}, status=400)

            # Check if the auction has already started
            latest_bid = bid_intents[sale_id][- 1] if sale_id in bid_intents else None

            if latest_bid and latest_bid["erc20_amount"] >= erc20_amount:
                # Ensure the bid is higher than the current bid
                return JsonResponse(
                    {"error": "Bid must be higher than the current bid"}, status=400
                )

            # Create a web3 instance
            w3_instance = Web3(Web3.HTTPProvider(config("PROVIDER_URL")))

            # Recreate the message hash
            message = w3_instance.solidity_keccak(
                ['address', 'address', 'uint256', 'uint256'],
                [nft_collection_address, erc20_address, token_id, int(
                    erc20_amount)]
            )

            # Encode the message and recover the buyer signature
            signable_message = encode_defunct(hexstr=message.hex())
            recovered_bidder_address = w3_instance.eth.account.recover_message(
                signable_message,
                signature=bidder_sig
            )

            # Ensure recovered address matches provided buyer address
            if recovered_bidder_address != buyer_address:
                return JsonResponse(
                    {"error": "Signature does not match the provided buyer address."}, status=400)

            # Construct auction data
            bid_intent = {
                "sale_id": listing["sale_id"],
                "nft_collection_address": listing["nft_collection_address"],
                "erc20Address": listing["erc20Address"],
                "tokenId": listing["tokenId"],
                "erc20_amount": erc20_amount,
                "bidderSig": bidder_sig,
                "bidderAddress": buyer_address,
                "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            bid_intents.setdefault(sale_id, []).append(bid_intent)

            return JsonResponse({"message": "Bid placed"}, status=200)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

    else:
        return HttpResponse(status=405)


@csrf_exempt
def settle_purchase_order(request):
    """
    Handle the settlement of NFT.
    """
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            validated_data = NFTSettle(**data)

            sale_id = validated_data.sale_id
            owner_approval_sig = validated_data.owner_approval_sig
            owner_address = validated_data.owner_address

            # Check if all required details are provided
            if not all([sale_id,
                        owner_approval_sig,
                        owner_address]):
                return JsonResponse(
                    {"error": "Missing required fields"}, status=400)

            purchase_intent = find_purchase_intents(sale_id)

            if not purchase_intent:
                # Ensure the listing exists
                return JsonResponse(
                    {"error": "No purchase intent for this token id"}, status=404)

            # Create a web3 instance
            w3_instance = Web3(Web3.HTTPProvider(config("PROVIDER_URL")))

            # Recreate the message hash
            message = w3_instance.solidity_keccak(['address',
                                                   'address',
                                                   'uint256',
                                                   'uint256'],
                                                  [purchase_intent["nft_collection_address"],
                                                   purchase_intent["erc20Address"],
                                                   purchase_intent["tokenId"],
                                                   int(purchase_intent["erc20_amount"])])

            # Encode the message and recover the buyer signature
            signable_message = encode_defunct(hexstr=message.hex())

            recovered_bidder_address = w3_instance.eth.account.recover_message(
                signable_message,
                signature=purchase_intent["buyerSig"]
            )

            # Ensure recovered address matches provided buyer address
            if recovered_bidder_address != purchase_intent["buyerAddress"]:
                return JsonResponse(
                    {"error": "Signature does not match the provided buyer address."}, status=404)

            # Hash the bidder's signature
            hashed_bidder_sig = w3_instance.solidity_keccak(
                ['bytes'], [purchase_intent["buyerSig"]])

            # Encode the message and recover the buyer signature
            signable_message = encode_defunct(hexstr=hashed_bidder_sig.hex())

            if isinstance(owner_approval_sig,
                          tuple) and len(owner_approval_sig) == 1:
                owner_approval_sig = owner_approval_sig[0]

            recovered_owner_address = w3_instance.eth.account.recover_message(
                signable_message,
                signature=owner_approval_sig
            )

            if recovered_owner_address != owner_address:
                return JsonResponse(
                    {"error": "Signature does not match the provided owner address."}, status=404)

            marketplace_contract = MarketplaceContract()
            tx_hash = marketplace_contract.send_transaction(
                purchase_intent["nft_collection_address"],
                purchase_intent["tokenId"],
                purchase_intent["erc20Address"],
                purchase_intent["erc20_amount"],
                purchase_intent["buyerSig"],
                owner_approval_sig,
                owner_address)

            return JsonResponse({
                "message": "Transaction successful created.",
                "txHash": tx_hash
            },
                status=200
            )
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)


def settle_auction_order(request):
    """
    Handle the settlement of NFT auction.
    """
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            validated_data = NFTSettle(**data)

            sale_id = validated_data.sale_id
            owner_approval_sig = validated_data.owner_approval_sig
            owner_address = validated_data.owner_address

            if not all([sale_id, owner_approval_sig, owner_address]):
                return JsonResponse(
                    {"error": "Missing required fields"}, status=400)

            # Extract the latest bid for the given sale_id
            print("bid_intents: ", bid_intents)
            bids_for_sale = bid_intents.get(sale_id)
            print("BID_FOR_SALE: ", bids_for_sale)
            if not bids_for_sale:
                return JsonResponse(
                    {"error": "No bids for this sale id"}, status=404)

            latest_bid = bids_for_sale[-1]

            w3_instance = Web3(Web3.HTTPProvider(config("PROVIDER_URL")))

            message = w3_instance.solidity_keccak(['address',
                                                   'address',
                                                   'uint256',
                                                   'uint256'],
                                                  [latest_bid["nft_collection_address"],
                                                   latest_bid["erc20Address"],
                                                   latest_bid["tokenId"],
                                                   int(latest_bid["erc20_amount"])])

            signable_message = encode_defunct(hexstr=message.hex())

            recovered_bidder_address = w3_instance.eth.account.recover_message(
                signable_message,
                signature=latest_bid["bidderSig"]
            )

            if recovered_bidder_address != latest_bid["bidderAddress"]:
                return JsonResponse(
                    {"error": "Signature does not match the provided bidder address."}, status=404)

            hashed_bidder_sig = w3_instance.solidity_keccak(
                ['bytes'], [latest_bid["bidderSig"]])
            signable_message = encode_defunct(hexstr=hashed_bidder_sig.hex())

            if isinstance(owner_approval_sig,
                          tuple) and len(owner_approval_sig) == 1:
                owner_approval_sig = owner_approval_sig[0]

            recovered_owner_address = w3_instance.eth.account.recover_message(
                signable_message,
                signature=owner_approval_sig
            )

            if recovered_owner_address != owner_address:
                return JsonResponse(
                    {"error": "Signature does not match the provided owner address."}, status=404)

            marketplace_contract = MarketplaceContract()
            tx_hash = marketplace_contract.send_transaction(
                latest_bid["nft_collection_address"],
                latest_bid["tokenId"],
                latest_bid["erc20Address"],
                latest_bid["erc20_amount"],
                latest_bid["bidderSig"],
                owner_approval_sig,
                owner_address)

            return JsonResponse({
                "message": "Transaction successfully created.",
                "txHash": tx_hash
            },
                status=200
            )
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
