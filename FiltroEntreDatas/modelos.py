# Importa o decorador @dataclass da biblioteca dataclasses.
# Esse recurso é utilizado para criar classes que têm como principal
# objetivo armazenar dados. Ao utilizar @dataclass, o Python gera
# automaticamente alguns métodos importantes, como o construtor (__init__),
# responsável por inicializar os atributos do objeto.
#
# Sem o uso de @dataclass, seria necessário criar manualmente esses métodos,
# escrevendo mais código para atribuir valores aos atributos sempre que um
# objeto fosse criado. Isso tornaria a classe maior, mais repetitiva e mais
# sujeita a erros de programação.
from dataclasses import dataclass

# Importa a classe date da biblioteca datetime.
# A classe date é utilizada para representar datas contendo apenas
# dia, mês e ano, sem armazenar informações de horário.
# Ela será utilizada para registrar a data de cada evento.
from datetime import date

# O decorador @dataclass informa ao Python que a classe abaixo será
# utilizada principalmente para armazenar dados.
# Com isso, o Python cria automaticamente métodos como:
# - __init__(): permite criar objetos atribuindo valores aos atributos;
# - __repr__(): exibe o objeto de forma legível;
# - __eq__(): permite comparar objetos.
#
# Sem @dataclass, seria necessário implementar esses métodos manualmente.
@dataclass
class Evento:

    # Armazena o identificador único do evento.
    # O tipo "int | None" indica que o atributo pode receber:
    # - um número inteiro (quando o evento já estiver cadastrado);
    # - None (quando o evento ainda não possuir um ID definido).
    #
    # Isso é comum em sistemas com banco de dados, pois o ID geralmente
    # é gerado automaticamente durante o cadastro do registro.
    id: int | None

    # Armazena a descrição do evento.
    # O tipo str indica que o valor será uma sequência de caracteres,
    # como um nome ou uma breve explicação sobre o evento.
    descricao: str

    # Armazena a data em que o evento ocorrerá.
    # O tipo date garante que o valor seja tratado como uma data válida,
    # facilitando operações como comparação, ordenação e formatação.
    dataEvento: date