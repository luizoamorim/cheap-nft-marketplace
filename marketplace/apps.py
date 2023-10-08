"""
This module contains the application configuration for the 'marketplace' app.

Django uses this configuration to handle app-specific settings and initialization processes.
"""

from django.apps import AppConfig


class MarketplaceConfig(AppConfig):
    """
    Application configuration class for the 'marketplace' app.

    This class contains settings specific to the 'marketplace' app, such as the
    default auto field type and the app's name.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "marketplace"
