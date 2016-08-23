from functools import wraps
from json import loads, dumps

import jwt
from channels.handler import AsgiRequest
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_jwt.utils import jwt_decode_handler
from rest_framework_jwt.utils import jwt_get_user_id_from_payload_handler

from apps.user.models import User
from utils.auth import exceptions


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.
    From: https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/authentication.py
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')

    if isinstance(auth, type('')):
        # Work around django test client oddness
        auth = auth.encode('iso-8859-1')

    return auth


def _close_reply_channel(message):
    message.reply_channel.send({'close': True})


def authenticate(token):
    """
    Tries to authenticate user based on the supplied token. It also checks
    the token structure and validity.

    Based on jwt_auth.JSONWebTokenAuthMixin.authenticate
    """
    try:
        payload = jwt_decode_handler(token)
    except jwt.ExpiredSignature:
        msg = 'Signature has expired.'
        raise exceptions.AuthenticationFailed(msg)
    except jwt.DecodeError:
        msg = 'Error decoding signature.'
        raise exceptions.AuthenticationFailed(msg)

    user = authenticate_credentials(payload)

    return user


def authenticate_credentials(payload):
    """
    Returns the user associated with the token payload.

    Based on jwt_auth.JSONWebTokenAuthMixin.authenticate_credentials
    """
    try:
        user_id = jwt_get_user_id_from_payload_handler(payload)

        if user_id:
            user = get_user_model().objects.get(pk=user_id, is_active=True)
        else:
            msg = 'Invalid payload'
            raise exceptions.AuthenticationFailed(msg)
    except ObjectDoesNotExist:
        msg = 'Invalid signature'
        raise exceptions.AuthenticationFailed(msg)

    return user


def jwt_request_parameter(func):
    """
    Checks the presence of a "token" request parameter and tries to
    authenticate the user based on its content.
    """
    @wraps(func)
    def inner(self, message, *args, **kwargs):
        # Taken from channels.session.http_session
        try:
            if "method" not in message.content:
                message.content['method'] = "FAKE"
            request = AsgiRequest(message)
        except Exception as e:
            raise ValueError("Cannot parse HTTP message - are you sure this is a HTTP consumer? %s" % e)

        key, value = message.content['query_string'].split('=')
        if key != "JWT" or value is None:
            _close_reply_channel(message)
            raise ValueError("Missing token request parameter. Closing channel.")

        token = value
        user = authenticate(token)

        message.token = token
        message.user = user

        self.message.token = token
        self.message.user = user

        return func(self, message, *args, **kwargs)
    return inner


def jwt_message_text_field(func):
    """
    Checks the presence of a "token" field on the message's text field and
    tries to authenticate the user based on its content.
    """
    @wraps(func)
    def inner(self, message, *args, **kwargs):
        message_text = message.get('text', None)
        if message_text is None:
            _close_reply_channel(message)
            raise ValueError("Missing text field. Closing channel.")

        try:
            message_text_json = loads(message_text)
        except ValueError:
            _close_reply_channel(message)
            raise

        token = message_text_json.pop('token', None)
        if token is None:
            _close_reply_channel(message)
            raise ValueError("Missing token field. Closing channel.")

        user = authenticate(token)

        message.token = token
        message.user = user
        message.text = dumps(message_text_json)

        self.message.token = token
        self.message.user = user
        self.message.text = dumps(message_text_json)

        return func(self, message, *args, **kwargs)
    return inner


def user_from_jwt_token(func):
    # TODO: eliminate this method and add_to_session() if they prove unable to replace the remaining decorators
    @wraps(func)
    def inner(message, *args, **kwargs):
        key, value = message.content['query_string'].split('=')
        if key == 'JWT':
            token = jwt_decode_handler(value)
            username = token['username']
            user = User.objects.get(username=username)
            add_to_session(message.channel_session, user)
        return func(message, *args, **kwargs)
    return inner


def add_to_session(session, user):
    # TODO: eliminate this method and user_from_jwt_token() if they prove unable to replace the remaining decorators
    session['user'] = user
