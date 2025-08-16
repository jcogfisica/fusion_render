# ======================================================================
# MODELS COMENTADOS LINHA A LINHA (SUPER DIDÁTICOS)
# ======================================================================

# Importações de módulos padrão do Python
import os       # O módulo 'os' fornece funções para manipular caminhos de arquivos,
                # variáveis de ambiente, diretórios e arquivos locais.
import uuid     # O módulo 'uuid' gera identificadores únicos universais (UUID),
                # usados aqui para nomear arquivos de forma única e evitar conflitos.

# Importações do Django
from django.db import models           # Necessário para criar modelos (classes que representam tabelas no banco)
from django.conf import settings       # Permite acessar variáveis definidas em settings.py, como MEDIA_URL
from pictures.models import PictureField  # Campo avançado para imagens, suporta breakpoints, placeholders e formatos de arquivo.

# ----------------------------------------------------------------------
# Função auxiliar para gerar nomes de arquivos únicos
# ----------------------------------------------------------------------
def get_file_path(_instance, filename):
    """
    Recebe a instância do modelo e o nome original do arquivo.
    Retorna um novo nome único baseado em UUID.
    Isso evita conflitos de nome quando vários arquivos têm o mesmo nome.
    """
    ext = filename.split('.')[-1]          # Pega a extensão do arquivo (parte após o último ponto)
    filename = f'{uuid.uuid4()}.{ext}'     # Cria um novo nome usando UUID + extensão original
    return filename                         # Retorna o nome final que será usado para salvar o arquivo

# ======================================================================
# Classe Base (abstrata) para outros modelos
# ======================================================================
class Base(models.Model):
    """
    Modelo base que adiciona campos comuns a todos os modelos que herdam dele:
    - criado: registra a data de criação
    - modificado: registra a última modificação
    - ativo: flag para exclusão lógica (não apaga do banco)
    """
    criado = models.DateTimeField(
        'Data de criação',  # Nome amigável no admin
        auto_now_add=True   # Define automaticamente a data ao criar o objeto
    )

    modificado = models.DateTimeField(
        'Data de modificação',  # Nome amigável no admin
        auto_now=True           # Atualiza automaticamente a data sempre que o objeto é salvo
    )

    ativo = models.BooleanField(
        'Ativo?',  # Nome amigável no admin
        default=True  # Todos os objetos criados são ativos por padrão
    )

    class Meta:
        abstract = True  # Não cria tabela no banco, só serve de base para outros modelos

# ======================================================================
# Modelo Cargo
# ======================================================================
class Cargo(Base):
    """
    Representa um cargo dentro da equipe (ex: Designer, Desenvolvedor)
    Herdando Base, já possui campos criado, modificado e ativo.
    """
    cargo = models.CharField(
        'Cargo',       # Nome amigável no admin
        max_length=100 # Limite máximo de caracteres (obrigatório para CharField)
    )

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    def __str__(self):
        """
        Retorna o nome do cargo ao converter o objeto em string (ex: no admin)
        """
        return self.cargo

# ======================================================================
# Modelo Servico
# ======================================================================
class Servico(Base):
    """
    Representa um serviço oferecido.
    Herdando Base, já possui campos criado, modificado e ativo.
    """
    # Opções possíveis para o campo 'icone' (para exibição visual)
    choices = (
        ("lni-cog", "Engrenagem"),
        ("lni-stats-up", "Gráfico"),
        ("lni-users", "Usuários"),
        ("lni-layers", "Design"),
        ("lni-mobile", "Mobile"),
        ("lni-rocket", "Foguete")
    )

    servico = models.CharField(
        'Serviço',    # Nome legível no admin
        max_length=100  # Limite de caracteres
    )

    descricao = models.TextField(
        'Descrição',  # Nome legível no admin
        blank=True,   # Permite campo vazio
        max_length=200 # Limite usado para validação, mesmo sendo TextField
    )

    icone = models.CharField(
        'Ícone',       # Nome legível no admin
        max_length=12, # Tamanho máximo do código do ícone
        choices=choices # Restringe os valores possíveis aos definidos em 'choices'
    )

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'

    def __str__(self):
        """
        Retorna o nome do serviço quando o objeto é convertido em string (ex: admin)
        """
        return self.servico

# ======================================================================
# Modelo Equipe
# ======================================================================
class Equipe(Base):
    """
    Representa um membro da equipe.
    Herdando Base, já possui criado, modificado e ativo.
    """
    nome = models.CharField(
        'Nome',       # Nome legível no admin
        max_length=100 # Limite de caracteres
    )

    cargo = models.ForeignKey(
        'core.Cargo',        # Relaciona o membro a um cargo específico
        verbose_name='Cargo',# Nome amigável no admin
        on_delete=models.CASCADE  # Se o cargo for deletado, todos os membros relacionados também serão deletados
    )

    bio = models.TextField(
        'Bio',      # Nome amigável no admin
        blank=True, # Permite campo vazio
        max_length=200 # Limite recomendado (TextField não exige)
    )

    imagem = PictureField(
        upload_to=get_file_path,    # Função que define o caminho e o nome do arquivo ao salvar.
                                     # Aqui usamos a função get_file_path, que cria um nome único com UUID
                                     # Isso evita conflitos de nomes iguais no bucket ou no disco local.

        width_field="image_width",  # Nome do campo que armazenará a largura real da imagem original.
                                     # Quando uma imagem é salva, o Django automaticamente grava a largura nesse campo.
                                     # Útil para exibir imagens com dimensões corretas no template.

        height_field="image_height",# Nome do campo que armazenará a altura real da imagem original.
                                     # Funciona igual ao width_field, mas para altura.

        aspect_ratios=[None, "1/1"], # Lista de proporções permitidas para o corte da imagem.
                                      # None → permite qualquer proporção (liberdade total)
                                      # "1/1" → permite corte quadrado (mesma largura e altura)
                                      # O usuário ou o sistema pode cortar ou redimensionar a imagem baseado nessas proporções.

        breakpoints={},              # Dicionário para definir larguras de imagens responsivas.
                                      # Cada breakpoint define uma versão redimensionada da imagem.
                                      # Vazio {} → sem redimensionamento automático.
                                      # Se fosse {"thumb": 480, "desktop": 992}, seriam criadas versões 480px e 992px.

        file_types=["PNG"],          # Lista de formatos de arquivo permitidos.
                                      # Aqui apenas PNG é aceito.
                                      # Evita que usuários enviem JPG, GIF ou WEBP, por exemplo.

        grid_columns=1,              # Configuração visual para exibição da imagem em grids responsivos.
                                      # Indica quantas colunas da grid a imagem ocupa.
                                      # Usado internamente pelo sistema de PictureField para layout de frontend.

        container_width=480,         # Largura máxima do container em pixels.
                                      # Base usada para calcular imagens responsivas e gerar URLs de imagem corretas.
                                      # Ex: se o container for 480px, a imagem redimensionada será gerada até esse limite.

        pixel_densities=[1],         # Lista de densidades de pixel suportadas.
                                      # 1 → densidade padrão (não gera versão retina)
                                      # Se fosse [1, 2], seriam geradas duas versões: padrão e 2x (retina)
                                      # Útil para sites que querem imagens mais nítidas em telas de alta resolução.
    )


    image_width = models.PositiveIntegerField(
        null=True,  # Pode ser nulo
        blank=True  # Pode ficar em branco
    )
    image_height = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    facebook = models.CharField('Facebook', max_length=100, default='#')   # Link do Facebook
    twitter = models.CharField('X', max_length=100, default='#')           # Link do Twitter/X
    instagram = models.CharField('Instagram', max_length=100, default='#') # Link do Instagram

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'

    # ------------------------------------------------------------------
    # Metodo para retornar URL da imagem
    # ------------------------------------------------------------------
    def imagem_480_url(self):
        """
        Retorna a URL pública da imagem.
        Se não houver imagem, retorna None.
        """
        if self.imagem:           # Verifica se existe imagem associada
            return self.imagem.url # Retorna URL pública (GCS ou local)
        return None               # Sem imagem, retorna None

    def __str__(self):
        """
        Representação em string do objeto (ex: no admin)
        """
        return self.nome
