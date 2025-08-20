from django.test import TestCase
# Importa a classe `TestCase` do módulo `django.test`.
# `TestCase` é uma classe base do Django que herda de `unittest.TestCase`.
# Ela é usada para criar testes automatizados integrados ao Django.
# Essa classe já traz recursos extras, como:
# - uso de um banco de dados de teste (criado e destruído automaticamente),
# - ferramentas para verificar respostas HTTP,
# - utilitários para criar dados de teste com fixtures.

from core.forms import ContactForm
# Importa o formulário `ContactForm` definido no arquivo `forms.py` do app `core`.
# Esse é o formulário que será testado aqui, garantindo que ele funcione conforme esperado.


class ContactFormTestCase(TestCase):
    # Define uma classe de testes chamada `ContactFormTestCase`.
    # Essa classe herda de `TestCase`, logo, pode utilizar toda a infraestrutura
    # de testes do Django.
    # Pelo nome, essa classe será usada para testar especificamente o formulário
    # `ContactForm`.

    def setUp(self):
        # Metodo especial chamado antes de cada teste ser executado.
        # Serve para configurar o ambiente de teste, criando dados iniciais
        # que serão usados em diferentes métodos de teste.

        self.nome = "Felicity Jones"
        # Define um atributo `nome` que simula o valor preenchido no formulário.
        # Aqui usamos um nome fictício de exemplo.

        self.email = "felicity@gmail.com"
        # Define um e-mail válido de exemplo que será usado nos testes.

        self.assunto = "Um assunto qualquer"
        # Define um assunto de exemplo, simulando a entrada do usuário no formulário.

        self.message = "Uma mensagem qualquer"
        # Define a mensagem de texto, simulando o campo de texto preenchido.

        self.dados = {
            "nome": self.nome,
            "email": self.email,
            "assunto": self.assunto,
            "mensagem": self.message,
        }
        # Cria um dicionário `self.dados` que contém todos os campos necessários
        # para instanciar e validar o `ContactForm`.
        # As chaves correspondem exatamente aos nomes definidos no formulário
        # (nome, email, assunto, mensagem).

        self.form = ContactForm(data = self.dados) # ContatForm(request.POST)
        # Cria uma instância de `ContactForm`, passando o dicionário como `data`.
        # Isso simula o envio de um formulário com dados preenchidos,
        # semelhante ao que aconteceria com `ContactForm(request.POST)` em uma view.


    def test_send_email(self):
        # Define um metodo de teste chamado `test_send_email`.
        # Cada um dos metodos de teste deve começar com `test_` para ser reconhecido pelo framework.
        # Este metodo vai verificar se o envio de e-mail do formulário funciona corretamente.

        form1 = ContactForm(data = self.dados)
        # Cria a primeira instância do formulário `ContactForm`, usando os mesmos dados definidos no setUp.

        form1.is_valid()
        # Chama o metodo `is_valid()` que:
        # - valida os dados do formulário,
        # - executa os validadores de cada campo,
        # - popula o atributo `cleaned_data` caso os dados sejam válidos.
        # Isso é necessário antes de chamar `send_email`, pois `send_email` depende de `cleaned_data`.

        res1 = form1.send_email()
        # Chama o metodo `send_email()` do formulário e armazena o resultado em `res1`.
        # Esse metodo deve enviar um e-mail (de acordo com a implementação no forms.py)
        # e possivelmente retornar algo (ou apenas `None`).

        form2 = self.form
        # Usa a instância do formulário já criada no `setUp` (`self.form`).

        form2.is_valid()
        # Novamente, valida o formulário para garantir que `cleaned_data` esteja populado.

        res2 = form2.send_email()
        # Chama o metodo `send_email()` para enviar o e-mail usando a segunda instância.
        # O resultado será armazenado em `res2`.

        self.assertEqual(res1, res2)
        # Compara os resultados dos dois envios (`res1` e `res2`) para garantir
        # que ambos sejam iguais.
        # Isso assegura que o envio do e-mail é consistente,
        # independentemente da instância usada para chamar o metodo.
