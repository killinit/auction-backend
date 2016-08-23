import logging
from json import dumps

from django.contrib.auth import get_user_model
from celery.task import task
from channels import Group

from apps.auction.models import Product


logger = logging.getLogger(__name__)


@task
def update_rating(product_id, rating):
    """
    Task to update average product rating on reception of new review.
    """
    try:
        product = Product.objects.get(id=product_id)
        previous_count = product.num_reviews if product.num_reviews else 0
        previous_rating = product.rating if product.rating else 0
        new_rating = (previous_rating + rating) / (previous_count + 1)
        product.rating = new_rating
        product.save()
    except Exception as e:
        print(e)


@task
def send_ws_message(group, notification):
    logger.info('Sending websocket message: {}'.format(notification))
    Group(group).send({'text': dumps(notification)})
