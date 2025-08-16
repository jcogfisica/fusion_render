"""
WSGI config for fusion project.

Este arquivo expõe a callable WSGI como variável de nível de módulo chamada `application`.

Para mais informações, consulte:
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

# =============================================
# IMPORTS BÁSICOS
# =============================================
import os
# Permite interagir com o sistema operacional:
# - Definir variáveis de ambiente
# - Consultar paths
# - Operações relacionadas ao SO

from django.core.wsgi import get_wsgi_application
# Função do Django que retorna um callable WSGI
# - Callable WSGI é a interface padrão que servidores (Gunicorn, uWSGI) usam para comunicar com o Django
# - Ex.: servidor envia request → callable retorna response

from dj_static import Cling, MediaCling
# Bibliotecas auxiliares para servir arquivos estáticos em ambientes WSGI simples
# - Cling: serve arquivos estáticos (STATIC_ROOT) no WSGI
# - MediaCling: serve arquivos de mídia (MEDIA_ROOT) no WSGI
# Útil em deploys que não usam Nginx/Apache para servir estáticos

# =============================================
# CONFIGURAÇÃO DE VARIÁVEL DE AMBIENTE
# =============================================
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fusion.settings')
# Define a variável de ambiente que indica qual arquivo de settings o Django deve usar
# - Se não estiver definida, usa 'fusion.settings'
# - Importante para que o Django saiba quais configurações carregar

# =============================================
# CRIAÇÃO DA APLICAÇÃO WSGI
# =============================================
application = Cling(MediaCling(get_wsgi_application()))
# Passo a passo:
# 1. get_wsgi_application() → cria o callable WSGI do Django
# 2. MediaCling(...) → envolve o WSGI para servir arquivos de mídia diretamente
# 3. Cling(...) → envolve o WSGI (e MediaCling) para servir arquivos estáticos diretamente
# Resultado:
# - `application` é o callable WSGI final que o servidor vai usar
# - Permite que requests de arquivos estáticos/mídia sejam tratados sem servidor externo adicional
