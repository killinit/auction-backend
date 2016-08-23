from channels.routing import route_class

from api.auction.consumers import AuctionConsumer

# The channel routing defines what channels get handled by what consumers,
# including optional matching on message attributes. WebSocket messages of all
# types have a 'path' attribute, so we're using that to route the socket.
# We can have the same paths as regular HTTP paths in urls because
# Daphne separates by protocol as it negotiates with a browser.
channel_routing = [
    route_class(AuctionConsumer, path=r"^/bids/(?P<product_id>[0-9]+)/"),
]
