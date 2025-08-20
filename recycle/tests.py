# Importa a classe base de testes do Django. 
# `TestCase` fornece um ambiente de teste isolado, com:
# - banco de dados de teste criado automaticamente (e revertido entre testes),
# - utilitários de asserção (assertEqual, assertTrue, etc.),
# - integração com o runner `manage.py test`.
from django.test import TestCase

# Declara uma função simples chamada `add_num` que recebe um argumento `num`.
# A ideia é ter uma unidade mínima de lógica para demonstrar como testar funções puras.
def add_num(num):
    # Retorna o valor de entrada incrementado em 1.
    # Por ser determinística e sem efeitos colaterais, é ideal para um teste unitário.
    return num + 1

# Define uma classe de teste que herda de `django.test.TestCase`.
# Cada metodo cujo nome começa com `test_` será executado automaticamente como um caso de teste.
# A herança de `TestCase` também garante setup/teardown de BD e utilitários de asserção.
class SimpleTesteCase(TestCase):

    # `setUp` é um hook especial do `unittest`/Django.
    # Ele é executado ANTES de cada metodo de teste, garantindo um estado inicial limpo para cada teste.
    def setUp(self):
        # Armazena em `self.numero` o valor 41, que será usado pelos testes.
        # Usar `self.` torna o valor acessível em qualquer metodo da classe (p.ex., `test_add_num`).
        self.numero = 41

    # Este é o metodo de teste propriamente dito. O prefixo `test_` é obrigatório
    # para que o runner do Django descubra e execute automaticamente este metodo como um teste.
    def test_add_num(self):
        # Chama a função sob teste (`add_num`) passando o dado preparado no `setUp`.
        # Esperamos que 41 se torne 42 após o incremento.
        valor = add_num(self.numero)
        # Verifica a condição booleana com `assertTrue`: se `valor == 42` for True, o teste passa;
        # caso contrário, o teste falha e o runner reporta o erro.
        # Observação: poderíamos usar `assertEqual(valor, 42)` — aqui é uma questão de estilo.
        self.assertTrue(valor == 42)
