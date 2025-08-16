# core/middleware.py
class DebugAfterRenderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)  # Primeiro deixa o Django gerar a response
        if request.path == "/":  # Só dispara para a homepage
            # Garante que só vai lançar o erro depois de processar a view/template
            raise Exception("Debug: Página index já renderizada no Render")
        return response
