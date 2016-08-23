from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AuctionConfig(AppConfig):
    name = 'apps.auction'
    verbose_name = _("Auction")

    def ready(self):
        from . import signals
