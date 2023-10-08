"""
This module defines data models for the NFT marketplace.

Here, the various database models related to the NFT marketplace are defined.
"""

from pydantic import BaseModel


# Create your models here.
class NFTListing(BaseModel):
    """
    Data model representing an NFT listing.

    This model captures essential details about an NFT listing, including collection address,
    token ID, price, and auction status.
    """

    collectionAddress: str
    tokenId: int
    price: float
    isAuction: bool
