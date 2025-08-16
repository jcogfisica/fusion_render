"""
URL configuration for fusion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Importa o módulo administrativo do Django
# Esse módulo fornece a interface administrativa que permite gerenciar os modelos via navegador
from django.contrib import admin

# Importa funções utilitárias para definir rotas
# path() → mapeia um padrão de URL para uma view específica
# include() → permite incluir as rotas de outro arquivo de URLs (útil para dividir rotas por aplicação)
from django.urls import path, include

# Importa função que auxilia a servir arquivos estáticos/mídia no modo de desenvolvimento
from django.conf.urls.static import static

# Importa as configurações do projeto (definidas no settings.py) para acessar MEDIA_URL e MEDIA_ROOT
from django.conf import settings

# Lista obrigatória que mapeia padrões de URL para views
# Cada entrada dessa lista indica: "Se o usuário acessar essa URL, execute essa view"
urlpatterns = [

    # Rota para o painel administrativo do Django
    # "/admin/" será atendido pelas URLs internas do sistema admin do Django
    path('admin/', admin.site.urls),

    # Rota para a página inicial (URL raiz "/")
    # O include('core.urls') delega o controle para o arquivo urls.py dentro do app "core"
    path('', include('core.urls')),

    # Sobre a seguinte linha de código considere a pergunta: pictures.urls serve para quê?
    # A inclusão de path('pictures/', include('pictures.urls'))
    # é necessária porque a biblioteca django-pictures depende de algumas URLs internas para funcionar corretamente,
    # especialmente se você está usando recursos como:
    # 1. Placeholders: Imagens temporárias (ex: enquanto uma imagem real não foi carregada)
    # Se você tiver PICTURES["USE_PLACEHOLDERS"] = True, então essas rotas são obrigatórias.
    # 2. Preview de imagens ou URLs resolvidas automaticamente: Algumas views internas do pacote são usadas para servir essas
    # imagens em tempo real (por exemplo, para admin ou frontend dinâmico).
    path('pictures/', include('pictures.urls'))
]

# Concatenação da lista urlpatterns com rotas extras para servir arquivos de mídia
# Isso só é usado no modo de desenvolvimento (DEBUG=True)
# static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT):
#   - MEDIA_URL: prefixo usado para acessar arquivos de mídia via URL (ex: "/media/")
#   - MEDIA_ROOT: caminho físico no servidor onde os arquivos enviados são salvos
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
