import logging

# Cria logger padrão do Django
logger = logging.getLogger(__name__)

class RequestLoggerMiddleware:
    """
    Middleware que registra detalhes de cada requisição.
    Funciona em produção e no Render sem quebrar a página.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Loga informações da requisição
        logger.info(f"[DEBUG] Acessando URL: {request.path}")
        logger.info(f"[DEBUG] Método HTTP: {request.method}")
        logger.info(f"[DEBUG] IP do cliente: {self.get_client_ip(request)}")

        # Continua processamento normal
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Tenta pegar IP real do cliente"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR", "")
        return ip
