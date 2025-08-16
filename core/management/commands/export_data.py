# =============================================
# IMPORTS NECESSÁRIOS
# =============================================
from django.core.management.base import BaseCommand
# BaseCommand é a classe do Django que permite criar comandos personalizados
# que podem ser executados com `python manage.py seu_comando`.
# Ao herdar dela, criamos o metodo handle(), que será chamado quando o comando for executado.

from core.models import Cargo, Equipe, Servico
# Importa os modelos que você quer exportar.
# Substitua 'core.models' pelo caminho correto do seu app.
# Esses modelos contêm os dados que serão serializados para JSON.

import json
# Módulo nativo do Python para trabalhar com JSON.
# Permite converter listas e dicionários Python em arquivos JSON.

import datetime
# Módulo para trabalhar com datas e horas.
# Precisamos dele para detectar objetos datetime e convertê-los para string.

# =============================================
# COMANDO PERSONALIZADO
# =============================================
class Command(BaseCommand):
    # Criamos uma classe chamada Command, obrigatória para comandos personalizados do Django.
    # O Django vai procurar automaticamente uma classe Command em cada arquivo dentro de
    # core/management/commands/ para registrar o comando.

    help = 'Exporta os modelos Cargo, Equipe e Servico para JSON com UTF-8'
    # Mensagem de ajuda que aparece ao rodar `python manage.py help export_data`.
    # Explica resumidamente o que o comando faz.

    # =============================================
    # METODO PRINCIPAL
    # =============================================
    def handle(self, *args, **kwargs):
        # Este é o metodo que o Django chama quando o comando é executado.
        # *args e **kwargs permitem receber parâmetros opcionais do terminal.

        # Lista de modelos a serem exportados
        lista_classes = [Cargo, Equipe, Servico]
        # Lista de nomes para criar arquivos JSON legíveis
        nomes = ['cargo', 'equipe', 'servico']

        # Itera simultaneamente sobre os modelos e seus nomes correspondentes
        for l, complemento in zip(lista_classes, nomes):

            # =============================================
            # OBTER DADOS DO BANCO
            # =============================================
            # values() retorna uma lista de dicionários simples
            # Cada dicionário representa uma linha do banco, chave = nome do campo
            obj = list(l.objects.values())

            # =============================================
            # CONVERTER DATETIME PARA STRING
            # =============================================
            # Percorre cada registro (linha do modelo)
            for registro in obj:
                # Para cada campo do registro
                for chave, valor in registro.items():
                    # Se o valor for um objeto datetime (DateField ou DateTimeField)
                    if isinstance(valor, datetime.datetime) or isinstance(valor, datetime.date):
                        # Converte para string ISO 8601: "YYYY-MM-DD" ou "YYYY-MM-DDTHH:MM:SS"
                        registro[chave] = valor.isoformat()

            # =============================================
            # SALVAR JSON EM ARQUIVO
            # =============================================
            # Abre um arquivo para escrita ('w') com encoding UTF-8
            # Nome do arquivo: backup_cargo.json, backup_equipe.json, backup_servico.json
            with open('backup_' + complemento + '.json', 'w', encoding='utf-8') as f:
                # json.dump escreve a lista de dicionários no arquivo JSON
                # ensure_ascii=False mantém caracteres acentuados legíveis
                # indent=2 formata o JSON de forma bonita (legível)
                json.dump(obj, f, ensure_ascii=False, indent=2)

        # =============================================
        # MENSAGEM DE SUCESSO
        # =============================================
        # Mostra no terminal uma mensagem de sucesso estilizada
        self.stdout.write(self.style.SUCCESS('Backups gerados com sucesso!'))

