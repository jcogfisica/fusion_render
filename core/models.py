# ======================================================================
# MODELS COMENTADOS LINHA A LINHA (EXPLICAÇÃO EXTREMAMENTE DETALHADA)
# ======================================================================

# ----------------------------------------------------------------------
# Importações de bibliotecas padrão do Python
# ----------------------------------------------------------------------
import os
# 'os' é um módulo da biblioteca padrão do Python.
# Ele oferece funções para manipular o sistema operacional.
# Exemplos: criar/remover diretórios, trabalhar com caminhos de arquivos,
# acessar variáveis de ambiente, juntar paths de forma segura.
# Aqui, pode ser útil caso precisemos manipular nomes e diretórios de arquivos.

import uuid
# 'uuid' é outro módulo padrão do Python.
# Ele gera "Universally Unique Identifiers" (UUIDs).
# UUIDs são números grandes usados para identificar coisas de forma única
# em diferentes sistemas sem risco de colisão.
# Exemplo: '550e8400-e29b-41d4-a716-446655440000'.
# Aqui é usado para gerar nomes de arquivos únicos (evitando conflitos).

# ----------------------------------------------------------------------
# Importações específicas do Django
# ----------------------------------------------------------------------
from django.db import models
# 'django.db' é o módulo de banco de dados do Django.
# 'models' fornece classes e tipos de campos para criar modelos.
# Um "modelo" é uma classe Python que representa uma tabela no banco de dados.
# Cada atributo da classe equivale a uma coluna da tabela.

from django.conf import settings
# 'settings' permite acessar as configurações globais do projeto (settings.py).
# Exemplo: podemos pegar MEDIA_URL, MEDIA_ROOT, AUTH_USER_MODEL, etc.

from pictures.models import PictureField
# 'PictureField' é um campo customizado de outro app (pictures).
# Ele funciona como uma extensão do 'ImageField' do Django.
# Adiciona suporte a:
#   - diferentes proporções de imagem (aspect_ratios),
#   - múltiplas resoluções (breakpoints),
#   - formatos de arquivo específicos,
#   - metadados de largura/altura.
# Isso facilita trabalhar com imagens em aplicações responsivas.

# ----------------------------------------------------------------------
# Função auxiliar para gerar nomes de arquivos únicos
# ----------------------------------------------------------------------
def get_file_path(_instance, filename):
    """
    Essa função é chamada sempre que um arquivo (ex: imagem) é salvo.
    Ela recebe:
      - _instance: o objeto do modelo que contém o campo de arquivo.
      - filename: o nome original do arquivo enviado pelo usuário.
    Retorna:
      - Um nome de arquivo único baseado em UUID.
    Isso evita que arquivos com o mesmo nome sobrescrevam uns aos outros.
    """

    ext = filename.split('.')[-1]
    # 'filename.split('.')' divide o nome do arquivo em partes separadas por ponto.
    # Exemplo: 'foto.png' → ['foto', 'png'].
    # '[-1]' pega a última parte da lista, que é a extensão ('png').
    # Assim, preservamos o formato original.

    filename = f'{uuid.uuid4()}.{ext}'
    # 'uuid.uuid4()' gera um UUID aleatório.
    # Exemplo: '4f5d3c8a-2e12-4c6a-88b9-3d3bcd899cab'.
    # Depois concatenamos a extensão para manter o formato.
    # Exemplo: '4f5d3c8a-2e12-4c6a-88b9-3d3bcd899cab.png'.

    return filename
    # Retorna o novo nome do arquivo, que será usado pelo campo de imagem.

# ======================================================================
# CLASSE BASE (Modelo abstrato para herança)
# ======================================================================
class Base(models.Model):
    """
    Esta é uma classe abstrata, usada como "modelo base".
    - 'models.Model' é a superclasse que conecta o modelo ao ORM do Django.
    - Não cria tabela no banco (por causa do 'abstract = True' no Meta).
    - Serve para evitar repetição de código em outros modelos.
    Contém:
    - criado: Data de criação.
    - modificado: Data da última modificação.
    - ativo: Indica se o registro está ativo ou não.
    """

    criado = models.DateTimeField(
        'Data de criação',
        auto_now_add=True
    )
    # 'DateTimeField' cria uma coluna de data e hora.
    # 'auto_now_add=True' → preenche automaticamente com a data atual
    # no momento em que o objeto é criado (primeiro save()).

    modificado = models.DateTimeField(
        'Data de modificação',
        auto_now=True
    )
    # 'auto_now=True' → atualiza o campo para a data/hora atual
    # sempre que o objeto for salvo (update).

    ativo = models.BooleanField(
        'Ativo?',
        default=True
    )
    # 'BooleanField' cria um campo booleano (True/False).
    # 'default=True' significa que, por padrão, a totalidade dos objetos é ativa.

    class Meta:
        abstract = True
        # 'abstract = True' indica que essa classe não será transformada
        # em uma tabela no banco.
        # Apenas outras classes que herdarem dela criarão tabelas.

# ======================================================================
# MODELO CARGO
# ======================================================================
class Cargo(Base):
    """
    Representa um cargo na equipe (exemplo: Designer, Desenvolvedor).
    Herda de Base → já possui criado, modificado e ativo.
    """

    cargo = models.CharField(
        'Cargo',
        max_length=100
    )
    # 'CharField' → campo de texto de tamanho limitado.
    # 'max_length=100' → aceita até 100 caracteres.
    # 'verbose_name="Cargo"' → nome legível exibido no admin.

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        # Configura nomes amigáveis para exibição no Django Admin.

    def __str__(self):
        return self.cargo
        # '__str__' define a representação em string do objeto.
        # Isso é usado no Django Admin, QuerySets, etc.
        # Aqui retorna o nome do cargo (ex: "Designer").

# ======================================================================
# MODELO SERVIÇO
# ======================================================================
class Servico(Base):
    """
    Representa um serviço oferecido (ex: Desenvolvimento Web).
    """

    # Lista de opções pré-definidas para o campo 'icone'.
    choices = (
        ("lni-cog", "Engrenagem"),
        ("lni-stats-up", "Gráfico"),
        ("lni-users", "Usuários"),
        ("lni-layers", "Design"),
        ("lni-mobile", "Mobile"),
        ("lni-rocket", "Foguete")
    )

    servico = models.CharField(
        'Serviço',
        max_length=100
    )

    descricao = models.TextField(
        'Descrição',
        # blank=True,
        max_length=200
    )
    # 'TextField' é usado para textos longos.
    # 'blank=True' → o campo pode ficar vazio.
    # 'max_length=200' → não é restritivo no banco, mas pode ser usado
    # como validação em formulários/admin.

    icone = models.CharField(
        'Ícone',
        max_length=12,
        choices=choices
    )
    # 'choices' restringe os valores permitidos a um conjunto fixo.
    # No admin, será exibido um dropdown com as opções definidas.

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'

    def __str__(self):
        return self.servico

# ======================================================================
# MODELO EQUIPE
# ======================================================================
class Equipe(Base):
    """
    Representa um membro da equipe (pessoa).
    """

    nome = models.CharField(
        'Nome',
        max_length=100
    )

    cargo = models.ForeignKey(
        'core.Cargo',
        verbose_name='Cargo',
        on_delete=models.CASCADE
    )
    # 'ForeignKey' cria um relacionamento N:1 (muitos para um).
    # Cada membro da equipe tem 1 cargo.
    # 'on_delete=models.CASCADE' → se o cargo for deletado, os membros relacionados também são deletados.

    bio = models.TextField(
        'Bio',
        # blank=True,
        max_length=200
    )

    imagem = PictureField(
        upload_to=get_file_path,
        width_field="image_width",
        height_field="image_height",
        aspect_ratios=[None, "1/1"],
        breakpoints={},
        file_types=["PNG"],
        grid_columns=1,
        container_width=480,
        pixel_densities=[1],
    )
    # 'PictureField' é um campo especial para imagens responsivas.
    # - 'upload_to': usa a função get_file_path para gerar nomes únicos.
    # - 'width_field' e 'height_field': armazenam dimensões reais.
    # - 'aspect_ratios': define proporções permitidas (aqui qualquer proporção ou quadrado).
    # - 'breakpoints': versões diferentes para responsividade (aqui vazio).
    # - 'file_types': apenas PNG é aceito.
    # - 'grid_columns': usado no layout responsivo.
    # - 'container_width': largura máxima considerada.
    # - 'pixel_densities': define versões retina (1 = normal apenas).

    image_width = models.PositiveIntegerField(
        null=True,
        # blank=True
    )
    image_height = models.PositiveIntegerField(
        null=True,
        # blank=True
    )
    # Esses campos armazenam largura/altura reais da imagem.
    # São preenchidos automaticamente pelo PictureField.

    facebook = models.CharField('Facebook', max_length=100, default='#')
    twitter = models.CharField('X', max_length=100, default='#')
    instagram = models.CharField('Instagram', max_length=100, default='#')
    # Links para redes sociais do membro.
    # 'default="#"' → evita campo vazio (link neutro).

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'

    def imagem_480_url(self):
        """
        Retorna a URL pública da imagem principal.
        Se não houver imagem, retorna None.
        """
        if self.imagem:
            return self.imagem.url
        return None

    def __str__(self):
        return self.nome
        # Representação amigável → nome da pessoa.
