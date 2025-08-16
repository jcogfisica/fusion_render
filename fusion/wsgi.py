import os
# Importa o módulo do sistema operacional
# Permite definir variáveis de ambiente, ler caminhos e configurar parâmetros globais do ambiente

from django.core.wsgi import get_wsgi_application
# Importa a função que cria a aplicação WSGI do Django
# WSGI (Web Server Gateway Interface) é o padrão Python para servidores web se comunicarem com aplicações Python

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fusion.settings')
# Define a variável de ambiente 'DJANGO_SETTINGS_MODULE' caso ainda não exista
# Essa variável informa ao Django qual módulo de settings usar
# No caso, 'fusion.settings' indica que o arquivo settings.py está no pacote fusion

application = get_wsgi_application()
# Cria a aplicação WSGI que será usada pelo servidor web (gunicorn, uwsgi, etc.)
# 'application' é o callable que o servidor chama para processar requisições HTTP

