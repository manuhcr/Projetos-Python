# Importa o recurso "dataclass"
#
# dataclass serve para criar classes de forma mais fácil
#
# Sem ela, precisaríamos escrever várias funções manualmente
from dataclasses import dataclass


# @dataclass é um decorator
#
# Ele fala para o Python:
#
# "Essa classe será usada para guardar dados"
#
# Então o Python cria automaticamente:
#
# - construtor (__init__)
# - impressão bonita (__repr__)
# - comparação (__eq__)
#
# automaticamente
@dataclass


# Cria uma classe chamada Local
#
# Classe = modelo/molde
#
# Pense como:
#
# um formulário
# ou
# uma estrutura de dados
#
# Essa classe representa um LOCAL
#
# Exemplo:
#
# País: Brasil
# Estado: SP
# Cidade: São Paulo
class Local:


    # "id" é um atributo da classe
    #
    # Ele vai guardar o ID do registro
    #
    # Exemplo:
    # 1
    # 2
    # 3
    #
    # int | None significa:
    #
    # int  -> pode ser número inteiro
    # None -> pode estar vazio
    #
    # Isso é útil porque:
    #
    # antes de salvar no banco:
    # id = None
    #
    # depois de salvar:
    # id = 1
    id: int | None


    # Guarda o nome do país
    #
    # str significa texto/string
    #
    # Exemplo:
    # "Brasil"
    country: str


    # Guarda o estado
    #
    # Exemplo:
    # "SP"
    state: str


    # Guarda a cidade
    #
    # Exemplo:
    # "São Paulo"
    city: str



# ==============================
# EXEMPLO DE USO
# ==============================

# Aqui estamos criando um OBJETO
#
# Objeto = dado criado a partir da classe
#
# A classe é o molde
# O objeto é a coisa criada
#
# Exemplo:
#
# Classe -> Planta da casa
# Objeto -> Casa construída

# local = Local(
    # ID do registro
    #id=1,

    # País
    #country="Brasil",

    # Estado
    #state="SP",

    # Cidade
    #city="São Paulo"
# )


# ==============================
# ACESSANDO DADOS
# ==============================

# Podemos acessar os dados usando "."
#
# Isso é MUITO melhor que tuplas
#
# Exemplo ruim:
#
# local[0]
# local[1]
#
# Exemplo bom:
#print(local.country)
#print(local.state)
#print(local.city)