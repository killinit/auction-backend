import logging

from django.db import models

logger = logging.getLogger(__name__)


class CategoryManager(models.Manager):

    pass


class ProductManager(models.Manager):

    pass


class ReviewManager(models.Manager):

    pass


class BidManager(models.Manager):

    pass
