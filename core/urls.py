# Importa a função `path` da biblioteca `django.urls`.
# Essa função é usada para definir os mapeamentos de URL (rotas) da aplicação para as views correspondentes.
# Estrutura: path(route, view, kwargs=None, name=None)
# - route → string que representa o padrão da URL.
# - view → a função ou classe que será chamada quando a URL for acessada.
# - kwargs → argumentos adicionais opcionais.
# - name → apelido da rota, útil para referenciar a URL nos templates ou no código.
from django.urls import path

# Importa a classe `IndexView` definida no arquivo `views.py` desta mesma aplicação.
# Essa classe representa a view que será executada quando o usuário acessar a rota configurada.
# Como ela é uma class-based view, precisará ser convertida em função com `.as_view()`.
from .views import IndexView

# Cria a lista `urlpatterns`, que contém todas as rotas (URLs) mapeadas para esta aplicação Django.
# O Django procura essa lista quando precisa decidir qual view deve atender a uma requisição.
urlpatterns = [
    # Define a rota raiz da aplicação:
    # - A string vazia ('') significa que a rota corresponde à URL base do site ou da aplicação.
    # - `IndexView.as_view()` converte a classe `IndexView` em uma função de view compatível com o Django.
    #   Isso é necessário porque o Django espera sempre uma função de view, mesmo que usemos uma class-based view.
    # - `name='index'` dá um nome para essa rota. Esse nome pode ser usado em:
    #   → templates (ex: {% url 'index' %})
    #   → código Python (ex: reverse('index'))
    #   Isso facilita a manutenção, pois não precisamos alterar todas as referências caso a URL mude no futuro.
    path('', IndexView.as_view(), name='index'),
]
