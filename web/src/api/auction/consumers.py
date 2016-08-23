import logging
import json

from channels import Group
from channels.generic.websockets import WebsocketConsumer
from apps.auction.models import Product

from utils.auth.decorators import jwt_request_parameter


logger = logging.getLogger(__name__)


class AuctionConsumer(WebsocketConsumer):

    http_user = True
    strict_ordering = False
    slight_ordering = False

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        return ["test"]

    # The "bids" keyword argument here comes from the regex capture group in
    # routing.py.
    #@jwt_request_parameter
    def connect(self, message, product_id):
        """
        When the user opens a WebSocket to a bids stream, add them to the
        group for that stream so they receive new bid notifications.

        The notifications are actually sent in a post_save signal of the Bid model.
        """
        logger.info('Connected to websocket server.')
        logger.info("Product_id: {}.".format(product_id))
        logger.info("Message: {}.".format(message))
        logger.info("Reply Channel: {}.".format(message.reply_channel))
        logger.info("Content: {}.".format(message.content))
        # Try to fetch the product by product_id; if that fails, close the socket.
        try:
            product = Product.objects.get(id=product_id)
            logger.info("Product: {}.".format(product))
        except Product.DoesNotExist:
            # Send "close" to make Daphne close off the socket, and some
            # error text for the client.
            message.reply_channel.send({"text": json.dumps({"error": "No valid product_id provided."}), "close": True})
            return
        # Each different client has a different "reply_channel", which is how you
        # send information back to them. We can add all the different reply channels
        # to a single Group, and then when we send to the group, they'll all get the
        # same message.
        logger.info("Group: product-{}.".format(product.id))
        Group("product-{}".format(product.id)).add(message.reply_channel)
        logger.info("Groups: {}.".format(self.connection_groups()))

    def receive(self, text=None, bytes=None, **kwargs):
        """
        Called when a message is received with either text or bytes filled out.
        """
        logger.info("Received message from websocket server")
        logger.info("Text: {}.".format(text))
        logger.info("Bytes: {}.".format(bytes))
        logger.info("Kwargs: {}.".format(kwargs))

    def disconnect(self, message, product_id):
        """
            Removes the user from the liveblog group when they disconnect.

            Channels will auto-cleanup eventually, but it can take a while, and having old
            entries cluttering up your group will reduce performance.
            """
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            # This is the disconnect message, so the socket is already gone; we can't
            # send an error back. Instead, we just return from the consumer.
            return
        Group("product-{}".format(product.id)).send({'text': 'goodbye anonymous user'})
        Group("product-{}".format(product.id)).discard(message.reply_channel)
        logger.info('Disconnected from websocket server: message = {}'.format(message))
