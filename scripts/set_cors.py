from google.cloud import storage


def cors_configuration(bucket_name):
    """
    Configura a política CORS do bucket para permitir que fontes e outros
    arquivos estáticos sejam carregados corretamente pelo navegador.

    Args:
        bucket_name (str): Nome do bucket no Google Cloud Storage.
    Returns:
        bucket: Objeto do bucket com CORS configurado.
    """
    # Inicializa o cliente do Google Cloud Storage
    storage_client = storage.Client()

    # Recupera o bucket pelo nome
    bucket = storage_client.get_bucket(bucket_name)

    # Define a política CORS
    bucket.cors = [
        {
            "origin": ["https://mysite-j65t.onrender.com"],  # permite acesso apenas deste domínio
            "method": ["GET", "HEAD", "OPTIONS"],  # métodos HTTP permitidos
            "responseHeader": ["*"],  # permite todos os headers de resposta
            "maxAgeSeconds": 31536000  # cache do preflight por 1 ano (em segundos)
        }
    ]

    # Aplica a política no bucket
    bucket.patch()

    # Imprime confirmação
    print(f"CORS configurado no bucket {bucket.name}: {bucket.cors}")

    return bucket


# Executa a função se o script for chamado diretamente
if __name__ == "__main__":
    cors_configuration("django-render")

