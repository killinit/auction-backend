import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from django_extensions.db.models import TimeStampedModel
from audit_log.models import AuthStampedModel

from .managers import CategoryManager, ProductManager, ReviewManager, BidManager, ProductCategoryManager


logger = logging.getLogger(__name__)


class Category(TimeStampedModel, AuthStampedModel):
    # Options

    # Relations

    # Attributes
    title = models.CharField(max_length=50, unique=True)

    # Manager
    objects = CategoryManager()

    # Functions
    def __str__(self):
        return _("[{}]: {}").format(self.id, self.title)

    # Meta
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Product(TimeStampedModel, AuthStampedModel):
    # Options

    # Relations
    categories = models.ManyToManyField('Category',
                                        through='ProductCategory',
                                        through_fields=('product', 'category'),
                                        related_name='category_products')

    reviewers = models.ManyToManyField('user.User',
                                       through='Review',
                                       through_fields=('product', 'user'),
                                       related_name='reviewed_products')

    bidders = models.ManyToManyField('user.User',
                                     through='Bid',
                                     through_fields=('product', 'user'),
                                     related_name='bid_products')

    # Attributes
    title = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    num_reviews = models.IntegerField(blank=True, null=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                              blank=True,
                                              null=True)
    description = models.CharField(max_length=255, blank=True, null=True)


    # Manager
    objects = ProductManager()

    # Functions
    def __str__(self):
        return _("[{}]: {}").format(self.id, self.title)

    # Meta
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


class Review(TimeStampedModel, AuthStampedModel):
    # Options

    # Relations
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name="product_reviews", db_index=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="user_reviews", db_index=True)

    # Attributes
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.CharField(max_length=255)

    # Manager
    objects = ReviewManager()

    # Functions
    def __str__(self):
        return _("[{}]: {} ({}) --> {} ({}) <=> Rating: {} - [{}]").\
            format(self.id,
                   self.user.email,
                   self.user.id,
                   self.product.title,
                   self.product.id,
                   self.rating,
                   self.created.strftime("%Y-%m-%d %H:%M:%S"))

    # Meta
    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")


class Bid(TimeStampedModel, AuthStampedModel):
    # Options

    # Relations
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name="product_bids", db_index=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="user_bids", db_index=True)

    # Attributes
    value = models.DecimalField(max_digits=19, decimal_places=2)

    # Manager
    objects = BidManager()

    # Functions
    def __str__(self):
        return _("[{}]: {} ({}) --> {} ({}) <=> Value: {} - [{}]").\
            format(self.id,
                   self.user.email,
                   self.user.id,
                   self.product.title,
                   self.product.id,
                   self.value,
                   self.created.strftime("%Y-%m-%d %H:%M:%S"))

    # Meta
    class Meta:
        verbose_name = _("Bid")
        verbose_name_plural = _("Bids")


class ProductCategory(TimeStampedModel, AuthStampedModel):
    # Options

    # Relations
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="product_category_pairs", db_index=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="category_product_pairs", db_index=True)

    # Attributes

    # Manager
    objects = ProductCategoryManager()

    # Functions
    def __str__(self):
        return _("[{}]: {} ({}) - {} ({})").\
            format(self.id,
                   self.product.title,
                   self.product.id,
                   self.category.title,
                   self.category.id)

    # Meta
    class Meta:
        unique_together = (("product", "category"),)
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")
