"""Ponto de entrada ASGI para servidores async."""

import os

from django.core.asgi import get_asgi_application

# Define qual modulo contem as configuracoes do Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Objeto que o servidor ASGI usa para atender requisicoes.
application = get_asgi_application()
