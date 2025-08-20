import uuid
# Importa o módulo `uuid` do Python.
# Esse módulo permite gerar identificadores únicos universais (UUIDs),
# que são úteis para criar nomes de arquivos únicos e evitar conflitos.

from django.test import TestCase
# Importa a classe `TestCase` do Django.
# Essa classe é usada para criar testes automatizados.
# Ela herda de `unittest.TestCase` e adiciona recursos extras do Django:
# - banco de dados de teste isolado,
# - integração com modelos e views,
# - fixtures automáticas.

from model_mommy import mommy
# Importa a biblioteca `model_mommy` (agora substituída pelo `model_bakery`).
# `mommy.make()` cria instâncias de modelos de forma automática, preenchendo
# campos obrigatórios com valores válidos sem precisar especificar manualmente.
# Muito útil para testes de modelos.

from core.models import get_file_path
# Importa a função `get_file_path` do módulo `models.py` do app `core`.
# Essa função é responsável por gerar nomes de arquivos únicos para upload
# baseado em UUID.


# ======================================================================
# Testes para a função get_file_path
# ======================================================================
class GetFilePathTestCase(TestCase):
    # Define uma classe de teste para a função `get_file_path`.
    # Herdando de `TestCase`, podemos criar testes isolados para essa função.

    def setUp(self):
        # Metodo executado antes de cada teste.
        # Aqui criamos dados iniciais que serão usados nos testes.
        self.filename = f"{uuid.uuid4()}.png"
        # Cria um nome de arquivo fictício único usando UUID e extensão PNG.
        # Será usado para comparar o comprimento do nome gerado pela função.

    def test_get_file_path(self):
        # Testa a função `get_file_path`.
        arquivo = get_file_path(None, "teste.png")
        # Chama a função passando `None` como instância (não usada)
        # e "teste.png" como nome original do arquivo.
        self.assertTrue(len(arquivo) == len(self.filename))
        # Verifica se o tamanho do nome retornado pela função é igual ao tamanho
        # do nome gerado no setUp. Garante que o UUID foi gerado corretamente.


# ======================================================================
# Testes para o modelo Servico
# ======================================================================
class ServicoTestCase(TestCase):
    # Define testes para o modelo `Servico`.

    def setUp(self):
        # Cria uma instância de `Servico` usando `mommy.make()`.
        self.servico = mommy.make("Servico")
        # `mommy.make()` cria automaticamente os campos obrigatórios com valores válidos.

    def test_str(self):
        # Testa o metodo `__str__` do modelo `Servico`.
        self.assertEqual(str(self.servico), self.servico.servico)
        # Garante que, ao converter o objeto em string, retorna o nome do serviço.


# ======================================================================
# Testes para o modelo Cargo
# ======================================================================
class CargoTestCase(TestCase):
    # Define testes para o modelo `Cargo`.

    def setUp(self):
        # Cria uma instância de `Cargo` usando `mommy.make()`.
        self.cargo = mommy.make("Cargo")

    def test_str(self):
        # Testa o metodo `__str__` do modelo `Cargo`.
        self.assertEqual(str(self.cargo), self.cargo.cargo)
        # Garante que o objeto convertido em string retorna o nome do cargo.


# ======================================================================
# Testes para o modelo Equipe
# ======================================================================
class EquipeTestCase(TestCase):
    # Define testes para o modelo `Equipe`.

    def setUp(self):
        # Cria uma instância de `Equipe` usando `mommy.make()`.
        self.equipe = mommy.make("Equipe")

    def test_str(self):
        # Testa o metodo `__str__` do modelo `Equipe`.
        self.assertEqual(str(self.equipe), self.equipe.nome)
        # Garante que o objeto convertido em string retorna o nome do membro da equipe.

