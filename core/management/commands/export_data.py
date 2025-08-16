# Importa a classe BaseCommand, que é a classe base para criar comandos customizados no Django
# Comandos customizados permitem criar scripts que você pode executar via "python manage.py nome_do_comando"
from django.core.management.base import BaseCommand

# Importa os serializadores do Django, que permitem transformar objetos de banco em JSON ou outros formatos
# É essencial para gerar backups compatíveis com fixtures do Django
from django.core import serializers

# Importa os modelos que você deseja exportar
# Substitua "core.models" e os nomes dos modelos pelos do seu projeto, se necessário
from core.models import Cargo, Equipe, Servico

# Define uma nova classe de comando personalizada
# Todo comando do Django precisa herdar BaseCommand
class Command(BaseCommand):
    # Mensagem de ajuda que aparece quando você executa "python manage.py help export_data"
    help = 'Exporta os modelos Cargo, Equipe e Servico para JSON de fixture com UTF-8'

    # O método handle() é chamado quando você executa o comando
    # É o "coração" do comando, onde a lógica real acontece
    def handle(self, *args, **kwargs):
        # Lista de classes de modelos que serão exportadas
        # Cada item aqui é uma referência direta à classe do modelo
        lista_classes = [Cargo, Equipe, Servico]

        # Lista de nomes que serão usados para criar os arquivos JSON
        # O nome será usado como sufixo do arquivo: "backup_nome.json"
        nomes = ['cargo', 'equipe', 'servico']

        # Percorre cada modelo junto com seu nome correspondente
        # zip() combina duas listas em pares: (modelo, nome)
        for model_class, complemento in zip(lista_classes, nomes):
            # Serializa todos os objetos do modelo para JSON no formato de fixture do Django
            # serializers.serialize('json', ...) produz uma lista de dicionários com:
            #  - "model": nome do app + nome do modelo (ex: "core.Cargo")
            #  - "pk": chave primária do objeto
            #  - "fields": dicionário com todos os campos e valores do objeto
            # Esse formato é **compatível com o comando "loaddata" do Django**
            data = serializers.serialize('json', model_class.objects.all())

            # Abre o arquivo para escrita
            # "f'backup_{complemento}.json'" cria um arquivo com o nome apropriado
            # encoding='utf-8' garante que caracteres acentuados ou especiais sejam preservados corretamente
            # 'w' significa "write" (sobrescreve se o arquivo já existir)
            with open(f'backup_{complemento}.json', 'w', encoding='utf-8') as f:
                # Escreve o JSON serializado no arquivo
                # f.write() grava a string exatamente como gerada pelo serializador
                f.write(data)

        # Exibe uma mensagem de sucesso no terminal
        # self.stdout.write() envia a mensagem para o console
        # self.style.SUCCESS() formata a mensagem em verde, indicando sucesso
        self.stdout.write(self.style.SUCCESS('Backups de fixtures gerados com sucesso!'))
