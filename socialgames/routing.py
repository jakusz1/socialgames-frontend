from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from game.consumers import GameSessionConsumer


application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^ws/(?P<device_type>\w*)/(?P<uri>\w*)$", GameSessionConsumer)
        ])
    ),
})