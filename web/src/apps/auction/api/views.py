import logging

import django_filters
from rest_framework import generics, filters, permissions
from rest_framework.response import Response

from apps.auction.models import Category, Product, Review, Bid
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, BidSerializer


logger = logging.getLogger(__name__)


class CategoryListView(generics.ListCreateAPIView):
    """Use this endpoint to list or create categories."""
    model = Category
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Use this endpoint to retrieve, update or delete a given category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductFilter(filters.FilterSet):
    category = django_filters.CharFilter(name="categories__title")

    class Meta:
        model = Product
        fields = ['title', 'price', 'category']


class ProductListView(generics.ListCreateAPIView):
    """Use this endpoint to list or create products."""
    queryset = Product.objects.all()
    model = Product
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ProductFilter


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Use this endpoint to retrieve, update or delete a given product."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    

class ReviewListView(generics.ListCreateAPIView):
    """Use this endpoint to list or create reviews."""
    model = Review
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Use this endpoint to retrieve, update or delete a given review."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
    

class BidListView(generics.ListCreateAPIView):
    """Use this endpoint to list or create bids."""
    model = Bid
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [permissions.AllowAny]


class BidDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Use this endpoint to retrieve, update or delete a given bid."""
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [permissions.AllowAny]


class ProductReviewsListView(generics.ListAPIView):
    """Use this endpoint to list or create products."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        This view should return a list of all the reviews for
        the product as determined by the product portion of the URL.
        """
        product = self.kwargs['pk']
        return Review.objects.filter(product__id=product)
