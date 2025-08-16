#!/bin/bash
set -e
# ===============================================
# Configuração de segurança do script
# ===============================================
# Faz o script parar imediatamente se algum comando retornar erro.
# Isso é fundamental em deploys automáticos para evitar que erros passem despercebidos
# e o ambiente fique parcialmente configurado.

echo "Instalando dependências"
# ===============================================
# Etapa 1: Instalação de bibliotecas Python
# ===============================================
# Mensagem informativa apenas para registrar no log que esta etapa começou.
pip install -r requirements.txt
# Instala todas as dependências listadas no arquivo requirements.txt.
# Explicação detalhada:
# - Cada biblioteca listada lá é instalada no ambiente virtual do Python.
# - Isso garante que o Django e todas as bibliotecas auxiliares (como dj_database_url, django-storages, etc.) estejam disponíveis.
# - Se faltar alguma dependência, essa etapa falha e o deploy para automaticamente.

echo "Executando migrações"
# ===============================================
# Etapa 2: Atualização da estrutura do banco
# ===============================================
# Mensagem informativa que indica que o banco de dados será sincronizado com os modelos do Django.

python manage.py migrate --noinput
# Comando do Django que aplica todas as migrações pendentes.
# Explicação detalhada:
# - Cada "migration" é um arquivo que descreve alterações na estrutura do banco (criar tabela, coluna, índice, etc.).
# - --noinput faz o comando rodar sem pedir confirmação. Isso é essencial em deploys automáticos.
# - Garantia: após esse comando, o banco estará compatível com o código atual da aplicação.
# - Se houver falha (como conflito de migration), o deploy será interrompido por causa do `set -e`.

echo "Coletando arquivos estáticos"
# ===============================================
# Etapa 3: Preparação de arquivos estáticos
# ===============================================
# Mensagem informativa para mostrar no log que a coleta começou.

python manage.py collectstatic --noinput
# Explicação detalhada:
# - O Django precisa que todos os arquivos estáticos (CSS, JS, imagens) fiquem em um único diretório (STATIC_ROOT) para produção.
# - collectstatic copia arquivos de cada app e do diretório "static" do projeto para STATIC_ROOT.
# - --noinput evita perguntas de confirmação durante o processo.
# - Isso garante que o servidor de produção consiga servir todos os recursos corretamente.

echo "Carregando dados iniciais"
# ===============================================
# Etapa 4: Inserção de dados essenciais (fixtures)
# ===============================================
# Mensagem informativa para logar o início do carregamento de dados.

python manage.py loaddata backup_cargo.json
python manage.py loaddata backup_equipe.json
python manage.py loaddata backup_servico.json
# Explicação detalhada:
# - loaddata importa dados do banco a partir de arquivos JSON.
# - Cada arquivo contém uma "fixture" com registros essenciais.
# - Exemplos: cargos da empresa, equipes, serviços cadastrados.
# - Isso é útil para inicializar o ambiente de produção com dados básicos que o site precisa para funcionar.
# - Se algum arquivo estiver faltando ou corrompido, o deploy falha devido ao `set -e`.

echo "Sincronizando mídia com bucket GCS"
# ===============================================
# Etapa 5: Upload de arquivos de mídia (uploads de usuários)
# ===============================================
# Mensagem informativa para logar o início da sincronização.

python manage.py upload_media
# Explicação detalhada:
# - upload_media é um comando customizado que envia o conteúdo da pasta local "media" para o bucket do Google Cloud Storage.
# - Garantia: todas as imagens, vídeos e outros arquivos de mídia estarão acessíveis em produção.
# - Isso é crítico para que recursos visuais e uploads de usuários funcionem corretamente.
# - Certifique-se de que o comando esteja implementado e funcionando antes do deploy.

echo "Criando superusuário se não existir"
# ===============================================
# Etapa 6: Criação automática de superusuário
# ===============================================
# Mensagem informativa que indica que a verificação e criação do admin está começando.

python manage.py shell << EOF
from django.contrib.auth.models import User
# Importa o modelo padrão de usuários do Django.
# User é a classe que representa cada conta de usuário no sistema.

if not User.objects.filter(username='jcogfisica').exists():
    # Verifica se já existe um superusuário com o username 'jcogfisica'.
    # Evita criar duplicatas, o que causaria erro.

    User.objects.create_superuser('jcogfisica', 'jcogfisica@yahoo.com.br', 'MON010deo010')
    # Cria um superusuário com:
    # - username: 'jcogfisica'
    # - email: 'jcogfisica@yahoo.com.br'
    # - senha: 'MON010deo010'
    # Superusuário pode acessar o admin e gerenciar todos os dados da aplicação.
EOF
# O bloco EOF executa comandos Python dentro do shell do Django, permitindo manipulação direta do banco de dados.

echo "Build concluído!"
# ===============================================
# Mensagem final indicando que todas as etapas do deploy foram concluídas com sucesso.
# Garantia de que:
# - Dependências foram instaladas
# - Migrações aplicadas
# - Arquivos estáticos coletados
# - Dados essenciais carregados
# - Mídia sincronizada
# - Superusuário criado (se necessário)
