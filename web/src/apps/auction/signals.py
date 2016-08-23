import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Category, Product, Review, Bid
from .tasks import update_rating, send_ws_message


logger = logging.getLogger(__name__)


# TODO: check why we have multiple signals being returned for a single post_save
@receiver(post_save, sender=Review, dispatch_uid="review_created")
def review_created(sender, instance, **kwargs):

    if kwargs['created']:

        logger.info("Review created with id: {}".format(instance.id))

        # Update average rating
        logger.info("Updating average rating")
        update_rating.delay(instance.product_id, instance.rating)


@receiver(post_save, sender=Bid, dispatch_uid="bid_created")
def bid_created(sender, instance, **kwargs):

    if kwargs['created']:

        logger.info("Bid created with id: {}".format(instance.id))

        # Send 'Bid' websocket notification
        group = 'product-{}'.format(instance.product_id)
        bid = {'id': instance.id,
               'user_id': instance.user_id,
               'product_id': instance.product_id,
               'value': str(instance.value),
               'created': str(instance.created)}
        send_ws_message.delay(group, bid)
