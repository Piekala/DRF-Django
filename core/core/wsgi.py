"""Ponto de entrada WSGI para servidores web tradicionais."""

import os

from django.core.wsgi import get_wsgi_application

# Define qual modulo contem as configuracoes do Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Objeto que o servidor WSGI usa para atender requisicoes.
application = get_wsgi_application()
