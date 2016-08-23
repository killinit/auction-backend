import requests
from apps.auction.models import Category, Product, Review, Bid
from api.auction.serializers import CategorySerializer, ProductSerializer, ReviewSerializer, BidSerializer


class Api:
    """Allows calls to a Restful API.

    Examples
    --------
    >>> from tests.utils import Api
    >>> api = Api("http://192.168.99.102/api/")
    >>> api.base_url
    'http://192.168.99.102/api/'
    >>> api.headers
    {'Content-type': 'application/json'}
    >>> api.token
    ''

    Attributes
    ----------
    base_url: str
        API's base URL.
    headers: dict
        Generic headers.
    token: str
        JWT Token, used for authentication.
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {'Content-type': 'application/json'}
        self.token = ""

    def login(self, email, password):
        """Login via API to get the authentication token.

        Examples
        --------
        >>> api.login('user@email.com', 'password')
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE0Njg4NT...'

        Parameters
        ----------
        email : str
            User's email.
        password: str
            User's password.

        Returns
        -------
        token: str
            JWT token to use in authenticated API calls.
        """
        url = "auth/login/"
        r = requests.post(self.base_url + url, headers=self.headers, json={"email": email, "password": password})
        token = r.json()["token"]
        self.token = token
        self.headers = {'Content-type': 'application/json', 'Authorization': "JWT {}".format(token)}
        return token

    def call(self, url, method, data=None, headers=None):
        """
        Make an API call.

        Examples
        --------
        >>> r = api.call('users/checked-in/?latitude=10.0001&longitude=10.0001&accuracy=10', 'get')
        >>> r
        <Response [200]>
        >>> r.content
        b'[{"id":4,"uuid":"DF7E1C79-43E9-44FF-886F-1D1F7DA6997A","email":"donaltrump@email.com","...}]'


        Parameters
        ----------
        url: str
            API endpoint.
        method : str
            API HTTP method to use (i.e. 'get', 'post', 'put', 'patch' or 'delete').
        data: optional(dict)
            Data to submit in 'post', 'put' or 'patch' requests.
        headers: optional(dict)
            Headers to use in the request. Used to override the object level headers.

        Returns
        -------
        response: Response
            The request's response object.

        """

        url = self.base_url + url
        headers = headers if headers is not None else self.headers
        method = method.lower()

        if method == 'get':
            r = requests.get(url, headers=headers)
        if method == 'post':
            r = requests.post(url, json=data, headers=headers)
        elif method == 'put':
            r = requests.put(url, json=data, headers=headers)
        elif method == 'patch':
            r = requests.patch(url, json=data, headers=headers)
        elif method == 'delete':
            r = requests.delete(url, headers=headers)
        print("url: {}".format(r.url))
        print("headers: {}".format(r.headers))
        print("status code: {}".format(r.status_code))
        print("reason: {}".format(r.reason))
        print("content: {}".format(r.content))
        return r
