import logging

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .serializers import UserProfileSerializer


logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes((permissions.AllowAny, ))
def user_picture(request, pk):
    """Use this endpoint to download the profile picture for an arbitrary user."""

    user = get_user_model().objects.get(id=pk)
    picture = user.picture
    response = Response()
    response["Content-Disposition"] = "attachment; filename={}".format(user.get_picture_pretty_name())
    response['X-Accel-Redirect'] = "/media/{}".format(picture.name)
    return response


class AccountProfileView(generics.RetrieveAPIView):
    """Use this endpoint to retrieve account profile."""
    model = get_user_model()
    queryset = get_user_model().objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self, *args, **kwargs):
        return self.request.user
