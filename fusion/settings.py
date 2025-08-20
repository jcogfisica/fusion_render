# =============================================
# IMPORTS BÁSICOS E EXTERNOS
# =============================================

import os
# Importa o módulo padrão do Python chamado "os".
# Este módulo fornece funções para interagir com o sistema operacional.
# Exemplos:
#   - os.environ → acessa variáveis de ambiente
#   - os.path → manipula caminhos de arquivos/pastas
#   - os.mkdir, os.remove → criar ou remover diretórios/arquivos

from pathlib import Path
# Importa a classe Path do módulo "pathlib".
# Path é uma classe orientada a objetos para lidar com caminhos de arquivos e diretórios.
# Diferente de os.path, ela usa operadores (/) de forma intuitiva para concatenar caminhos.
# Exemplo: BASE_DIR / "templates" em vez de os.path.join(BASE_DIR, "templates").

import dj_database_url
# Importa a biblioteca "dj_database_url", externa ao Django.
# Essa biblioteca transforma uma URL de conexão de banco de dados em um dicionário de configuração
# no formato esperado pelo Django.
# Exemplo: converte "postgres://user:senha@host:5432/dbname" em DATABASES['default'].

from google.oauth2 import service_account
# Importa a classe service_account do módulo google.oauth2 (Google SDK).
# Permite carregar credenciais de autenticação de um arquivo JSON de "Service Account" do Google Cloud.
# Essas credenciais são usadas para acessar serviços como o Google Cloud Storage (GCS).

RENDER = os.environ.get('RENDER') == 'TRUE'
# Cria a variável booleana RENDER.
# - Busca a variável de ambiente "RENDER".
# - Se o valor for a string "TRUE", a variável será True, senão será False.
# Serve para detectar se o app está rodando na plataforma Render.com.

DEBUG = not RENDER
# Cria a variável DEBUG.
# DEBUG é True quando RENDER for False (modo de desenvolvimento).
# DEBUG é False quando RENDER for True (modo de produção).
# Em DEBUG=True:
#   - Django mostra páginas de erro detalhadas.
#   - Django serve arquivos estáticos diretamente.
# Em DEBUG=False:
#   - Páginas de erro são ocultadas.
#   - Necessário servidor/provedor para arquivos estáticos.
#   - Mais seguro para produção.

# ---------------------------------------------------
# URL padrão do banco para desenvolvimento local
# ---------------------------------------------------
LOCAL_DATABASE_URL = 'postgresql://jcog:MON010deo010@localhost:5432/fusion'
# String de conexão para PostgreSQL local.
# Formato: postgresql://usuario:senha@host:porta/nome_do_banco
# Usada como banco padrão durante desenvolvimento.

# ---------------------------------------------------
# Configuração do banco de dados
# ---------------------------------------------------
if DEBUG:
    # Se DEBUG=True, significa que o projeto está em ambiente de desenvolvimento.

    DATABASES = {
        'default': dj_database_url.config(
            default=LOCAL_DATABASE_URL,
            # Se não existir a variável de ambiente DATABASE_URL, usa LOCAL_DATABASE_URL.
            conn_max_age=600,
            # Mantém conexões abertas por até 600 segundos (10 minutos).
            # Isso evita recriar conexão a cada requisição (ganho de performance).
            ssl_require=False
            # Não exige SSL em localhost (ambiente de desenvolvimento).
        )
    }
else:
    # Se DEBUG=False, significa que o projeto está em ambiente de produção.

    DATABASES = {
        'default': dj_database_url.config(
            default=LOCAL_DATABASE_URL,
            # Caso DATABASE_URL não esteja definida no ambiente, ainda usa LOCAL_DATABASE_URL como fallback.
            conn_max_age=600,
            # Mantém conexões abertas por até 10 minutos em produção.
            ssl_require=True
            # Exige SSL na conexão com o banco de dados em produção.
            # Isso garante criptografia entre servidor e banco remoto.
        )
    }

# Explicação detalhada de cada parâmetro:
# - default: URL do banco usada caso a variável DATABASE_URL não exista.
# - conn_max_age: tempo de reuso das conexões abertas.
# - ssl_require: se True, obriga conexão criptografada via SSL.
# - dj_database_url.config(): converte URL de banco para dict no formato esperado por Django.
# - DATABASES['default']: dicionário de configuração usado pelo Django para conectar ao banco.

# =============================================
# BASE_DIR
# =============================================
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR aponta para a pasta raiz do projeto (onde está manage.py).
# __file__: caminho absoluto deste arquivo settings.py.
# .resolve(): converte em caminho absoluto, resolvendo links simbólicos.
# .parent: sobe um nível (do arquivo para a pasta do app).
# .parent.parent: sobe outro nível, até a raiz do projeto.
# Isso evita caminhos fixos no código e torna o projeto portátil.

# =============================================
# SEGURANÇA
# =============================================
SECRET_KEY = 'django-insecure-9ws=#c@fv-y%#a3%b8ua422auu)#eq5$m%93tc0kv3d*ih8#vj'
# Chave secreta do Django.
# Usada internamente para:
#   - Assinar cookies de sessão.
#   - Proteger formulários CSRF.
#   - Criar hashes criptográficos.
# Deve ser mantida em segredo em produção (ideal em variável de ambiente).

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']
# Lista de hosts/domínios autorizados a acessar o projeto.
# Protege contra ataque "Host header injection".
# Durante desenvolvimento, aceita localhost, 127.0.0.1 e testserver (para testes).

if not DEBUG:
    # Só executa este bloco se for produção (DEBUG=False).

    external = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    # Captura o hostname externo fornecido pela Render.com.
    # Exemplo: "meu-app-xyz.onrender.com".

    if external:
        ALLOWED_HOSTS.append(external)
        # Adiciona o hostname externo válido à lista de hosts permitidos.

    ALLOWED_HOSTS.append('.onrender.com')
    # Permite qualquer subdomínio do domínio onrender.com (*.onrender.com).
    # Útil se a aplicação for acessada por múltiplos subdomínios no Render.

# =============================================
# INSTALLED_APPS
# =============================================
INSTALLED_APPS = [
    'django.contrib.admin',
    # Admin: interface administrativa do Django.
    'django.contrib.auth',
    # Auth: sistema de autenticação de usuários e permissões.
    'django.contrib.contenttypes',
    # Contenttypes: sistema de tipos de conteúdo genérico, usado por permissões.
    'django.contrib.sessions',
    # Sessions: armazena dados de sessão de usuários.
    'django.contrib.messages',
    # Messages: sistema de mensagens "flash".
    'django.contrib.staticfiles',
    # Staticfiles: gerenciamento de arquivos estáticos (CSS, JS, imagens).

    'core',
    # App principal do projeto (definido pelo desenvolvedor).
    'bootstrap4',
    # Integração de templates com Bootstrap 4.
    'stdimage',
    # Biblioteca para manipulação de imagens e thumbnails.
    'pictures',
    # Geração de imagens responsivas (diferentes tamanhos para diferentes dispositivos).
    'storages'
    # Biblioteca django-storages, para integrar armazenamento remoto (S3, GCS).
]
# Cada app registrado:
# - É inicializado automaticamente quando o servidor sobe.
# - Registra seus models.
# - Disponibiliza templates, arquivos estáticos e signals.

# =============================================
# MIDDLEWARE
# =============================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Middleware de segurança do Django.
    # Adiciona headers HTTP de segurança (HSTS, X-Content-Type-Options).
    # Protege contra ataques como XSS, MIME sniffing, etc.

    'django.contrib.sessions.middleware.SessionMiddleware',
    # Middleware de sessões.
    # Habilita request.session para armazenar dados temporários do usuário.

    'django.middleware.common.CommonMiddleware',
    # Middleware de utilidades comuns.
    # Exemplo: adiciona barra final às URLs se faltando (APPEND_SLASH).

    'django.middleware.csrf.CsrfViewMiddleware',
    # Middleware de proteção CSRF (Cross-Site Request Forgery).
    # Valida o token CSRF em formulários POST/PUT/DELETE.

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # Middleware de autenticação.
    # Adiciona request.user com o usuário logado (ou AnonymousUser).

    'django.contrib.messages.middleware.MessageMiddleware',
    # Middleware de mensagens "flash".
    # Usa sessões para armazenar mensagens temporárias entre requests.

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Middleware anti-clickjacking.
    # Adiciona cabeçalho X-Frame-Options: SAMEORIGIN.
    # Impede que a página seja embutida em iframes externos.
]
# Ordem dos middlewares é importante:
# - SessionMiddleware deve vir antes de AuthenticationMiddleware.
# - CSRF precisa vir antes de views que validam POST.
# - SecurityMiddleware sempre no topo para aplicar regras cedo.

# =============================================
# URLS E TEMPLATES
# =============================================
ROOT_URLCONF = 'fusion.urls'
# Aponta para o módulo de configuração de URLs do projeto (fusion/urls.py).
# Este módulo contém urlpatterns que roteiam requisições para views.

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Define o mecanismo de templates usado: DjangoTemplates (motor nativo do Django).
        'DIRS': [BASE_DIR / 'templates'],
        # Lista de diretórios adicionais para procurar templates fora dos apps.
        'APP_DIRS': True,
        # Se True, procura templates automaticamente em cada app instalado (pasta /templates).
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                # Insere o objeto request em todos os templates.
                'django.contrib.auth.context_processors.auth',
                # Insere variáveis user e perms nos templates.
                'django.contrib.messages.context_processors.messages',
                # Insere mensagens flash nos templates.
            ],
        },
    },
]
# Context processors são funções que inserem variáveis globais nos templates.
# Permitem usar objetos como request, user e messages diretamente no HTML.

# =============================================
# CONFIGURAÇÃO DA BIBLIOTECA PICTURES
# =============================================
PICTURES = {
    "BREAKPOINTS": {'thumb': 480, "mobile": 576, "tablet": 768, "desktop": 992},
    # Define larguras de tela (em pixels) para gerar versões diferentes das imagens.
    "GRID_COLUMNS": 1,
    # Número de colunas lógicas do grid.
    "CONTAINER_WIDTH": 480,
    # Largura máxima do container.
    "FILE_TYPES": ["WEBP", "JPG", "JPEG", "BMP", "PNG"],
    # Formatos de arquivos de imagem suportados.
    "PIXEL_DENSITIES": [1],
    # Escalas de densidade (1x, 2x, etc).
    "USE_PLACEHOLDERS": True,
    # Ativa placeholders enquanto imagens reais carregam.
}

# =============================================
# WSGI
# =============================================
WSGI_APPLICATION = 'fusion.wsgi.application'
# Caminho para o objeto WSGI da aplicação.
# Servidores como Gunicorn e uWSGI usam este objeto para servir o projeto.

# =============================================
# VALIDADORES DE SENHA
# =============================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    # Validador: proíbe senhas parecidas com atributos do usuário (nome, email).
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    # Validador: exige comprimento mínimo de senha (padrão 8).
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    # Validador: bloqueia senhas comuns (ex: "123456", "password").
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
    # Validador: bloqueia senhas compostas apenas por números.
]

# =============================================
# INTERNACIONALIZAÇÃO
# =============================================
LANGUAGE_CODE = 'pt-br'
# Define idioma padrão como português do Brasil.

TIME_ZONE = 'America/Sao_Paulo'
# Define fuso horário padrão (São Paulo, Brasil).

USE_I18N = True
# Ativa suporte à internacionalização (tradução de textos).

USE_TZ = True
# Usa fuso horário UTC no banco de dados e converte para local quando necessário.

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Define o tipo padrão de campo para chaves primárias.
# BigAutoField cria IDs longos (64 bits).

# -------------------------------------------------------------------
# Configuração para autenticação e acesso ao Google Cloud Storage (GCS)
# -------------------------------------------------------------------

path_credenciais = None
# Variável para armazenar caminho do arquivo JSON de credenciais do Google Cloud.

filename = "credenciais.json"
# Nome esperado do arquivo de credenciais JSON.

GS_CREDENTIALS = None
# Variável para armazenar objeto de credenciais carregado.

if not DEBUG:
    # Caso esteja em produção (DEBUG=False):

    path_credenciais = "/etc/secrets/" + filename
    # Caminho fixo em produção (Render.com monta credenciais em /etc/secrets).

    if os.path.exists(path_credenciais):
        GS_CREDENTIALS = service_account.Credentials.from_service_account_file(path_credenciais)
        # Carrega credenciais a partir do arquivo JSON.
        # from_service_account_file retorna objeto GS_CREDENTIALS.
    else:
        raise Exception(f"O arquivo {path_credenciais} não existe!")
        # Se arquivo não for encontrado, lança exceção crítica.

else:
    # Caso esteja em desenvolvimento (DEBUG=True):

    path_credenciais = os.path.join(BASE_DIR, filename)
    # Procura credenciais na raiz do projeto (local).

    if os.path.exists(path_credenciais):
        GS_CREDENTIALS = service_account.Credentials.from_service_account_file(path_credenciais)
        # Carrega credenciais a partir do arquivo JSON.
    else:
        raise Exception(f"O arquivo {path_credenciais} não existe!")
        # Se não encontrar arquivo local, lança exceção.

# -------------------------------------------------------------------
# Configurações do Google Cloud Storage para arquivos estáticos e mídia
# -------------------------------------------------------------------

GS_BUCKET_NAME = "django-render"
# Nome do bucket no Google Cloud Storage que armazenará arquivos estáticos e mídia.

if not DEBUG:
    # Em produção:

    STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"
    # URL pública para arquivos estáticos (servidos pelo GCS).

    MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"
    # URL pública para arquivos de mídia.

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
    # STORAGES define como arquivos estáticos e de mídia serão salvos/servidos.
    # "default": armazena arquivos de mídia enviados por usuários.
    # "staticfiles": armazena arquivos estáticos do projeto (CSS, JS).
    # Ambos usam o mesmo bucket, mas organizados em subpastas ("media" e "static").

    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    # Define backend padrão para uploads de mídia (usuários).

    STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    # Define backend para arquivos estáticos (CSS/JS).

else:
    # Em desenvolvimento local:

    STATIC_URL = '/static/'
    # URL para acessar arquivos estáticos localmente.

    MEDIA_URL = '/media/'
    # URL para acessar arquivos de mídia localmente.

    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Pasta local onde collectstatic junta arquivos estáticos.

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    # Pasta local para armazenar uploads de usuários.

    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    # Backend de armazenamento de mídia local (disco do servidor).

    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    # Backend de armazenamento de arquivos estáticos local.
    # Copia arquivos para STATIC_ROOT ao rodar collectstatic.

    if DEBUG:
        EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
        # Em desenvolvimento: envia emails apenas imprimindo no console.

    LOGOUT_REDIRECT_URL = 'index'
    # URL para redirecionar após logout.

    """
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_PASSWORD = '<PASSWORD>'
    EMAIL_HOST_USER = 'no-reply@seudominio.com'
    """
    # Configurações de envio de email via SMTP (comentadas).
    # Usadas para funcionalidades como reset de senha.
