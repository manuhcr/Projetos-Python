#O arquivo modelos.py contém as classes que representam os modelos da aplicação.
# Essas classes servem como uma receita para criar objetos, que serão utilizados
# pelo repositório e pela interface.

# Importa o decorador @dataclass,
# utilizado para criar classes que
# armazenam apenas dados, gerando
# automaticamente métodos como __init__().
from dataclasses import dataclass

# Importa a classe date, utilizada para
# representar datas (dia, mês e ano).
#
# Ela será utilizada para armazenar
# a data de cadastro do produto.
from datetime import date

# @dataclass é um decorador utilizado para criar
# classes que armazenam apenas dados.
#
# Ela cria automaticamente métodos como __init__(),
# evitando que seja necessário escrever um construtor
# manualmente.
#
# Neste projeto, a classe Produto funciona como um
# modelo (ou receita) de um produto.
#
# O repositório cria objetos dessa classe quando
# lê informações do banco de dados, e a interface
# utiliza esses objetos para exibir e manipular
# os dados.
@dataclass
class Produto:

    # Identificador único do produto.
    #
    # Antes de ser salvo no banco de dados,
    # o ID pode ser None, pois ele será gerado
    # automaticamente pelo MySQL.
    idProduto: int | None

    # Categoria à qual o produto pertence.
    categoriaProduto: str

    # Nome do produto.
    nomeProduto: str

    # Preço unitário do produto.
    precoProduto: float

    # Quantidade disponível em estoque.
    estoque: int

    # Data em que o produto foi cadastrado.
    dataProduto: date