# ======================================================================
# IMPORTAÇÕES NECESSÁRIAS
# ======================================================================

# Importa a classe genérica `FormView`, fornecida pelo Django.
# - Essa classe é uma *Class-Based View (CBV)* já pronta para lidar com formulários.
# - Em vez de escrever manualmente toda a lógica de exibir, validar e processar formulários,
#   herdamos de `FormView` e só sobrescrevemos os métodos que queremos personalizar.
from django.views.generic import FormView

# Importa a função `reverse_lazy`, que gera dinamicamente URLs a partir do nome da rota.
# - A diferença entre `reverse` e `reverse_lazy`:
#   * `reverse` resolve a URL imediatamente (quando o módulo é carregado).
#   * `reverse_lazy` só resolve a URL quando ela realmente for necessária.
# - Em *Class-Based Views* (como esta), usamos `reverse_lazy` para evitar erros
#   no carregamento, já que as rotas podem ainda não estar carregadas no momento da importação.
from django.urls import reverse_lazy

# Importa o sistema de mensagens do Django.
# - Esse sistema permite enviar mensagens de feedback para o usuário
#   (ex: "Formulário enviado com sucesso", "Ocorreu um erro", etc.).
# - As mensagens podem ser exibidas no HTML usando o template tag `{% if messages %}`.
from django.contrib import messages

# Importa os modelos `Servico` e `Equipe` definidos no arquivo `models.py` desta aplicação.
# - `Servico`: provavelmente armazena informações sobre os serviços oferecidos pela empresa/site.
# - `Equipe`: provavelmente armazena informações sobre os membros da equipe.
# - Esses dados serão enviados ao template para que sejam exibidos dinamicamente.
from .models import Servico, Equipe

# Importa o formulário de contato (`ContactForm`), definido em `forms.py`.
# - Esse formulário contém os campos necessários (nome, email, assunto, mensagem).
# - A view usará esse formulário para exibir os campos e validar os dados enviados pelo usuário.
from .forms import ContactForm

# ======================================================================
# DEFINIÇÃO DA VIEW PRINCIPAL
# ======================================================================

# Criamos a classe `IndexView`, que representa a view responsável pela página inicial do site.
# - Herdamos de `FormView` porque queremos exibir e processar um formulário.
# - Além disso, aproveitamos a estrutura da CBV para manter o código organizado e reutilizável.
class IndexView(FormView):

    # ------------------------------------------------------------------
    # Configurações básicas da view
    # ------------------------------------------------------------------

    # Define o template que será renderizado quando essa view for chamada.
    # - Aqui usamos o arquivo `index.html`, que ficará dentro da pasta `templates`.
    template_name = 'index.html'

    # Define qual formulário será exibido nesta view.
    # - Estamos dizendo que o formulário usado aqui é o `ContactForm`.
    form_class = ContactForm

    # Define para onde o usuário será redirecionado após o envio bem-sucedido do formulário.
    # - `reverse_lazy('index')` gera a URL da rota chamada "index" (definida no arquivo urls.py).
    # - Assim, após o envio do formulário, o usuário volta para a página inicial.
    success_url = reverse_lazy('index')

    # ------------------------------------------------------------------
    # Enviando dados extras para o template
    # ------------------------------------------------------------------

    # Sobrescrevemos o metodo `get_context_data`.
    # - Esse metodo é chamado pelo Django para preparar o "contexto" enviado ao template.
    # - O contexto é um dicionário onde as chaves são nomes de variáveis
    #   e os valores são os dados que estarão disponíveis no HTML.
    def get_context_data(self, **kwargs):
        # Primeiro chamamos a implementação da classe-pai (`FormView`) para obter o contexto padrão.
        # Esse contexto já contém, por exemplo, o objeto do formulário (`form`).
        context = super(IndexView, self).get_context_data(**kwargs)

        # Agora adicionamos dados personalizados ao contexto:

        # Consulta todos os serviços no banco de dados.
        # - `Servico.objects.all()` → retorna todos os registros da tabela `Servico`.
        # - `.order_by('?')` → embaralha a ordem dos resultados (retorna de forma aleatória).
        # - Isso é útil quando queremos mostrar serviços de maneira variada a cada acesso.
        context['servicos'] = Servico.objects.order_by('?').all()

        # Consulta todos os membros da equipe.
        # - Da mesma forma, usamos `.order_by('?')` para mostrar os membros em ordem aleatória.
        # - OBS: aqui a chave foi escrita como `'Equipe'` (com E maiúsculo).
        #   Isso significa que no template devemos acessar `Equipe` e não `equipe`.
        context['Equipe'] = Equipe.objects.order_by('?').all()

        # Retorna o dicionário atualizado com os novos dados incluídos.
        return context


    # ------------------------------------------------------------------
    # Tratamento de formulário válido
    # ------------------------------------------------------------------

    # Sobrescrevemos o metodo `form_valid`.
    # - Esse metodo é chamado automaticamente quando o usuário envia o formulário
    #   e todos os dados são validados corretamente.
    def form_valid(self, form, *args, **kwargs):
        # Primeiro, chamamos o metodo `send_email` do formulário.
        # - Esse metodo foi definido em `ContactForm` e é responsável por montar e enviar o email.
        form.send_email()

        # Adicionamos uma mensagem de sucesso ao sistema de mensagens do Django.
        # - Essa mensagem pode ser exibida no template para informar ao usuário
        #   que o envio foi realizado com sucesso.
        messages.success(self.request, 'Email enviado com sucesso!')

        # Chamamos a versão original (`super`) de `form_valid`, para manter o comportamento padrão:
        # - Redirecionar o usuário para `success_url`.
        return super(IndexView, self).form_valid(form, *args, **kwargs)

    # ------------------------------------------------------------------
    # Tratamento de formulário inválido
    # ------------------------------------------------------------------

    # Sobrescrevemos o metodo `form_invalid`.
    # - Esse metodo é chamado automaticamente quando o formulário enviado
    #   contém erros de validação (ex: email inválido, campos obrigatórios vazios, etc.).
    def form_invalid(self, form, *args, **kwargs):
        # Adicionamos uma mensagem de erro ao sistema de mensagens.
        # - Essa mensagem será exibida no template, avisando o usuário
        #   que houve um problema no envio.
        messages.error(self.request, 'Erro ao tentar enviar o email!')

        # Chamamos a versão original (`super`) de `form_invalid`, que:
        # - Reexibe o template do formulário (`index.html`).
        # - Inclui os erros de validação nos campos correspondentes.
        return super(IndexView, self).form_invalid(form, *args, **kwargs)


