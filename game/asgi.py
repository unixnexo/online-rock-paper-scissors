import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from rps_game import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game.settings')

application = get_asgi_application({})
