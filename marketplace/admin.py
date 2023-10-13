"""
This module defines the admin interfaces for the models in the NFT marketplace app.

Here, you can configure how the models of this app are displayed and managed in
Django's built-in admin site.
"""

from django.contrib import admin
from .models import NFTListing


# Register your models here.
@admin.register(NFTListing)
class NFTListingAdmin(admin.ModelAdmin):
    """
    Admin interface for the NFTListing model.

    This class configures how the NFTListing model is displayed and managed
    in Django's built-in admin site. It allows for easy viewing and modification
    of NFT listings directly through the admin interface.

    Attributes:
    - list_display: Fields of the NFTListing model to be displayed in the list view.
    """

    list_display = ("collectionAddress", "tokenId", "price", "isAuction")
