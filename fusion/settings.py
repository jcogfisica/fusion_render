# =============================================
# IMPORTS BÁSICOS E EXTERNOS
# =============================================

import os
# Permite interagir com o sistema operacional:
# - ler variáveis de ambiente (os.environ)
# - criar/verificar pastas e arquivos
# - manipular caminhos com os.path

from pathlib import Path
# Classe orientada a objetos para caminhos
# Permite escrever BASE_DIR / 'templates' de forma segura e multiplataforma

import dj_database_url
# Converte uma URL de banco (ex: postgres://user:pass@host:port/db) em dict compatível com Django
# Útil para Heroku, Render e outras plataformas de cloud

from google.oauth2 import service_account
# Cria objetos de credenciais do Google Cloud a partir de arquivos JSON de Service Account
# Necessário para autenticar uploads para GCS

# Configuração do banco de dados principal da aplicação Django usando a biblioteca dj_database_url:
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://jcog:MON010deo010@localhost:5432/fusion',
        # Caso a variável de ambiente DATABASE_URL não esteja definida,
        # usa a URL padrão do banco MySQL local especificada acima.

        conn_max_age = 600,
        # Tempo máximo (em segundos) que a conexão com o banco pode permanecer aberta e reutilizada.
        # Usado para melhorar a performance evitando abrir uma conexão a cada requisição.

        ssl_require = False
        # Define se a conexão com o banco de dados requer SSL.
        # False significa que a conexão não usará criptografia SSL.
    )
}

# =============================================
# BASE_DIR
# =============================================
BASE_DIR = Path(__file__).resolve().parent.parent
# Caminho absoluto para a raiz do projeto (onde está manage.py)
# - __file__ é o caminho deste arquivo settings.py
# - .resolve() transforma em caminho absoluto
# - .parent.parent sobe até a raiz do projeto
# Evita hardcoding de caminhos e facilita portabilidade

# =============================================
# SEGURANÇA
# =============================================
SECRET_KEY = 'django-insecure-9ws=#c@fv-y%#a3%b8ua422auu)#eq5$m%93tc0kv3d*ih8#vj'
# Chave secreta do Django
# - Usada para sessões, CSRF e hashes internos
# - Não deve ser versionada em produção

RENDER = os.environ.get('RENDER') == 'TRUE'
# Flag booleana para detectar se o app está rodando em Render.com

DEBUG = not RENDER
# DEBUG=True em dev: mostra erros detalhados, permite runserver servir arquivos estáticos
# DEBUG=False em prod: oculta erros, obrigatório por segurança

ALLOWED_HOSTS = ['*'] # ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1']
# Inicializa a lista de domínios/hosts que o Django aceitará para requisições HTTP
# Evita ataques do tipo "Host header injection" ao recusar requests vindos de domínios não autorizados
"""
if not DEBUG:
    # Executa este bloco somente em produção (DEBUG=False)
    external = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    # Obtém o hostname público fornecido automaticamente pelo Render.com para este serviço
    # Ex.: 'meu-app-xyz.onrender.com'

    if external:
        ALLOWED_HOSTS.append(external)
        # Adiciona o hostname público à lista de hosts permitidos
        # Isso garante que o site acessível pela internet seja reconhecido pelo Django

    ALLOWED_HOSTS.append('.onrender.com')
    # Adiciona um curinga para permitir qualquer subdomínio de onrender.com (*.onrender.com)
    # Útil se o app estiver disponível em múltiplos subdomínios gerenciados pelo Render
"""
# =============================================
# INSTALLED_APPS
# =============================================
INSTALLED_APPS = [
    # Apps padrões do Django
    'django.contrib.admin',  # painel de administração
    'django.contrib.auth',  # autenticação de usuários
    'django.contrib.contenttypes',  # tipos de conteúdo genéricos
    'django.contrib.sessions',  # sessões de usuário
    'django.contrib.messages',  # mensagens flash
    'django.contrib.staticfiles',  # arquivos estáticos

    # Apps do projeto
    'core',  # app principal do projeto
    'bootstrap4',  # integração com Bootstrap 4
    'stdimage',  # thumbnails automáticos
    'pictures',  # imagens responsivas
    'storages'  # integração com storage remoto (GCS, S3)
]
# Cada app registrado:
# - executa ready()
# - registra models
# - disponibiliza staticfiles e templates

# =============================================
# MIDDLEWARE
# =============================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Middleware de segurança do Django.
    # Adiciona headers HTTP de proteção, como HSTS, X-Content-Type-Options, X-XSS-Protection.
    # Ajuda a proteger a aplicação contra ataques comuns.

    'whitenoise.middleware.WhiteNoiseMiddleware',
    # Middleware do WhiteNoise.
    # Serve arquivos estáticos diretamente pelo Django em produção sem depender de um servidor externo.
    # Útil quando não há Nginx ou CDN configurados para servir static files.

    'django.contrib.sessions.middleware.SessionMiddleware',
    # Middleware de sessões do Django.
    # Habilita o uso de request.session para armazenar dados temporários do usuário.
    # Deve vir antes do AuthenticationMiddleware, pois ele depende das sessões.

    'django.middleware.common.CommonMiddleware',
    # Middleware com funcionalidades comuns de utilidade.
    # Inclui suporte a APPEND_SLASH, redirecionamentos automáticos e tratamento de ETags.

    'django.middleware.csrf.CsrfViewMiddleware',
    # Middleware de proteção CSRF (Cross-Site Request Forgery).
    # Garante que requisições POST, PUT e DELETE venham de fontes confiáveis.
    # Adiciona e valida o token CSRF automaticamente.

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # Middleware de autenticação.
    # Adiciona request.user, permitindo identificar o usuário logado em cada requisição.
    # Depende de SessionMiddleware para funcionar corretamente.

    'django.contrib.messages.middleware.MessageMiddleware',
    # Middleware de mensagens "flash".
    # Permite enviar mensagens temporárias entre requests, integrando com templates e exibição de alertas.

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Middleware anti-clickjacking.
    # Adiciona o header X-Frame-Options para evitar que páginas do site sejam exibidas dentro de iframes de terceiros.
    # Normalmente configurado como SAMEORIGIN.
]

# Middleware processa cada request/response
# Ordem importante:
# - SessionMiddleware antes de AuthMiddleware
# - CSRF verifica POST/PUT/DELETE
# - SecurityMiddleware adiciona headers de proteção

# =============================================
# URLS E TEMPLATES
# =============================================
ROOT_URLCONF = 'fusion.urls'
# Define o módulo raiz de URLs do projeto

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],  # procura templates fora dos apps
        'APP_DIRS': True,  # procura templates dentro de cada app
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                # Adiciona 'request' nos templates
                'django.contrib.auth.context_processors.auth',
                # Adiciona 'user' e 'perms' nos templates
                'django.contrib.messages.context_processors.messages',
                # Adiciona mensagens flash nos templates
            ],
        },
    },
]
# Context processors inserem variáveis globais nos templates

# =============================================
# CONFIGURAÇÃO DA BIBLIOTECA PICTURES
# =============================================
PICTURES = {
    "BREAKPOINTS": {'thumb': 480, "mobile": 576, "tablet": 768, "desktop": 992},
    # Define larguras de referência para gerar imagens responsivas
    "GRID_COLUMNS": 1,
    # Número de colunas lógicas do grid
    "CONTAINER_WIDTH": 480,
    # Largura máxima de container usada no cálculo das imagens
    "FILE_TYPES": ["WEBP", "JPG", "JPEG", "BMP", "PNG"],
    # Formatos suportados
    "PIXEL_DENSITIES": [1],
    # Densidade de pixels (1x, 2x etc.)
    "USE_PLACEHOLDERS": True,
    # Cria placeholders para melhor UX ao carregar imagens
}

# =============================================
# WSGI
# =============================================
WSGI_APPLICATION = 'fusion.wsgi.application'
# Entry point WSGI que servidores como gunicorn/uwsgi usam para servir o app

# =============================================
# VALIDADORES DE SENHA
# =============================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    # Evita senhas semelhantes a atributos do usuário
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    # Exige comprimento mínimo de senha
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    # Bloqueia senhas muito comuns
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
    # Bloqueia senha composta só por números
]

# =============================================
# INTERNACIONALIZAÇÃO
# =============================================
LANGUAGE_CODE = 'pt-br'
# Idioma padrão do projeto

TIME_ZONE = 'America/Sao_Paulo'
# Fuso horário padrão do projeto

USE_I18N = True
# Ativa o mecanismo de internacionalização

USE_TZ = True
# Armazena datetimes em UTC no banco e converte para timezone local ao exibir

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Define o tipo padrão de campo para chaves primárias automáticas.

# -------------------------------------------------------------------
# Configuração para autenticação e acesso ao Google Cloud Storage (GCS)
# -------------------------------------------------------------------

path_credenciais = None
# path_credenciais é o caminho para o arquivo de credenciais JSON, o qual contém as credenciais para acessar o bucket do Google Cloud

filename = "credenciais.json"
# Nome do arquivo de credenciais

GS_CREDENTIALS = None
# Objeto contendo as credenciais propriamente ditas

if not DEBUG:
    # Se a aplicação estiver em produção

    path_credenciais = "/etc/secrets/" + filename
    # Caminho para o arquivo de credenciais no ambiente do Render

    if os.path.exists(path_credenciais): # se o caminho path_credenciais aponta para o arquivo cujo nome é filename
        # print(f"O arquivo {path_credenciais} existe!")

        GS_CREDENTIALS = service_account.Credentials.from_service_account_file(path_credenciais)
        # Carrega as credenciais do arquivo JSON utilizando a classe service_account.
        # O metodo from_service_account_file lê o arquivo JSON e retorna um objeto credencial: GS_CREDENTIALS

    else:
        raise Exception(f"O arquivo {path_credenciais} não existe!")
        # Retorna uma exceção mostrando que path_credenciais não aponta para o arquivo JSON


else:
    path_credenciais = os.path.join(BASE_DIR, filename)
    # Caminho para o arquivo de credenciais no ambiente local

    if os.path.exists(path_credenciais): # se o caminho path_credenciais aponta para o arquivo cujo nome é filename
        # print(f"O arquivo {path_credenciais} existe!")

        GS_CREDENTIALS = service_account.Credentials.from_service_account_file(path_credenciais)
        # Carrega as credenciais do arquivo JSON utilizando a classe service_account.
        # O metodo from_service_account_file lê o arquivo JSON e retorna um objeto credencial: GS_CREDENTIALS

    else:
        raise Exception(f"O arquivo {path_credenciais} não existe!")
        # Retorna uma exceção mostrando que path_credenciais não aponta para o arquivo JSON

# -------------------------------------------------------------------
# Configurações do Google Cloud Storage para arquivos estáticos e mídia
# -------------------------------------------------------------------

GS_BUCKET_NAME = "django-render"
# Nome do bucket no Google Cloud Storage onde os arquivos serão armazenados.

# ---------- INÍCIO DA CONFIGURAÇÃO CONDICIONAL PARA AMBIENTES ----------

# Abaixo implementamos uma diferenciação entre o ambiente de produção (quando DEBUG = False)
# e o ambiente de desenvolvimento local (DEBUG = True), para que localmente os arquivos estáticos e de mídia
# sejam armazenados e servidos pelo sistema de arquivos local, facilitando o desenvolvimento e testes.
# Já em produção, os arquivos serão armazenados e servidos pelo bucket do Google Cloud Storage (GCS).
#
# Isso resolve o problema onde, localmente, a aplicação tentava enviar arquivos estáticos diretamente para o GCS,
# o que pode não ser desejável ou configurado para funcionar no ambiente local.
#
# Essa abordagem permite que:
# - No desenvolvimento local, arquivos estáticos e mídia sejam facilmente acessados e modificados localmente.
# - Na produção, o uso do armazenamento em nuvem garante alta disponibilidade e escalabilidade.

if not DEBUG:
    STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"
    MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"
    # URLs públicas para acesso direto a arquivos estáticos e de mídia hospedados no bucket GCS.

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
            "OPTIONS": {
                "bucket_name": GS_BUCKET_NAME,
                "credentials": GS_CREDENTIALS,
                "location": "media",
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
            "OPTIONS": {
                "bucket_name": GS_BUCKET_NAME,
                "credentials": GS_CREDENTIALS,
                "location": "static",
            },
        },
    }
    # Configuração que o Django usa para definir como e onde ele vai armazenar arquivos — principalmente arquivos estáticos (CSS, JS, imagens do layout)
    # e arquivos de mídia (imagens, documentos enviados pelo usuário).
    # Quando você usa armazenamento em nuvem — aqui, o Google Cloud Storage (GCS) — o Django precisa saber:
    # 1) Qual é o backend de armazenamento (no caso, o storages.backends.gcloud.GoogleCloudStorage, que é a integração do Django com o Google Cloud Storage)
    # 2) Em qual bucket os arquivos vão ser guardados (bucket_name)
    # 3) Quais credenciais usar para autenticar e ter permissão de acessar esse bucket (credentials)
    # 4) E uma "pasta" (localização) dentro do bucket para organizar os arquivos (location), por exemplo "media" para arquivos de mídia e "static" para arquivos estáticos
    # O que significa cada chave?
    # "default": define o armazenamento padrão para arquivos de mídia enviados pelo usuário (exemplo: fotos enviadas, PDFs etc)
    # "staticfiles" — define o armazenamento para arquivos estáticos do seu site (exemplo: CSS, JavaScript, imagens do tema)
    # Cada um aponta para o mesmo bucket, mas em locais diferentes (location: "media" e location: "static"),
    # assim os arquivos ficam organizados separadamente dentro do bucket.

    # Configuração para produção no GCS:
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    # É uma configuração do Django que define qual backend de armazenamento será usado para arquivos de mídia
    # (ou seja, arquivos enviados por usuários, como fotos, documentos, etc).
    # 'storages.backends.gcloud.GoogleCloudStorage' é o backend do pacote django-storages para armazenar arquivos no Google Cloud Storage (GCS).
    # Quando o Django salva um arquivo de mídia (por exemplo, um upload de imagem),
    # ele usará esse backend para enviar o arquivo para o bucket configurado no GCS, ao invés de salvar localmente no disco do servidor.

    STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    # Define qual backend será usado para armazenar e servir os arquivos estáticos (CSS, JavaScript, imagens fixas usadas pelo site).
    # Também aponta para o backend do GCS. Isso indica que, quando você executar o comando collectstatic do Django,
    # os arquivos estáticos serão enviados para o bucket no Google Cloud, ao invés de serem guardados localmente.

else:
    STATIC_URL = '/static/'
    # Define a URL base para acessar os arquivos estáticos localmente, ou seja, quando você estiver desenvolvendo ou rodando o projeto em modo debug (não em produção).

    MEDIA_URL = '/media/'
    # Define a URL base para acessar arquivos de mídia (uploads de usuários) localmente.

    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Diretório local no servidor onde o comando collectstatic vai reunir todos os arquivos estáticos do projeto.
    # Em ambiente local, o Django coleta todos os arquivos estáticos (de apps e pastas STATICFILES_DIRS) e os coloca nessa pasta para serem servidos pelo servidor local.

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    # Diretório local onde o Django salva os arquivos de mídia (uploads de usuários) quando você está rodando o projeto localmente.
    # Para desenvolvimento local, onde normalmente não se usa armazenamento em nuvem, mas salva arquivos no disco do próprio computador.

    # Pode adicionar diretórios extras para arquivos estáticos, caso use:
    # STATICFILES_DIRS = [
        #BASE_DIR / 'core' / 'static',
    #]

    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    # Define o backend de armazenamento para arquivos de mídia (uploads feitos por usuários) usando o sistema de arquivos local.
    # Ao invés de enviar para o Google Cloud Storage, o Django vai salvar os arquivos no diretório local definido por MEDIA_ROOT.
    # Esse é o comportamento padrão do Django quando você não configura nada relacionado a armazenamento em nuvem.

    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    # Backend padrão para lidar com arquivos estáticos (CSS, JS, imagens do site).
    # Ao rodar python manage.py collectstatic, todos os arquivos estáticos serão reunidos no diretório local STATIC_ROOT.    #
    # Eles não serão enviados para um bucket em nuvem.
    # Esse backend apenas cuida de copiar e organizar os arquivos localmente para que o servidor de desenvolvimento ou um servidor web (como Nginx) possa servi-los.

    # ---------- FIM DA CONFIGURAÇÃO CONDICIONAL PARA AMBIENTES ----------

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    LOGOUT_REDIRECT_URL = 'index'

    # Comentários adicionais:
    # Ao executar o comando 'python manage.py collectstatic', o Django irá coletar
    # os arquivos estáticos de todos os apps instalados e também de STATICFILES_DIRS
    # e armazená-los em STATIC_ROOT para posteriormente fazer upload no bucket.

    """
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_PASSWORD = '<PASSWORD>'
    EMAIL_HOST_USER = 'no-reply@seudominio.com'
    """
    # Configurações de email, atualmente comentadas.
    # Servem para enviar emails via servidor SMTP, como confirmação de cadastro, reset de senha, etc.
