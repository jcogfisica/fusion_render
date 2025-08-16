# ======================================================================
# VIEWS LINHA A LINHA – EXPLICAÇÃO DETALHADA
# ======================================================================

# Importa a classe FormView do Django
# - FormView é uma "Class-Based View" (CBV) projetada para lidar com formulários.
# - Ela já possui métodos prontos para exibir o formulário, validar os dados enviados
#   e redirecionar o usuário após o envio.
# - Usar CBVs permite menos repetição de código e maior organização.
from django.views.generic import FormView

# Importa reverse_lazy, que permite gerar URLs a partir de nomes de rotas
# - 'reverse_lazy' é a versão "preguiçosa" de reverse, ou seja, só resolve a URL quando realmente necessário.
# - Em CBVs, usamos reverse_lazy em vez de reverse para evitar problemas de importação circular,
#   porque a view pode ser carregada antes que as URLs estejam totalmente definidas.
from django.urls import reverse_lazy

# Importa o sistema de mensagens do Django
# - Permite adicionar mensagens temporárias para feedback ao usuário
#   (ex: "Email enviado com sucesso", "Erro ao enviar formulário", etc.)
# - As mensagens ficam armazenadas na sessão e podem ser exibidas no template
#   usando a template tag {% if messages %}.
from django.contrib import messages

# Importa os modelos usados nesta view
# - Servico: provavelmente armazena os serviços oferecidos pela empresa
# - Equipe: armazena membros da equipe e suas informações (nome, cargo, imagem, redes sociais)
from .models import Servico, Equipe

# Importa o formulário de contato definido em forms.py
# - ContactForm contém campos do formulário (ex: nome, email, assunto, mensagem)
# - Também deve ter um metodo send_email() para enviar emails ao administrador ou destinatário definido
from .forms import ContactForm

# ======================================================================
# Definição da View IndexView
# ======================================================================
class IndexView(FormView):
    """
    Representa a página inicial do site, que contém um formulário de contato.
    - Herdando de FormView, a view já lida automaticamente com GET e POST.
    - GET: exibe o formulário vazio.
    - POST: processa os dados enviados pelo usuário.
    """

    # ------------------------------------------------------------------
    # Template usado para renderizar esta view
    # ------------------------------------------------------------------
    template_name = 'index.html'
    # - Nome do arquivo HTML dentro da pasta templates.
    # - Django procura por 'templates/index.html' ou nas pastas definidas em TEMPLATES['DIRS'].

    # ------------------------------------------------------------------
    # Formulário que será exibido e processado
    # ------------------------------------------------------------------
    form_class = ContactForm
    # - Indica qual classe de formulário será usada.
    # - FormView cria automaticamente o objeto do formulário e adiciona ao contexto como 'form'.

    # ------------------------------------------------------------------
    # URL para redirecionamento após envio bem-sucedido
    # ------------------------------------------------------------------
    success_url = reverse_lazy('index')
    # - Quando o formulário é enviado corretamente, o usuário será redirecionado para esta URL.
    # - O nome 'index' deve estar definido em urls.py.
    # - reverse_lazy é usado aqui para evitar resolver a URL antes das rotas estarem carregadas.

    # ------------------------------------------------------------------
    # Metodo para enviar dados extras para o template
    # ------------------------------------------------------------------
    def get_context_data(self, **kwargs):
        """
        Adiciona informações adicionais ao contexto do template:
        - lista de serviços
        - lista de membros da equipe
        """
        # Chama o metodo da classe pai para obter o contexto padrão
        # - Inclui automaticamente o objeto 'form' que será renderizado no template
        context = super().get_context_data(**kwargs)

        # Adiciona todos os serviços disponíveis no contexto
        # - Servico.objects.all() retorna todos os registros da tabela Servico
        # - order_by('?') retorna os serviços em ordem aleatória a cada requisição
        context['servicos'] = Servico.objects.order_by('?').all()

        # Adiciona todos os membros da equipe ao contexto
        # - Semelhante aos serviços, a ordem é aleatória
        # - IMPORTANTE: no template devemos usar {{ Equipe }} com E maiúsculo, pois a chave do dicionário é 'Equipe'
        context['Equipe'] = Equipe.objects.order_by('?').all()

        # Retorna o dicionário de contexto atualizado
        return context

    # ------------------------------------------------------------------
    # Metodo chamado quando formulário enviado é válido
    # ------------------------------------------------------------------
    def form_valid(self, form, *args, **kwargs):
        """
        Executa quando todos os dados do formulário passam na validação:
        - Campos obrigatórios preenchidos
        - Dados com formato correto (ex: email válido)
        """
        # Chama o metodo send_email do formulário
        # - Responsável por montar e enviar o email para o destinatário definido no formulário
        form.send_email()

        # Adiciona uma mensagem de sucesso para o usuário
        # - Fica disponível para exibição no template usando {% if messages %}
        messages.success(self.request, 'Email enviado com sucesso!')

        # Chama o form_valid da classe pai
        # - Redireciona automaticamente para success_url
        # - Mantém o comportamento padrão do FormView
        return super().form_valid(form, *args, **kwargs)

    # ------------------------------------------------------------------
    # Metodo chamado quando formulário enviado é inválido
    # ------------------------------------------------------------------
    def form_invalid(self, form, *args, **kwargs):
        """
        Executa quando o formulário contém erros de validação:
        - Campos obrigatórios não preenchidos
        - Dados em formato incorreto
        """
        # Adiciona uma mensagem de erro para o usuário
        # - Fica disponível no template
        messages.error(self.request, 'Erro ao tentar enviar o email!')

        # Chama o form_invalid da classe pai
        # - Reexibe o template com o formulário
        # - Inclui os erros de validação nos campos correspondentes
        return super().form_invalid(form, *args, **kwargs)
