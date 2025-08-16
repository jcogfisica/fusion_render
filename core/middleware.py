# core/middleware.py

from django.template.loader import get_template, TemplateDoesNotExist
from django.http import HttpResponse, HttpResponseServerError
import logging

logger = logging.getLogger(__name__)

class DebugIndexMiddleware:
    """
    Middleware que registra debug da homepage e verifica se index.html existe.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Debug básico
        if request.path == '/':
            logger.debug(f"Acessando homepage - Método: {request.method}, IP: {self.get_client_ip(request)}")

            # Verifica se index.html existe
            try:
                get_template('index.html')
            except TemplateDoesNotExist:
                logger.error("Template index.html não encontrado!")
                return HttpResponseServerError("Erro interno: index.html não encontrado.")

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
