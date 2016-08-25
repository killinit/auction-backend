from django.conf.urls import url

from .views import user_picture


urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/pictures/$', user_picture, name='user_picture'),
]
