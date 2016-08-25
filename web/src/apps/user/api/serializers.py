from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'picture', 'first_name', 'last_name')
