# core/middleware.py

import logging

logger = logging.getLogger(__name__)

class DebugIndexMiddleware:
    """
    Middleware que apenas registra debug da homepage.
    Não intercepta exceções para que elas sejam logadas pelo Django/Gunicorn.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/':
            logger.debug(f"Acessando homepage - Método: {request.method}, IP: {self.get_client_ip(request)}")
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
