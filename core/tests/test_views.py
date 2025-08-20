from django.test import TestCase
# Importa a classe `TestCase` do Django.
# Permite criar testes automatizados integrados ao Django,
# incluindo acesso ao banco de dados de teste e métodos auxiliares.

from django.test import Client
# Importa o `Client` do Django, que simula um navegador para fazer
# requisições GET e POST às views do Django.
# Útil para testar o comportamento das views sem precisar de um navegador real.

from django.urls import reverse_lazy
# Importa `reverse_lazy`, que gera URLs a partir do nome da rota.
# Usamos `reverse_lazy` em testes para evitar problemas de carregamento
# das URLs antes da inicialização do Django.


# ======================================================================
# Testes para a view IndexView
# ======================================================================
class IndexViewTestCase(TestCase):
    # Define a classe de teste para a página inicial (`IndexView`).
    # Herdando de `TestCase`, podemos testar requisições GET e POST
    # simulando um usuário interagindo com o formulário.


    def setUp(self):
        # Executado antes de cada teste.
        # Define dados de formulário válidos para simular envio.
        self.dados = {
            "nome" : "Felicity Jones",
            "email" : "felicity@gmail.com",
            "assunto" : "Um assunto qualquer",
            "mensagem" : "Uma mensagem qualquer",
        }

        self.cliente = Client()
        # Cria uma instância do `Client`, que será usada para enviar
        # requisições HTTP simuladas às views.


    def test_form_valid(self):
        # Testa o envio de formulário com dados válidos.
        request = self.cliente.post(
            path = reverse_lazy("index"),  # Gera a URL da view 'index'
            data = self.dados               # Passa os dados completos do formulário
        )
        self.assertEqual(302, request.status_code)
        # Verifica se a resposta HTTP é 302 (redirecionamento),
        # que indica que o formulário foi enviado com sucesso
        # e a view redirecionou para success_url.


    def test_form_invalid(self):
        # Testa o envio de formulário com dados incompletos.
        dados_incompletos = {
            "nome" : "Felicity Jones",
            "email" : "felicity@gmail.com",
            # Campos 'assunto' e 'mensagem' estão faltando
        }
        request = self.cliente.post(
            path = reverse_lazy("index"),  # URL da view 'index'
            data = dados_incompletos       # Passa dados incompletos para simular erro
        )
        self.assertEqual(200, request.status_code)
        # Verifica se a resposta HTTP é 200 (reexibe o formulário com erros),
        # que indica que a view não redirecionou porque o formulário é inválido.



