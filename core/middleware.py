# core/middleware.py
class DebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/":  # Só dispara para a homepage
            raise Exception("Debug: Página index acessada no Render")  # <-- força erro
        response = self.get_response(request)
        return response