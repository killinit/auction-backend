import os

from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APIRequestFactory

from apps.auction.models import Category, Product, Review, Bid


class TestJSONTokenAuthentication(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Load test data.
        """
        cls.user = get_user_model().objects.create(email="email@gmail.com", password="password")
        cls.category = Category.objects.create(id=1, title="Books")
        cls.product = Product.objects.create(title="The Happening", price=15, num_reviews=0, description="Lorem ipsum.")
        cls.product.categories.add(cls.category)
        cls.review = Review.objects.create(user=cls.user, product=cls.product, rating=5, comment="Lorem ipsum.")
        cls.review = Review.objects.create(user=cls.user, product=cls.product, rating=5, value=17)

    def setUp(self):
        """
        Set authenticated and anonymous users.

        Note: method client.credentials() avoids having to manually add the HTTP_AUTHORIZATION header on every request.
        """
        response = client.post('/api/auth/login/', {'email': "email@gmail.com", 'password': "password"})
        token = "JWT {}".format(response.data['token'])
        client = APIClient()
        self.auth_client = client.credentials(HTTP_AUTHORIZATION=token)
        self.anon_client = APIClient()

    def test_should_accept_request_from_authenticated_user(self):
        """
        The API should accept requests from an authenticated user.
        """
        expected = {'id': 1, 'title': 'Electronics'}
        response = self.auth_client.get('/api/categories/1/')
        self.assertEqual(response.data, expected)

    def test_should_reject_request_from_anonymous_user(self):
        """
        The API should reject requests from anonymous user.
        """
        expected = {'detail': 'Authentication credentials were not provided.'}
        response = self.anon_client.get('/api/categories/1/')
        self.assertEqual(response.data, expected)
