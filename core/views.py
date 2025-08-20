# ======================================================================
# VIEWS LINHA A LINHA – EXPLICAÇÃO DETALHADA
# ======================================================================

from django.views.generic import FormView
# Importa a classe FormView do módulo django.views.generic
# - "django.views.generic" contém "Class-Based Views" (CBVs) já prontas para usos comuns.
# - A classe FormView é uma view genérica projetada para lidar com formulários HTML.
# - Ela automatiza:
#   * exibição do formulário (GET),
#   * validação do envio (POST),
#   * tratamento de sucesso (redirect),
#   * tratamento de erro (reexibição do form com mensagens).
# - Evita repetição de código, já que substitui a necessidade de criar várias funções manuais.

from django.urls import reverse_lazy
# Importa a função reverse_lazy do módulo django.urls
# - reverse_lazy gera uma URL a partir do "nome da rota" definido em urls.py.
# - É chamada "lazy" porque só resolve a URL no momento em que for usada,
#   e não imediatamente no carregamento do módulo.
# - Em CBVs usamos reverse_lazy porque o arquivo views.py é carregado antes de urls.py,
#   e isso evita erro de importação circular.

from django.contrib import messages
# Importa o framework de mensagens do Django.
# - Permite registrar mensagens temporárias (sucesso, erro, aviso, info).
# - Essas mensagens ficam associadas à sessão ou ao request.
# - No template, podem ser acessadas com a tag {% if messages %}.
# - São úteis para dar feedback ao usuário sem ter que manipular HTML manualmente.

from .models import Servico, Equipe
# Importa os modelos Servico e Equipe definidos no mesmo app.
# - Servico: provavelmente representa os serviços oferecidos pela aplicação/site.
# - Equipe: representa os membros da equipe, com informações como nome, função, foto, redes sociais.
# - Esses modelos são classes Python que herdam de django.db.models.Model.
# - Por herdar de Model, eles possuem acesso ao ORM do Django (ex: objects.all(), objects.filter()).

from .forms import ContactForm
# Importa a classe ContactForm definida em forms.py do mesmo app.
# - ContactForm é um formulário Django (herda de forms.Form ou forms.ModelForm).
# - Ele define os campos do formulário de contato (nome, email, assunto, mensagem, etc.).
# - Também deve conter um metodo send_email(), usado para enviar os dados por email.
# - O Django cria automaticamente widgets HTML a partir desse form.

# ======================================================================
# Definição da View IndexView
# ======================================================================

class IndexView(FormView):
    """
    Classe que representa a página inicial do site.
    - Herda de FormView, portanto já possui comportamento padrão para lidar com formulários.
    - Ciclo de vida:
        * GET request → exibe o formulário vazio (chama get_context_data).
        * POST request válido → executa form_valid().
        * POST request inválido → executa form_invalid().
    - Além do formulário, essa view também adiciona dados extras (serviços e equipe) ao contexto.
    """

    template_name = 'index.html'
    # Nome do template HTML que será renderizado.
    # - Django procura este arquivo na pasta "templates" configurada no settings.py.
    # - O metodo render_to_response() da CBV usará esse template.
    # - Aqui será exibido tanto o formulário quanto os dados adicionais do contexto.

    form_class = ContactForm
    # Define qual formulário Django será utilizado nesta view.
    # - O FormView vai instanciar automaticamente ContactForm e disponibilizar no contexto como 'form'.
    # - GET: cria form vazio.
    # - POST: cria form preenchido com request.POST e valida os dados.

    success_url = reverse_lazy('index')
    # Define para onde o usuário será redirecionado após envio válido do formulário.
    # - Usa reverse_lazy para resolver o nome da rota 'index' definido em urls.py.
    # - O FormView chamará HttpResponseRedirect para essa URL depois de form_valid().

    def get_context_data(self, **kwargs):
        """
        Retorna o dicionário de contexto usado para renderizar o template.
        - Aqui adicionamos dados extras além do formulário padrão.
        - Inclui:
            * Lista de serviços disponíveis (ordem aleatória).
            * Lista de membros da equipe (ordem aleatória).
        """
        context = super().get_context_data(**kwargs)
        # Chama o metodo get_context_data da superclasse (FormView → TemplateResponseMixin).
        # - Esse metodo cria o contexto inicial.
        # - Ele já inclui o formulário em 'form', pronto para ser usado no template.
        # - O uso de super() chama a implementação herdada, mantendo o comportamento padrão.

        context['servicos'] = Servico.objects.order_by('?').all()
        # Adiciona ao contexto todos os registros do modelo Servico.
        # - Servico.objects é o "manager" padrão do ORM, que gera consultas SQL.
        # - order_by('?') embaralha a ordem dos resultados (aleatório).
        # - all() retorna um QuerySet com todos os serviços.
        # - O template pode iterar sobre context['servicos'] para exibir cada serviço.

        context['Equipe'] = Equipe.objects.order_by('?').all()
        # Adiciona todos os registros do modelo Equipe ao contexto.
        # - Semelhante aos serviços, mas para a equipe.
        # - Também em ordem aleatória.
        # - Observação: a chave é 'Equipe' com "E" maiúsculo, então no template deve-se usar {{ Equipe }}.

        return context
        # Retorna o dicionário de contexto atualizado.
        # - Esse dicionário será passado para o template index.html.
        # - O template terá acesso a 'form', 'servicos' e 'Equipe'.

    def form_valid(self, form, *args, **kwargs):
        """
        Executado quando o formulário enviado é válido.
        - 'form' já contém os dados validados.
        - Fluxo:
            1. Chama form.send_email() → envia email com os dados.
            2. Cria mensagem de sucesso (feedback ao usuário).
            3. Redireciona automaticamente para success_url.
        """
        form.send_email()
        # Chama o metodo definido em ContactForm.
        # - Responsável por montar o conteúdo do email.
        # - Pode usar send_mail() do Django ou outra biblioteca SMTP.
        # - Só é chamado se todos os campos forem válidos.

        messages.success(self.request, 'Email enviado com sucesso!')
        # Cria uma mensagem de sucesso associada ao request atual.
        # - 'self.request' é o objeto HttpRequest processado pela view.
        # - Essa mensagem será exibida no template (se configurado).
        # - 'success' adiciona mensagem com nível de sucesso (cor verde na maioria dos templates).

        return super().form_valid(form, *args, **kwargs)
        # Chama a implementação padrão de form_valid.
        # - Essa implementação retorna um HttpResponseRedirect para success_url.
        # - Garante que o comportamento esperado de FormView seja mantido.

    def form_invalid(self, form, *args, **kwargs):
        """
        Executado quando o formulário contém erros de validação.
        - 'form' aqui já está preenchido com os dados inválidos e com erros.
        - Fluxo:
            1. Adiciona mensagem de erro para o usuário.
            2. Reexibe o formulário no template, com erros destacados.
        """
        messages.error(self.request, 'Erro ao tentar enviar o email!')
        # Cria uma mensagem de erro associada ao request.
        # - Essa mensagem aparecerá no template como feedback negativo.
        # - O nível "error" geralmente aparece em vermelho.

        return super().form_invalid(form, *args, **kwargs)
        # Chama a implementação padrão de form_invalid.
        # - Essa implementação renderiza novamente o template definido em template_name.
        # - Inclui o objeto 'form' com os erros no contexto.
        # - Assim, o usuário vê os campos preenchidos e as mensagens de erro.
