import os

from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import renderers, response, schemas
from rest_framework.decorators import api_view, renderer_classes
from djoser import views as djoser_views
from rest_framework_jwt import views as jwt_views

from api.user.views import AccountProfileView
from apps.main.views import index


urlpatterns = [
    # admin
    url(r'^admin/', admin.site.urls),
    # api
    url(r'^api/docs/', include('rest_framework_swagger.urls')),
    url(r'^api/', include('api.auction.urls')),
    url(r'^api/account/', include('djoser.urls')),
    url(r'^api/account/profile/$', AccountProfileView.as_view(), name='user_profile'),
    url(r'^api/auth/login/$', jwt_views.obtain_jwt_token, name='login'),
    url(r'^api/auth/token-refresh/$', jwt_views.refresh_jwt_token, name='token-refresh'),
    url(r'^api/auth/logout/$', djoser_views.LogoutView.as_view(), name='logout'),
    url(r'^api/users/', include('api.user.urls')),
    # home
    url(r'^$|^index/$', index, name='index'),
]

# Login and logout views for the browsable API
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
