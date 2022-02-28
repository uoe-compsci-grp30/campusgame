"""
ASGI config for campusgame project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
# mysite/asgi.py
import os

import django
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter

import games.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusgame.settings')
django.setup()

router = URLRouter(games.routing.websocket_urlpatterns)

application = ProtocolTypeRouter({
    "http": AsgiHandler(),
    "websocket": AuthMiddlewareStack(
        router
    ),
    # Just HTTP for now. (We can add other protocols later.)
})
