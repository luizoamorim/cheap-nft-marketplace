"""
This module contains views for the NFT marketplace.

It provides endpoints for listing NFTs, retrieving listed NFTs, and other related functionalities.
"""

import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pydantic import ValidationError
from .models import NFTListing

# In-memory data structure
listings = []


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
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            validated_data = NFTListing(**data)
            # If validation passes, add the data to your in-memory listings

            # Extracting details from the received data
            collection_address = validated_data.collectionAddress
            token_id = validated_data.tokenId
            price = validated_data.price
            is_auction = validated_data.isAuction

            # Check if all required details are provided
            if not all([collection_address, token_id, price]):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # Add to our in-memory listings
            listings.append(
                {
                    "collectionAddress": collection_address,
                    "tokenId": token_id,
                    "price": price,
                    "isAuction": is_auction,
                }
            )

            return JsonResponse({"message": "Listing added successfully"}, status=201)

        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == "GET":
        return JsonResponse(listings, safe=False)

    else:
        return HttpResponse(status=405)
