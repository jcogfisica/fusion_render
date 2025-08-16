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

import tempfile

# Criação de arquivos temporários seguros, caso seja necessário materializar credenciais

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

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
# Lista de hosts/domínios permitidos para evitar ataques de Host header injection
if not DEBUG:
    # Em produção, adiciona host público fornecido pelo Render
    external = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if external:
        ALLOWED_HOSTS.append(external)
    ALLOWED_HOSTS.append('.onrender.com')
# Adiciona curinga para permitir subdomínios *.onrender.com

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
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

# =============================================
# CREDENCIAIS GOOGLE CLOUD E BANCO DE DADOS
# =============================================
path_credenciais = None
# Variável que vai armazenar o caminho do arquivo JSON de credenciais

filename = "credenciais.json"
# Nome padrão do arquivo de credenciais

GS_CREDENTIALS = None
# Variável que vai guardar o objeto Credentials do Google Cloud

if not DEBUG:
    # Configurações de produção
    DATABASES = {
        'default': dj_database_url.config(
            default='postgresql://jcog:MON010deo010@localhost:5432/fusion',
            # URL fallback para dev/localhost
            conn_max_age=600,  # tempo de reutilização de conexões
            ssl_require=False  # SSL obrigatório em produção
        )
    }
    path_credenciais = "/etc/secrets/" + filename
    if os.path.exists(path_credenciais):
        GS_CREDENTIALS = service_account.Credentials.from_service_account_file(path_credenciais)
        # Cria objeto Credentials a partir do arquivo JSON
    else:
        raise Exception(f"O arquivo {path_credenciais} não existe!")
else:
    # Configurações de desenvolvimento
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',  # driver Postgres
            'NAME': 'fusion',  # nome do banco local
            'USER': 'jcog',  # usuário local
            'PASSWORD': 'MON010deo010',  # senha local
            'HOST': 'localhost',  # host local
            'PORT': '5432',  # porta padrão Postgres
        }
    }
    path_credenciais = os.path.join(BASE_DIR, filename)
    # Procura arquivo de credenciais no diretório do projeto
    if os.path.exists(path_credenciais):
        GS_CREDENTIALS = service_account.Credentials.from_service_account_file(path_credenciais)
    else:
        raise Exception(f"O arquivo {path_credenciais} não existe!")

# =============================================
# STORAGE E BUCKET GOOGLE CLOUD
# =============================================
GS_BUCKET_NAME = "django-render"
# Nome do bucket no Google Cloud Storage

if not DEBUG:
    # Produção: URLs públicas dos arquivos
    STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"
    MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"

    # Configuração de storages remotos
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
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
else:
    # Desenvolvimento local: diretórios físicos
    STATIC_URL = '/static/'  # URL para arquivos estáticos locais
    MEDIA_URL = '/media/'  # URL para uploads locais
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Diretório físico para collectstatic
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    # Diretório físico para uploads
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    # Salva uploads em MEDIA_ROOT
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    # Coleta arquivos estáticos para STATIC_ROOT
