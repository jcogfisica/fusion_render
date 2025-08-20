from django import forms
# Importa o módulo `forms` do Django.
# Este módulo fornece classes e ferramentas para criar formulários HTML de maneira declarativa.
# Um formulário no Django não é apenas HTML estático: ele também inclui validação de dados,
# conversão de tipos, integração com modelos e geração automática de widgets (inputs, selects, etc.).
# Aqui estamos importando o pacote inteiro, pois vamos herdar da classe `forms.Form`.

from django.core.mail.message import EmailMessage
# Importa a classe `EmailMessage` do submódulo `django.core.mail.message`.
# Essa classe representa um objeto de e-mail completo no Django.
# Com ela podemos configurar assunto, corpo, remetente, destinatários e cabeçalhos,
# e depois enviá-lo através do backend de e-mail definido no `settings.py` (SMTP, console, file, etc.).

# ==============================
# DEFINIÇÃO DO FORMULÁRIO
# ==============================
class ContactForm(forms.Form):
    # Define a classe `ContactForm`, que herda de `forms.Form`.
    # `forms.Form` é uma classe base para criação de formulários que não estão diretamente
    # ligados a modelos do banco de dados (diferente de `forms.ModelForm`, que é integrado ao ORM).
    # Esta classe representa a estrutura e a lógica de validação de um formulário de contato,
    # normalmente usado em páginas "Fale Conosco".

    nome = forms.CharField(label="Nome", max_length=100)
    # Define um campo de formulário chamado `nome`.
    # `forms.CharField` cria um campo de texto simples (input type="text").
    # O parâmetro `label` define o texto que aparecerá como rótulo no formulário renderizado.
    # O `max_length=100` define a restrição de tamanho máximo para o valor desse campo,
    # e também influencia a validação: se o usuário digitar mais que 100 caracteres, o formulário será inválido.

    email = forms.EmailField(label="E-mail", max_length=100)
    # Define um campo de formulário chamado `email`.
    # `forms.EmailField` é uma subclasse de `CharField` que adiciona validação extra:
    # verifica se o valor informado segue o formato padrão de endereço de e-mail.
    # Assim, o Django garante que o valor armazenado seja um e-mail válido.
    # O `max_length=100` limita o tamanho do valor, assim como no campo `nome`.

    assunto = forms.CharField(label="Assunto", max_length=200)
    # Define um campo chamado `assunto`.
    # Também é um `CharField`, mas aqui permitimos até 200 caracteres.
    # Representa o assunto do e-mail que será enviado.
    # Esse campo não tem validações específicas além do tamanho máximo.

    mensagem = forms.CharField(label="Mensagem", widget=forms.Textarea)
    # Define um campo chamado `mensagem`.
    # É um `CharField`, mas aqui passamos um parâmetro especial: `widget=forms.Textarea`.
    # Widgets controlam como o campo será renderizado em HTML. O `Textarea` gera um
    # elemento `<textarea>` (múltiplas linhas de texto), adequado para mensagens longas.
    # O `label="Mensagem"` será exibido junto ao campo no HTML.

    # ==============================
    # METODO PERSONALIZADO PARA ENVIO DE E-MAIL
    # ==============================
    def send_email(self):
        # Define um metodo de instância chamado `send_email`, pertencente ao formulário `ContactForm`.
        # Este metodo encapsula a lógica para enviar os dados preenchidos via e-mail.
        # Importante: esse metodo só deve ser chamado após validar o formulário com `is_valid()`.
        # Isso porque ele depende de `self.cleaned_data`, que só existe se o formulário for válido.

        nome = self.cleaned_data['nome']
        # Acessa o valor do campo `nome` a partir do dicionário `cleaned_data`.
        # `cleaned_data` é criado internamente pelo Django quando `form.is_valid()` é chamado.
        # Ele contém os dados já convertidos e validados.
        # Aqui, `nome` já é garantidamente uma string com até 100 caracteres.

        email = self.cleaned_data['email']
        # Acessa o valor validado do campo `email`.
        # Neste ponto, já foi verificado se é um e-mail válido.
        # O valor armazenado é uma string no formato de endereço eletrônico.

        assunto = self.cleaned_data['assunto']
        # Acessa o valor do campo `assunto` validado.
        # Representa a linha de assunto do e-mail que será enviado.

        mensagem = self.cleaned_data['mensagem']
        # Acessa o valor do campo `mensagem` validado.
        # Será usado como corpo do e-mail, junto com os outros dados.

        conteudo = f"Nome: {nome}\nE-mail: {email}\nAssunto: {assunto}\nMensagem: {mensagem}"
        # Cria uma string formatada (f-string) contendo todos os dados do formulário.
        # Essa string será o corpo principal do e-mail.
        # Inclui quebras de linha `\n` para organizar as informações em linhas separadas.

        mail = EmailMessage(
            subject=assunto,
            # Define o campo "assunto" do e-mail como o mesmo informado pelo usuário.

            body=conteudo,
            # Define o corpo (texto) do e-mail como a string criada acima.
            # O parâmetro `body` pode ser texto simples ou HTML, mas aqui usamos texto simples.

            from_email="contato@fusion.com.br",
            # Define o remetente do e-mail (campo "From:").
            # Este endereço deve ser configurado no backend de e-mail do Django (ex.: SMTP).
            # Se não for válido ou não estiver autorizado no servidor, o envio pode falhar.

            to=["contato@fusion.com.br"],
            # Define a lista de destinatários do e-mail (campo "To:").
            # Aqui passamos uma lista contendo apenas um endereço, mas poderia haver vários.

            headers={"Reply-To": "contato@fusion.com.br"}
            # Define cabeçalhos extras do e-mail.
            # O `Reply-To` indica o endereço para onde as respostas devem ser enviadas.
            # É útil para diferenciar o endereço do remetente e o endereço que recebe respostas.
        )
        # A variável `mail` agora contém um objeto `EmailMessage` pronto para ser enviado.

        mail.send()
        # Chama o metodo `send()` do objeto `EmailMessage`.
        # Este metodo interage com o backend de envio de e-mail configurado no Django (`EMAIL_BACKEND`).
        # Pode ser SMTP (para envio real), console (apenas exibe no terminal) ou file (salva em arquivos).
        # Se for SMTP, aqui é estabelecida a conexão com o servidor, e a mensagem é transmitida.

