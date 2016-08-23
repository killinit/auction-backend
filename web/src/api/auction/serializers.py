import logging

from django.contrib.auth import get_user_model

from rest_framework import serializers

from apps.auction.models import Category, Product, Review, Bid


logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'first_name', 'last_name', 'picture')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'title')


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'num_reviews', 'rating', 'description', 'categories')


class ReviewSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    user = serializers.ReadOnlyField(read_only=True, source='user.email')
    product_id = serializers.IntegerField()
    product = serializers.ReadOnlyField(read_only=True, source='product.title')

    class Meta:
        model = Review
        fields = ('id', 'user_id', 'user', 'product_id', 'product', 'rating', 'comment', 'created')


class BidSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    user = serializers.ReadOnlyField(read_only=True, source='user.email')
    product_id = serializers.IntegerField()
    product = serializers.ReadOnlyField(read_only=True, source='product.title')

    class Meta:
        model = Bid
        fields = ('id', 'user_id', 'user', 'product_id', 'product', 'value', 'created')
