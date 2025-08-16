# core/middleware.py
class DebugTemplateContextMiddleware:
    """
    Middleware para depurar o template da homepage.
    Ele captura o contexto enviado ao template e força um erro proposital
    para gerar log completo no Render.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Executa a view e obtém a response
        response = self.get_response(request)

        # Só queremos debugar a homepage
        if request.path == "/":
            try:
                # Se for uma TemplateResponse, podemos acessar o contexto
                context_data = getattr(response, 'context_data', None)
                print("DEBUG: Contexto da homepage:", context_data)
            except Exception as e:
                print("DEBUG: Não foi possível acessar o contexto:", str(e))

            # Força um erro proposital para gerar o log completo no Render
            raise Exception("Debug: Página index já renderizada no Render")

        # Retorna a response normalmente para outras URLs
        return response
