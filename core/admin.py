from django.contrib import admin
# importa o pacote `admin` do Django (django.contrib.admin).
# - `django.contrib.admin` é o módulo que fornece a **interface administrativa** pronta do Django,
#   um painel web para criar/editar/excluir instâncias dos seus models sem você ter que construir formulários/rotas.
# - Nesse módulo existem objetos e utilitários importantes:
#     * `admin.site`  -> instância que representa o site admin em si (onde os models são registrados).
#     * `admin.register` -> um *decorator* conveniente para registrar modelos.
#     * `admin.ModelAdmin` -> classe base que você herda para customizar como um model aparece no admin.
# - Ao importar `admin` você terá acesso a essas ferramentas para expor seus modelos ao painel administrativo.

from .models import Cargo, Servico, Equipe
# importa localmente (do mesmo pacote) as classes de modelo `Cargo`, `Servico` e `Equipe` definidas em models.py.
# - O prefixo `.` significa "do mesmo pacote/module" (import relativo). Aqui supõe-se que este arquivo admin.py esteja
#   no mesmo diretório/packge que models.py (ex.: app `core`).
# - Cada um desses nomes (Cargo, Servico, Equipe) é uma **classe de model** (subclasse de django.db.models.Model).
#   Essas classes definem atributos/fields (CharField, BooleanField, ForeignKey, DateTimeField, ImageField, etc.),
#   comportamento do ORM (métodos, __str__, meta) e mapeamento para tabelas do banco de dados.
# - Importar os models é necessário para registrar cada um no admin e dizer ao Django como exibi-los/editar no painel.

@admin.register(Cargo)
# decorator que registra o model `Cargo` no site administrativo do Django.
# - Equivalente a: admin.site.register(Cargo, CargoAdmin) (quando a classe CargoAdmin já estiver definida).
# - Vantagem do decorator: código mais limpo e claro, fixa o registro imediatamente acima da classe de configuração.
# - Observação: o decorator deve preceder a definição da classe de admin que customiza o comportamento do model no painel.
class CargoAdmin(admin.ModelAdmin):
    # define uma classe de configuração para o admin relativa ao model Cargo.
    # - `admin.ModelAdmin` é a *classe base* que contém dezenas de pontos de extensão (métodos e atributos).
    # - Ao herdar `ModelAdmin`, você pode:
    #     • controlar quais campos aparecem na lista (list_display),
    #     • habilitar filtros laterais (list_filter),
    #     • adicionar busca por texto (search_fields),
    #     • customizar o formulário de edição (fieldsets, form, formfield_overrides),
    #     • controlar permissões, comportamentos de salvamento (save_model), etc.
    # - A classe em si não executa nada até ser instanciada pelo framework do admin; Django cria uma instância
    #   dessa classe por conta do decorator/registro e usa seus métodos para renderizar páginas do admin.
    list_display = ('cargo', 'ativo', 'modificado')
    # atributo de classe que informa quais colunas exibir na **change list** (a página que lista os objetos do model).
    # - É uma tupla de *strings* (nomes de atributos) ou callables:
    #     'cargo'       -> normalmente o nome do campo (ex.: CharField) definido no model; será exibido tal como __str__ do valor.
    #     'ativo'       -> tipicamente um BooleanField; o admin renderiza um ícone de check/cross.
    #     'modificado'  -> tipicamente um DateTimeField (ex.: auto_now=True) indicando quando o registro foi alterado.
    # - Regras e detalhes:
    #     • Cada string pode ser:
    #         - o nome de um field do model,
    #         - o nome de um metodo definido no model que retorna algo a ser exibido,
    #         - o nome de um metodo definido no próprio `ModelAdmin` (se declarado como def nome(self, obj): ...).
    #     • Se você usar um metodo, pode personalizar `short_description` (texto da coluna) e `admin_order_field`
    #       (permite ordenar pela coluna).
    #     • Evite operações muito custosas aqui — a `change list` é executada para muitos objetos; operações caras causam lentidão.
    #     • Para evitar consultas N+1, se a coluna acessa relações ForeignKey, use `list_select_related` (explicado nos comentários).
    #
    # Exemplo de extensões (não aplicadas aqui, apenas ilustração):
    #   - list_filter = ('ativo',)           # mostraria um filtro lateral para campos booleanos/choices/dates
    #   - search_fields = ('cargo',)         # adiciona barra de busca que pesquisa nos campos listados
    #   - list_select_related = ('outra_fk',)  # evita N+1 quando a list_display acessa relações FK

@admin.register(Servico)
# registra o model `Servico` no admin usando o decorator; funciona igual ao caso anterior.
class ServicoAdmin(admin.ModelAdmin):
    # classe que configura a forma como `Servico` aparece no painel administrativo.
    # - você pode sobrescrever métodos como save_model(self, request, obj, form, change) para interceptar salvamentos,
    #   ou get_queryset(self, request) para alterar os objetos retornados (ex.: adicionar .select_related()).
    list_display = ('servico', 'icone', 'ativo', 'modificado')
    # define as colunas exibidas para o model Servico.
    # - 'servico'  : normalmente um CharField com o nome/título do serviço.
    # - 'icone'    : pode ser um campo que guarda um nome de ícone, uma imagem ou um método que retorna HTML.
    #                • Se for HTML (por exemplo, um <img> inline), para exibí-lo adequadamente você teria que marcar como seguro
    #                  (usar django.utils.safestring.mark_safe) e declarar short_description, e provavelmente marcar como readonly_fields
    #                  no formulário de edição se não for um campo editável simples.
    # - 'ativo'    : booleano que informa se o serviço está ativo/visível no site.
    # - 'modificado': data/hora da última alteração. Como em CargoAdmin, atente para performance ao buscar/formatar datas.
    # Observações de boas práticas:
    # - Se 'icone' for um campo que faz query a outro model, pense em `prefetch_related`/`select_related` no get_queryset para otimizar.
    # - Você pode adicionar `ordering = ('servico',)` para definir ordenação padrão da change list.

@admin.register(Equipe)
# registra o model `Equipe` no admin.
class EquipeAdmin(admin.ModelAdmin):
    # classe que customiza a interface do model Equipe no admin.
    # - Equipe costuma representar pessoas/colaboradores; geralmente possui campos como nome, cargo (ForeignKey), imagem, bio, ativo, etc.
    # - Aqui você pode querer adicionar recursos típicos de admin para esse tipo de model: search_fields por nome, list_filter por cargo, inlines para relações etc.
    list_display = ('nome', 'cargo', 'ativo', 'modificado')
    # define as colunas a exibir na lista de Equipe:
    # - 'nome'   : texto representando a pessoa (CharField).
    # - 'cargo'  : provavelmente é um ForeignKey para o model Cargo; o Django exibirá o __str__() do objeto relacionado por padrão.
    #             • Para evitar N+1 queries ao exibir várias linhas, recomenda-se:
    #                 list_select_related = ('cargo',)
    #               que fará o ORM trazer os cargos via JOIN em uma única query.
    # - 'ativo'  : booleano indicando se o membro está ativo no site.
    # - 'modificado' : timestamp de alteração; pode ser útil para ordenação/visualização rápida.
    #
    # Sugestões práticas que você pode adicionar conforme necessidade (exemplos; não aplicados automaticamente):
    #   - search_fields = ('nome', 'cargo__cargo')    # permite busca por nome da pessoa e por nome do cargo (através da relação FK).
    #   - list_filter = ('ativo', 'cargo')            # adiciona filtros laterais por cargo e ativo.
    #   - list_select_related = ('cargo',)            # melhora performance evitando queries extras por linha.
    #   - readonly_fields = ('modificado',)           # marca campos somente-leitura no formulário de edição.
    #   - prepopulated_fields = {'slug': ('nome',)}   # exemplo para preencher automaticamente um slug a partir do nome.
    #
    # Observação final:
    # - Cada uma das tuplas em list_display deve referenciar algo que o Django saiba extrair de cada instância de model:
    #     - atributo do model (campo),
    #     - metodo do model (def meu_metodo(self): return ...),
    #     - metodo do ModelAdmin (def meu_metodo(self, obj): return ...),
    #     - ou uma propriedade/descriptor do objeto.
    # - Se você usar métodos, pode definir `meu_metodo.admin_order_field = 'campo_de_ordenacao'` para permitir ordenar por essa coluna,
    #   e `meu_metodo.short_description = 'Nome da Coluna'` para personalizar o título da coluna no admin.





