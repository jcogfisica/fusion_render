import os
# Biblioteca padrão do Python para interagir com o sistema operacional.
# Fornece funcionalidades para manipular caminhos de arquivos, navegar por diretórios,
# ler variáveis de ambiente, executar comandos do SO, entre outras operações.

from django.core.management.base import BaseCommand
# Importa a classe BaseCommand do módulo django.core.management.base.
# BaseCommand é a classe base para criar comandos customizados no Django.
# Esses comandos podem ser executados via manage.py e são úteis para tarefas administrativas,
# como sincronizar arquivos, limpar dados, gerar relatórios etc.

from google.cloud import storage
# Importa o módulo 'storage' da SDK oficial do Google Cloud.
# Essa biblioteca fornece classes e métodos para interagir com o Google Cloud Storage (GCS),
# que é o serviço de armazenamento de arquivos na nuvem do Google.
# Permite criar clientes, acessar buckets (containers de arquivos), criar blobs (arquivos),
# fazer upload, download, listagem e exclusão de arquivos no bucket.

from google.oauth2 import service_account
# Importa a classe service_account do pacote google.oauth2.
# Essa classe permite carregar credenciais (chaves) de uma conta de serviço do Google,
# normalmente armazenadas em arquivos JSON, para autenticar e autorizar acessos às APIs Google,
# como a do Cloud Storage. Essencial para operações seguras via SDK.

import traceback
# Biblioteca padrão para imprimir o rastreamento de exceções (útil para debug detalhado).

def upload_media_to_gcs(local_media_path, bucket_name, credentials, prefix='media'):
    """
    Função que sincroniza recursivamente os arquivos da pasta local_media_path (local)
    para o bucket do Google Cloud Storage (GCS) especificado, dentro da pasta prefix (padrão: 'media').

    Parâmetros:
    - local_media_path (str): Caminho absoluto ou relativo para a pasta local que contém os arquivos a enviar.
    - bucket_name (str): Nome do bucket GCS onde os arquivos serão armazenados.
    - credentials (google.oauth2.service_account.Credentials): Objeto contendo as credenciais para autenticação no GCS.
    - prefix (str): Prefixo/pasta dentro do bucket para organizar os arquivos. Por padrão 'media'.

    Essa função faz upload dos arquivos mantendo a estrutura de pastas relativa dentro do prefixo.
    """

    client = storage.Client(credentials = credentials)
    # Cria um cliente autenticado para se comunicar com o Google Cloud Storage.
    # O objeto 'client' é uma instância da classe google.cloud.storage.Client,
    # que representa o ponto de entrada para interagir com o serviço GCS.

    bucket = client.bucket(bucket_name)
    # Obtém uma referência ao bucket no GCS pelo nome fornecido.
    # 'bucket' é uma instância da classe google.cloud.storage.bucket.Bucket,
    # que representa um container lógico de objetos (arquivos) dentro do GCS.

    success_count = 0
    error_count = 0
    total_count = 0
    # Contadores de sucesso/erro para relatório final

    for root, dirs, files in os.walk (local_media_path):
    # Percorre a árvore de diretórios da pasta local_media_path usando os.walk do módulo os.
    # os.walk gera uma tupla (root, dirs, files) para cada diretório:
    # - root: caminho atual sendo percorrido,
    # - dirs: lista de subdiretórios dentro de root,
    # - files: lista de arquivos dentro de root.
    # Aqui usamos para processar todos os arquivos de forma recursiva.

        # print(f"[DEBUG] upload_media_to_gcs - diretório atual: {root}")
        # DEBUG: indica em que diretório estamos iterando

        if dirs:
            # print(f"[DEBUG] upload_media_to_gcs - subpastas encontradas: {dirs}")
            # DEBUG: lista subpastas no diretório atual
            pass

        if files:
            # print(f"[DEBUG] upload_media_to_gcs - arquivos encontrados: {files}")
            # DEBUG: lista arquivos no diretório atual
            pass

        for filename in files:
            total_count += 1

            local_path = os.path.join(root, filename)
            # Junta o caminho do diretório atual 'root' com o nome do arquivo,
            # formando o caminho absoluto ou relativo completo para o arquivo local.

            if os.path.getsize(local_path) == 0:
                # print(f"Aviso: Ignorando arquivo vazio {local_path}")
                continue
                # Ignorar arquivos vazios (tamanho 0 bytes)

            relative_path = os.path.relpath(local_path, local_media_path)
            # Calcula o caminho relativo do arquivo em relação ao diretório base local_media_path.
            # Isso é importante para preservar a estrutura de pastas ao enviar para o bucket.
            # Exemplo: se local_path = "media/uploads/img.jpg" e local_media_path = "media",
            # relative_path será "uploads/img.jpg".

            gcs_path = f"{prefix}/{relative_path.replace(os.sep, '/')}"
            # Gera o caminho final dentro do bucket, concatenando o prefixo com o caminho relativo do arquivo.
            # Substitui '\' por '/' para garantir compatibilidade com a forma Unix de caminhos no GCS,
            # pois GCS usa caminhos estilo URL (com '/').

            # print(f"[DEBUG] upload_media_to_gcs - preparando upload: {local_path} -> gs://{bucket_name}/{gcs_path}")
            # DEBUG: mostra o mapeamento local -> remoto antes do upload

            blob = bucket.blob(gcs_path)
            # Cria um objeto Blob no bucket, que representa um arquivo armazenado em GCS.
            # A classe google.cloud.storage.blob.Blob encapsula funcionalidades para upload,
            # download e manipulação de arquivos no bucket.

            try:
                blob.upload_from_filename(local_path)
                # Faz upload do arquivo local para o blob no bucket usando o caminho do arquivo local.
                # O metodo upload_from_filename lê o arquivo local e envia seu conteúdo para o GCS.

                # print(f"Uploaded {local_path} to gs://{bucket_name}/{gcs_path}")
                # Imprime no terminal uma mensagem indicando que o upload foi concluído para aquele arquivo.
                # Útil para monitorar o progresso do script durante a execução.
                success_count += 1

            except Exception as e:
                # print(f"Erro ao fazer upload do arquivo {local_path}: {e}")
                # Caso ocorra algum erro durante o upload, imprime o erro no terminal
                # DEBUG: imprime traceback completo para diagnóstico
                traceback.print_exc()
                error_count += 1

    # print(f"Upload finalizado: total verificados: {total_count}, enviados com sucesso: {success_count}, falhas: {error_count}")
    # Relatório final resumido

class Command(BaseCommand):
    """
    Classe que define o comando customizado Django para sincronizar arquivos locais da pasta 'media'
    com o bucket do Google Cloud Storage.

    - Essa classe herda de BaseCommand e deve estar localizada dentro de uma pasta
      'management/commands' de algum app Django para ser reconhecida.

    - Pode ser executada via linha de comando Django com:
      python manage.py sync_media
    """

    help = "Sincroniza a pasta media local com o bucket Google Cloud Storage."
    # Atributo de classe 'help' que fornece uma descrição curta do que o comando faz,
    # exibida quando o usuário roda `python manage.py help sync_media`.

    def handle(self, *args, **kwargs):
        """
        Metodo principal executado quando o comando customizado é chamado via manage.py.

        Passos:
        1. Obtém o caminho da pasta local 'media' onde estão os arquivos a enviar.
        2. Define o nome do bucket do Google Cloud Storage (GCS) onde os arquivos serão enviados.
        3. Define o caminho do arquivo de credenciais local 'credenciais.json'.
        4. Verifica se a pasta 'media' existe e se tem arquivos para enviar.
        5. Verifica se o arquivo de credenciais existe; caso contrário, interrompe com erro.
        6. Carrega as credenciais a partir do arquivo local usando a classe
           `service_account.Credentials.from_service_account_file`.
        7. Chama a função `upload_media_to_gcs` para sincronizar os arquivos da pasta local
           com o bucket do GCS usando as credenciais autenticadas.
        8. Imprime uma mensagem de sucesso no terminal.
        """

        local_media_path = os.path.join(os.getcwd(), "media")
        # Passo 1: Define o caminho da pasta 'media' no diretório atual do projeto

        if not os.path.exists(local_media_path):
            self.stdout.write(self.style.ERROR(f"Pasta '{local_media_path}' não encontrada. Abortando sincronização."))
            return
        if not any(os.scandir(local_media_path)):
            self.stdout.write(self.style.WARNING(f"Pasta '{local_media_path}' está vazia. Nada para sincronizar."))
            return  # Interrompe execução se pasta estiver vazia
        # Verificação extra: se a pasta 'media' não existe ou está vazia, avisa e encerra

        total_files = 0
        for _, _, files in os.walk(local_media_path):
            total_files += len(files)
        # print(f"[DEBUG] handle - total de arquivos encontrados em '{local_media_path}': {total_files}")
        # DEBUG: conta total de arquivos na pasta media (recursivamente)

        bucket_name = "django-render"
        # Passo 2: Nome do bucket no Google Cloud Storage (ajuste conforme seu bucket)

        cred_file_path = os.path.join(os.getcwd(), "credenciais.json")
        # Passo 3: Define o caminho local para o arquivo de credenciais JSON

        # print(f"[DEBUG] handle - cred_file_path = {cred_file_path}, existe? {os.path.exists(cred_file_path)}")
        # DEBUG: informa se o arquivo de credenciais existe

        if not os.path.exists(cred_file_path):
            raise Exception(f"Arquivo de credenciais '{cred_file_path}' não encontrado. Impossível autenticar no Google Cloud Storage.")
        # Passo 5: Verifica se o arquivo de credenciais existe

        credentials = service_account.Credentials.from_service_account_file(cred_file_path)
        # DEBUG: confirma tipo de objeto de credenciais carregado (sem imprimir conteúdo sensível)
        # print(f"[DEBUG] handle - credenciais carregadas: {type(credentials)}")
        # Passo 6: Carrega as credenciais do arquivo JSON local

        # print("[DEBUG] handle - iniciando upload_media_to_gcs()")
        upload_media_to_gcs(local_media_path, bucket_name, credentials)
        # Passo 7: Chama a função que faz o upload dos arquivos locais para o bucket GCS

        self.stdout.write(self.style.SUCCESS("Sincronização concluída com sucesso!"))
        # Passo 8: Imprime mensagem de sucesso na saída padrão do Django
