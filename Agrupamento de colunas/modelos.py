
# Importa o decorador @dataclass.
#
# O @dataclass é utilizado para facilitar a criação
# de classes que armazenam dados.
from dataclasses import dataclass

# Importa a classe date do módulo datetime.
#
# A classe date é utilizada para representar datas
# (dia, mês e ano), sem armazenar horário.
#
# Exemplo:
# data = date(2026, 6, 24)
#
# Resultado:
# 24/06/2026
from datetime import date

# O decorador @dataclass é utilizado para transformar
# a classe em uma estrutura de dados simples e organizada.
#
# Ao utilizá-lo, o Python cria automaticamente métodos
# importantes como:
#
# __init__() -> construtor da classe
# __repr__() -> representação textual do objeto
# __eq__() -> comparação entre objetos
#
# Dessa forma, não é necessário escrever manualmente
# métodos repetitivos apenas para armazenar dados.
#
# A classe Venda será utilizada para representar
# uma venda realizada pela empresa, agrupando todas
# as informações relacionadas em um único objeto.
#
# Exemplo:
#
# venda = Venda(
#     id=1,
#     nomeCliente="Manoela",
#     total=150.00,
#     cidade="São Paulo",
#     setor="Tecnologia",
#     produto="Notebook",
#     quantidade=1
# )
#
# Após criar o objeto, os dados podem ser acessados
# de forma clara através dos atributos:
#
# venda.nomeCliente
# venda.total
# venda.produto
#
# Isso torna o código mais legível e facilita
# a manutenção da aplicação.
@dataclass

# Classe utilizada para representar uma venda.
#
# Cada objeto da classe Venda corresponde a um
# registro armazenado no banco de dados.
class Venda:

    # Identificador único da venda.
    #
    # Pode ser None antes do registro ser salvo
    # no banco de dados.
    id: int | None

    # Nome do cliente que realizou a compra.
    nomeCliente: str

    # Valor total da venda.
    #
    # Normalmente é calculado através da
    # multiplicação da quantidade pelo
    # preço unitário.
    total: float

    # Cidade onde a venda foi realizada.
    cidade: str

    # Setor ou categoria da venda.
    #
    # Exemplo:
    # Tecnologia
    # Alimentos
    # Vestuário
    setor: str

    # Nome do produto vendido.
    produto: str

    # Quantidade de unidades vendidas.
    quantidade: int

    # Valor de uma única unidade do produto.
    #
    # Exemplo:
    # Produto = Notebook
    # Preço Unitário = R$ 2.500,00
    precoUnitario: float

    # Data em que a venda foi realizada.
    #
    # Utiliza o tipo date para armazenar
    # apenas dia, mês e ano.
    dataVenda: date
