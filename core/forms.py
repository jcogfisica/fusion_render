from django import forms
# Importa o módulo `forms` do Django, que fornece classes e ferramentas
# para criar formulários HTML de maneira simples e integrada com o framework.
# Isso nos permite validar dados e estruturar entradas de usuários de forma consistente.

from django.core.mail.message import EmailMessage
# Importa a classe `EmailMessage`, responsável por criar e enviar mensagens de e-mail.
# Com ela, conseguimos definir remetente, destinatários, assunto, corpo do e-mail
# e até cabeçalhos personalizados.

# ==============================
# DEFINIÇÃO DO FORMULÁRIO
# ==============================
class ContactForm(forms.Form):
    # Define um formulário chamado `ContactForm` que herda de `forms.Form`.
    # Isso significa que estamos criando um formulário manualmente, sem vínculo
    # direto com modelos do banco de dados (ModelForm seria esse caso).
    # Ele será usado para coletar informações enviadas pelo usuário em uma página de contato.

    nome = forms.CharField(label="Nome", max_length=100)
    # Campo de texto simples (`CharField`) para armazenar o nome do usuário.
    # `label="Nome"` define o rótulo exibido no formulário.
    # `max_length=100` limita o tamanho da string para evitar dados muito grandes.

    email = forms.EmailField(label="E-mail", max_length=100)
    # Campo de e-mail (`EmailField`) que automaticamente valida se o valor
    # fornecido segue o formato de um endereço de e-mail.
    # `max_length=100` impede textos muito longos.

    assunto = forms.CharField(label="Assunto", max_length=200)
    # Campo de texto (`CharField`) que representa o assunto da mensagem.
    # `max_length=200` define o tamanho máximo permitido.

    mensagem = forms.CharField(label="Mensagem", widget=forms.Textarea)
    # Campo de texto (`CharField`) que utiliza um widget especial: `Textarea`.
    # Diferente de um campo de entrada de linha única, `Textarea` gera
    # uma caixa de múltiplas linhas para que o usuário escreva sua mensagem.
    # Ideal para textos longos.

    # ==============================
    # METODO PERSONALIZADO PARA ENVIO DE E-MAIL
    # ==============================
    def send_email(self):
        # Define um metodo da classe `ContactForm` para enviar um e-mail
        # com os dados preenchidos no formulário. Só deve ser chamado após
        # validar o formulário com `is_valid()`.

        nome = self.cleaned_data['nome']
        # Recupera o valor do campo `nome` já validado pelo formulário.
        # `cleaned_data` é um dicionário que só existe após a validação.

        email = self.cleaned_data['email']
        # Recupera o valor do campo `email` validado.
        # Garantido que é um e-mail válido (graças ao `EmailField`).

        assunto = self.cleaned_data['assunto']
        # Recupera o assunto informado pelo usuário.

        mensagem = self.cleaned_data['mensagem']
        # Recupera a mensagem de texto enviada.

        conteudo = f"Nome: {nome}\nE-mail: {email}\nAssunto: {assunto}\nMensagem: {mensagem}"
        # Monta o corpo do e-mail que será enviado.
        # Aqui usamos uma f-string para formatar e incluir todos os dados
        # do formulário em um texto organizado.

        mail = EmailMessage(
            subject=assunto,
            # Define o assunto do e-mail como sendo o mesmo preenchido pelo usuário.

            body=conteudo,
            # Define o corpo da mensagem como o texto montado acima.

            from_email="contato@fusion.com.br",
            # Define o remetente do e-mail. Deve ser um e-mail configurado
            # no servidor SMTP do projeto.

            to=["contato@fusion.com.br"],
            # Lista de destinatários do e-mail. Pode conter um ou mais endereços.
            # Aqui, estamos enviando para o mesmo e-mail de contato.

            headers={"Reply-To": "contato@fusion.com.br"}
            # Define cabeçalhos adicionais. `Reply-To` indica para onde
            # as respostas devem ser direcionadas, útil quando queremos
            # centralizar todas as respostas em um endereço específico.
        )

        mail.send()
        # Envia o e-mail de fato. Esse metodo faz a integração com o backend de envio
        # configurado no settings.py (como SMTP, console backend etc.).
