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
    token ID, price, auction status and owner address.
    """

    nftCollectionAddress: str
    tokenId: int
    erc20Address: str
    erc20Amount: float
    isAuction: bool
    ownerAddress: str


class NFTPurchaseIntent(BaseModel):
    """
    Data model representing an intent to purchase an NFT.

    This model captures essential details required for the purchase, including
    collectionAddress, tokenId, bid, and the necessary signatures for verification.
    """

    nftCollectionAddress: str
    tokenId: int
    erc20Address: str
    erc20Amount: float
    bidderSig: str
    buyerAddress: str
    saleId: int


class NFTSettle(BaseModel):
    """
    Data model representing an intent to settle an NFT.

    This model captures essential details required for the purchase, including
    saleId and the necessary signatures for verification.
    """

    sale_id: int
    owner_approval_sig: str
    owner_address: str
