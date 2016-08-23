from ..user.serializers import UserProfileSerializer


# This method overrides JWT_AUTH's JWT_RESPONSE_PAYLOAD_HANDLER setting to include the
# user 'Id' in the response payload besides the default 'Token' upon login.
# Other fields from the UserSerializer may be included if required, following the same syntax.
def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'id': UserProfileSerializer(user).data["id"]
    }
