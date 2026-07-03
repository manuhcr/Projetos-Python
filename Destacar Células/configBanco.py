# Importa a biblioteca PyMySQL, responsável por
# conectar o Python ao banco de dados MySQL.
#
# Ela permite executar comandos SQL como:
# INSERT, SELECT, UPDATE e DELETE (CRUD).
import pymysql


# Usuário utilizado para acessar o MySQL.
usuario = "root"

# Senha do usuário do MySQL.
senha = "$aluno123DB"

# Endereço do servidor onde o MySQL está executando.
#
# "localhost" indica que o banco está
# na própria máquina.
host = "localhost"

# Porta utilizada pelo MySQL.
#
# A porta padrão é 3306.
porta = 3306

# Nome do banco de dados utilizado
# pela aplicação.
nomeDoBanco = "destacarCelulaDB"


# Cria e retorna uma conexão com o banco de dados.
#
# O parâmetro "banco" é opcional.
#
# Se um nome de banco for informado,
# a conexão será feita diretamente nele.
#
# Caso contrário, a conexão será criada
# apenas com o servidor MySQL.
def conectar(banco: str | None = None) -> pymysql.connections.Connection:

    conexao = pymysql.connect(

        # Endereço do servidor MySQL.
        host=host,

        # Porta utilizada para a conexão.
        port=porta,

        # Usuário do banco.
        user=usuario,

        # Senha do usuário.
        password=senha,

        # Banco de dados utilizado.
        #
        # Se "banco" possuir um valor,
        # conecta nesse banco.
        #
        # Caso contrário, utiliza None,
        # conectando apenas ao servidor.
        database=banco if banco else None,

        # Define a codificação utilizada.
        #
        # utf8mb4 suporta caracteres especiais,
        # acentos e emojis.
        charset="utf8mb4",

        # Define o tipo de cursor utilizado pela conexão.
        #
        # O cursor é um objeto responsável por executar
        # comandos SQL no banco de dados e recuperar
        # os resultados das consultas.
        #
        # É através dele que são utilizados métodos como:
        #
        # cursor.execute()
        # cursor.fetchone()
        # cursor.fetchall()
        #
        # O DictCursor faz com que cada linha retornada
        # pelo banco seja um dicionário, em vez de
        # uma tupla.
        #
        # Exemplo:
        #
        # Sem DictCursor:
        #
        # ("Maria", 2500.00)
        #
        # nome = row[0]
        # total = row[1]
        #
        # Com DictCursor:
        #
        # {
        #     "nomeCliente": "Maria",
        #     "total": 2500.00
        # }
        #
        # nome = row["nomeCliente"]
        # total = row["total"]
        #
        # Isso torna o código mais legível e facilita
        # o acesso aos dados retornados pelo banco.
        cursorclass=pymysql.cursors.DictCursor,

        # As alterações no banco não são
        # salvas automaticamente.
        #
        # É necessário chamar:
        # conexao.commit()
        #
        # Isso evita salvar alterações
        # por engano.
        autocommit=False
    )

    # Retorna a conexão criada.
    return conexao