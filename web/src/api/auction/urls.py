from django.conf.urls import url

from .views import CategoryListView, CategoryDetailView, ProductListView, ProductDetailView, ReviewListView, \
    ReviewDetailView, BidListView, BidDetailView, ProductReviewsListView

urlpatterns = [
    url(r'^categories/$', CategoryListView.as_view(), name='category-list'),
    url(r'^products/$', ProductListView.as_view(), name='product-list'),
    url(r'^reviews/$', ReviewListView.as_view(), name='review-list'),
    url(r'^bids/$', BidListView.as_view(), name='bid-list'),
    url(r'^categories/(?P<pk>[0-9]+)/$', CategoryDetailView.as_view(), name='category-detail'),
    url(r'^products/(?P<pk>[0-9]+)/$', ProductDetailView.as_view(), name='product-detail'),
    url(r'^products/(?P<pk>[0-9]+)/reviews$', ProductReviewsListView.as_view(), name='product-reviews-list'),
    url(r'^reviews/(?P<pk>[0-9]+)/$', ReviewDetailView.as_view(), name='review-detail'),
    url(r'^bids/(?P<pk>[0-9]+)/$', BidDetailView.as_view(), name='bid-detail'),
]
