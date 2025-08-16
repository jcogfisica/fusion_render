import os, uuid  # Importa dois módulos da biblioteca padrão do Python:
                 # - os: fornece funções para interagir com o sistema operacional.
                 # - uuid: permite gerar identificadores únicos universais (UUIDs), usados aqui para nomear arquivos de forma única.

from django.db import models  # Importa o módulo de models do Django, usado para definir classes que representam tabelas no banco de dados.
from pictures.models import PictureField  # Importa um campo especial para armazenar imagens, com funcionalidades adicionais em relação ao ImageField padrão.
from django.conf import settings  # Importa as configurações do projeto Django, permitindo acesso a variáveis como MEDIA_URL.

# Função auxiliar para gerar caminhos de arquivos únicos ao salvar imagens ou uploads.
def get_file_path(_instance, filename):
    ext = filename.split('.')[-1]  # Extrai a extensão do arquivo (parte após o último ponto). Exemplo: "foto.png" → "png".
    filename = f'{uuid.uuid4()}.{ext}'  # Gera um novo nome de arquivo baseado em um UUID aleatório + a extensão original.
    return filename  # Retorna o novo nome do arquivo, que será usado pelo Django para salvar o upload.

# Classe base abstrata usada como "modelo genérico" para outros modelos.
# Isso evita duplicação de código, pois todos os modelos que herdarem desta classe terão os mesmos campos.
class Base(models.Model):
    criado = models.DateTimeField('Data de criação', auto_now_add=True)
    # Campo de data/hora preenchido automaticamente quando o objeto é criado.
    # auto_now_add=True → o valor é definido apenas uma vez, no momento da criação.

    modificado = models.DateTimeField('Data de modificação', auto_now=True)
    # Campo de data/hora atualizado automaticamente toda vez que o objeto for salvo.
    # auto_now=True → útil para registrar a última modificação.

    ativo = models.BooleanField('Ativo?', default=True)
    # Campo booleano que indica se o registro está ativo ou não.
    # Útil como “flag de exclusão lógica”: em vez de deletar, apenas marca como inativo.

    class Meta:
        abstract = True
        # Define que esta classe é abstrata. Isso significa que ela NÃO gera tabela própria no banco de dados.
        # Outras classes herdarão seus campos, evitando repetição.

# Modelo que representa um "Serviço" oferecido, herdando os campos padrão de Base.
class Servico(Base):
    choices = (  # Define um conjunto de opções possíveis para o campo 'icone'.
        ("lni-cog", "Engrenagem"),
        ("lni-stats-up", "Gráfico"),
        ("lni-users", "Usuários"),
        ("lni-layers", "Design"),
        ("lni-mobile", "Mobile"),
        ("lni-rocket", "Foguete")
    )

    servico = models.CharField('Serviço', max_length=100)
    # Campo de texto curto para armazenar o nome do serviço. Limite de 100 caracteres.

    descricao = models.TextField('Descrição', blank=True, max_length=200)
    # Campo de texto longo para armazenar uma descrição do serviço.
    # blank=True → pode ser deixado vazio.
    # max_length=200 → recomendado para validação, mesmo em campos TextField.

    icone = models.CharField('Ícone', max_length=12, choices=choices)
    # Campo de texto para armazenar o código do ícone.
    # choices=choices → restringe os valores possíveis às opções definidas em "choices".

    class Meta:
        verbose_name = 'Serviço'  # Nome amigável para o modelo no admin do Django.
        verbose_name_plural = 'Serviços'  # Nome no plural para exibição no admin.

    def __str__(self):
        return self.servico  # Quando o objeto for convertido para string (ex.: no admin), mostra o nome do serviço.

# Modelo que representa um "Cargo" dentro da equipe.
class Cargo(Base):
    cargo = models.CharField('Cargo', max_length=100)
    # Campo de texto curto para armazenar o nome do cargo (ex.: "Designer", "Desenvolvedor").

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    def __str__(self):
        return self.cargo  # Exibe o nome do cargo quando o objeto for convertido em string.

# Modelo que representa uma pessoa da equipe.
class Equipe(Base):
    nome = models.CharField('Nome', max_length=100)
    # Nome da pessoa na equipe.

    cargo = models.ForeignKey(
        'core.Cargo',  # Relaciona a pessoa com um Cargo específico.
        verbose_name='Cargo',  # Nome amigável exibido no admin.
        max_length=100,  # (Não tem efeito prático em ForeignKey, mas não causa erro.)
        on_delete=models.CASCADE  # Se o Cargo for deletado, a pessoa também será apagada.
    )

    bio = models.TextField('Bio', blank=True, max_length=200)
    # Campo de texto longo para uma pequena biografia ou descrição da pessoa.

    imagem = PictureField(
        upload_to=get_file_path,  # Usa a função get_file_path para definir o nome e caminho do arquivo.
        width_field="image_width",  # Campo relacionado que guarda a largura real da imagem.
        height_field="image_height",  # Campo relacionado que guarda a altura real da imagem.
        aspect_ratios=[None, "1/1"],  # Define proporções permitidas para o corte da imagem.
        breakpoints={},  # Configurações de redimensionamento adicionais (aqui está vazio).
        file_types=["PNG"],  # Apenas imagens PNG serão aceitas.
        grid_columns=1,  # Configuração de exibição em grade.
        container_width=480,  # Largura máxima do container onde a imagem será exibida.
        pixel_densities=[1],  # Suporte apenas para densidade padrão de pixels (sem versões retina).
    )

    image_width = models.PositiveIntegerField(null=True, blank=True)
    # Guarda a largura da imagem enviada. Pode ser nulo ou deixado em branco.

    image_height = models.PositiveIntegerField(null=True, blank=True)
    # Guarda a altura da imagem enviada. Também pode ser nulo ou em branco.

    facebook = models.CharField('Facebook', max_length=100, default='#')
    # Link para o perfil do Facebook. Valor padrão é "#" (nenhum link válido).

    twitter = models.CharField('X', max_length=100, default='#')
    # Link para o perfil do Twitter (X). Padrão "#".

    instagram = models.CharField('Instagram', max_length=100, default='#')
    # Link para o perfil do Instagram. Padrão "#".

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'

    # Metodo que gera dinamicamente a URL da imagem com base nas configurações do projeto.
    def imagem_480_url(self):
        caminho_fisico = self.imagem.path  # Caminho físico completo da imagem no sistema de arquivos.
        lista = caminho_fisico.split('\\')  # Divide o caminho em partes, usando "\" como separador (Windows).
        dir_img = lista[len(lista) - 1].split('.')[0]  # Pega o nome do arquivo sem a extensão.
        ext = lista[len(lista) - 1].split('.')[-1]  # Pega a extensão do arquivo.
        container_width = self._meta.get_field('imagem').container_width
        # Obtém a largura do container definida no campo "imagem".
        url = f"{settings.MEDIA_URL.rstrip('/')}/{dir_img}/" + str(container_width) + "w." + ext
        # Monta a URL final baseada no MEDIA_URL do Django e nas informações da imagem.
        return url  # Retorna a URL construída.

    def __str__(self):
        return self.nome  # Exibe o nome da pessoa quando o objeto for convertido em string.


