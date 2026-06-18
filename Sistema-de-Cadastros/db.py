# Biblioteca utilizada para conectar o Python
# ao banco de dados MySQL.
import pymysql

# Importa as classes de exceção (erros)
# fornecidas pela biblioteca PyMySQL.
#
# Elas permitem identificar problemas
# específicos durante a conexão.
from pymysql import err as pymysql_err

# Importa as configurações necessárias para
# estabelecer a conexão com o banco de dados.
#
# Essas informações estão armazenadas em
# um arquivo separado para facilitar a manutenção.
from config import (
    host,
    porta,
    usuario,
    senha,
    nome_banco,
    nome_tabela
)


# Cria e retorna uma conexão com o banco de dados.
#
# Parâmetro:
# usar_banco:
#     True  -> conecta diretamente ao banco informado.
#     False -> conecta apenas ao servidor MySQL.
#
# Retorno:
#     Objeto de conexão que será utilizado para
#     executar comandos SQL.
def conectar(usar_banco=True):
    # Tenta estabelecer a conexão.
    #
    # Caso ocorra algum erro, o fluxo será enviado
    # para o bloco except.
    try:

        # Verifica se a conexão deve ser criada já
        # apontando para o banco de dados principal.
        if usar_banco:
            # Cria uma conexão com o MySQL utilizando
            # os parâmetros definidos no arquivo config.py.
            return pymysql.connect(

                # Endereço do servidor MySQL.
                host=host,

                # Porta utilizada pelo MySQL.
                port=porta,

                # Usuário para autenticação.
                user=usuario,

                # Senha do usuário.
                password=senha,

                # Banco de dados que será utilizado.
                database=nome_banco,

                # Permite armazenar caracteres especiais,
                # acentos e emojis.
                charset='utf8mb4',

                # Define o tipo de cursor utilizado
                # para executar consultas SQL.
                cursorclass=pymysql.cursors.Cursor,

                # Salva automaticamente alterações realizadas
                # por comandos INSERT, UPDATE e DELETE,
                # sem precisar da função conn.commit().
                autocommit=True
            )

        # Caso usar_banco seja False, cria uma conexão
        # apenas com o servidor MySQL, sem selecionar
        # previamente um banco de dados.
        #
        # Esse tipo de conexão costuma ser utilizado
        # quando precisamos criar bancos ou realizar
        # operações administrativas.
        else:

            return pymysql.connect(

                # Endereço do servidor MySQL.
                host=host,

                # Porta utilizada pelo MySQL.
                port=porta,

                # Usuário utilizado na autenticação.
                user=usuario,

                # Senha do usuário.
                password=senha,

                # Conjunto de caracteres utilizado
                # para suportar acentos e caracteres especiais.
                charset='utf8mb4',

                # Tipo de cursor utilizado para executar
                # comandos SQL.
                cursorclass=pymysql.cursors.Cursor,

                # Salva automaticamente as alterações
                # realizadas no banco de dados.
                autocommit=True

            )

    # Captura erros relacionados à conexão
    # com o servidor MySQL.
    #
    # Se ocorrer algum problema durante o connect(),
    # o erro será armazenado na variável "erro".
    except pymysql_err.OperationalError as erro:

        # Verifica se o erro ocorrido foi o código 1049.
        #
        # O erro 1049 significa:
        # "Unknown database"
        #
        # Ou seja, o banco informado ainda não existe.
        if getattr(erro, "args", None) and erro.args[0] == 1049:
            # Cria uma conexão temporária para permitir
            # a criação do banco de dados e da tabela.
            #
            # Como o banco ainda não existe, primeiro
            # precisamos conectar ao servidor MySQL.
            conn = pymysql.connect(

                # Endereço do servidor.
                host=host,

                # Usuário utilizado para autenticação.
                user=usuario,

                # Senha do usuário.
                password=senha,

                # Porta do MySQL.
                port=porta,

                # Conjunto de caracteres.
                charset='utf8mb4',

                # Cursor utilizado para executar SQL.
                cursorclass=pymysql.cursors.Cursor
            )
            # Cria automaticamente o banco de dados
            # e a tabela principal da aplicação.
            criar_banco_e_tabela(conn)

            # Fecha a conexão temporária após a criação
            # da estrutura necessária.
            conn.close()

            # Cria e retorna uma nova conexão com o banco de dados.
            #
            # Neste ponto do código, o banco já existe
            # (ou acabou de ser criado pela função
            # criar_banco_e_tabela()).
            #
            # Por isso a aplicação já pode se conectar
            # normalmente e começar a executar consultas,
            # inserções, alterações e exclusões.
            return pymysql.connect(

                # Endereço do servidor MySQL.
                host=host,

                # Usuário utilizado para autenticação.
                user=usuario,

                # Senha associada ao usuário informado.
                password=senha,

                # Nome do banco de dados que será utilizado
                # pela aplicação.
                #
                # Como o banco já existe, a conexão será
                # criada diretamente apontando para ele.
                database=nome_banco,

                # Porta utilizada pelo servidor MySQL.
                port=porta,

                # Define o conjunto de caracteres utilizado
                # durante a comunicação com o banco.
                #
                # utf8mb4 permite armazenar acentos,
                # caracteres especiais e emojis.
                charset='utf8mb4',

                # Faz com que comandos como INSERT,
                # UPDATE e DELETE sejam gravados
                # automaticamente no banco de dados.
                #
                # Sem essa configuração seria necessário
                # executar conn.commit() manualmente.
                autocommit=True,

                # Define o tipo de cursor utilizado
                # para executar comandos SQL.
                #
                # O Cursor é responsável por enviar
                # instruções SQL para o banco e obter
                # os resultados retornados.
                cursorclass=pymysql.cursors.Cursor

            )

# Cria automaticamente o banco de dados e a tabela
# principal utilizada pela aplicação.
#
# Parâmetro:
# conn -> conexão ativa com o servidor MySQL.
def criar_banco_e_tabela(conn):

    # Cria um cursor para executar comandos SQL.
    #
    # O comando "with" funciona como um gerenciador
    # de contexto (Context Manager), garantindo que
    # o cursor será fechado automaticamente ao final
    # da execução, mesmo que ocorra algum erro.
    with conn.cursor() as curs:

        # Cria o banco de dados caso ele ainda não exista.
        #
        # IF NOT EXISTS:
        #     Evita erro caso o banco já tenha sido criado.
        #
        # DEFAULT CHARACTER SET utf8mb4:
        #     Permite armazenar acentos, caracteres
        #     especiais e emojis.
        #
        # COLLATE:
        #     Define as regras de comparação e ordenação
        #     dos textos armazenados.
        curs.execute(
            f"CREATE DATABASE IF NOT EXISTS {nome_banco} "
            "DEFAULT CHARACTER SET utf8mb4 "
            "COLLATE utf8mb4_general_ci;"
        )

        # Seleciona o banco recém-criado.
        #
        # A partir desse momento, todos os comandos SQL
        # serão executados dentro deste banco de dados.
        curs.execute(
            f"USE {nome_banco};"
        )

        # Cria a tabela principal da aplicação.
        #
        # IF NOT EXISTS:
        #     Evita erro caso a tabela já exista.
        #
        # A tabela será utilizada para armazenar
        # os dados cadastrados pelo usuário.
        curs.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {nome_tabela}(

                -- Identificador único do registro.
                -- AUTO_INCREMENT faz o MySQL gerar
                -- automaticamente os valores.
                -- PRIMARY KEY define a chave primária.
                id INT AUTO_INCREMENT PRIMARY KEY,

                -- Armazena o nome da pessoa.
                -- VARCHAR(120) permite até
                -- 120 caracteres.
                -- NOT NULL torna o campo obrigatório.
                nome VARCHAR(120) NOT NULL,

                -- Armazena o endereço de e-mail.
                -- Campo obrigatório.
                email VARCHAR(250) NOT NULL,

                -- Armazena o telefone da pessoa.
                -- Foi utilizado VARCHAR porque
                -- telefones são tratados como texto
                -- e podem conter caracteres como:
                -- (), -, espaços e +55.
                telefone VARCHAR(30) NOT NULL,

                -- Data e hora de criação do registro.
                --
                -- CURRENT_TIMESTAMP faz com que
                -- o próprio MySQL preencha
                -- automaticamente esse valor
                -- no momento do cadastro.
                criado_em TIMESTAMP NOT NULL
                DEFAULT CURRENT_TIMESTAMP

            )

            -- InnoDB é o mecanismo de armazenamento
            -- utilizado pelo MySQL.
            --
            -- Ele oferece suporte a relacionamentos,
            -- transações e integridade dos dados.
            ENGINE=InnoDB

            -- Define o conjunto de caracteres
            -- utilizado pela tabela.
            DEFAULT CHARACTER SET utf8mb4;
            """
        )
