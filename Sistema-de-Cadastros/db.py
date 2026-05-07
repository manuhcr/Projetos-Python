import pymysql
from pymysql import err as pymysql_err

from config import host, porta, usuario, senha, nome_banco, nome_tabela


def conectar(usar_banco=True):

    try:
        # Tenta conectar usando as configurações salvas no arquivo 'config.py'
        if usar_banco:
            return pymysql.connect(
                host=host,
                port=porta,
                user=usuario,
                password=senha,
                database=nome_banco,  # Tenta entrar direto no seu banco
                charset='utf8mb4',
                cursorclass=pymysql.cursors.Cursor,
                autocommit=True  # Salva as alterações automaticamente sem precisar de conn.commit()
            )
        # ... (o else faz algo similar)
        else:

             return pymysql.connect(host=host,

                               port=porta,

                               user=usuario,

                               password=senha,

                               database=nome_banco,

                               charset='utf8mb4',

                               cursorclass=pymysql.cursors.Cursor,

                               autocommit=True

                               )


    except pymysql_err.OperationalError as erro:

        # Se der erro porque o banco NÃO EXISTE (Erro 1049 do MySQL)
        if getattr(erro, "args", None) and erro.args[0] == 1049:
            # Aqui o código é esperto: ele conecta-se ao servidor sem especificar o banco
             conn = pymysql.connect(

            host=host,

            user=usuario,

            password=senha,

            db=nome_banco,

            port=porta,

            charset='utf8mb4',

            cursorclass=pymysql.cursors.Cursor)
            # Chama a função para criar o banco e a tabela do zero
             criar_banco_e_tabela(conn)
            # Fecha essa conexão temporária e retorna uma conexão nova e pronta
             conn.close()


        return pymysql.connect(

            host=host,

            user=usuario,

            password=senha,

            database=nome_banco,

            port=porta,

            charset='utf8mb4',

            autocommit=True,

            cursorclass=pymysql.cursors.Cursor

        )




def criar_banco_e_tabela(conn):
    # O 'with' garante que o cursor seja fechado automaticamente ao final,
    # mesmo que ocorra um erro. É uma prática de segurança (Context Manager).
    with conn.cursor() as curs:
        # 1. CRIAÇÃO DO BANCO (O 'Container' principal)
        # Usamos DEFAULT CHARACTER SET para que o banco aceite acentos e emojis (utf8mb4).
        # Nota: Corrigi 'DEFAUT' para 'DEFAULT'.
        curs.execute(f"CREATE DATABASE IF NOT EXISTS {nome_banco} "
                     "DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")

        # 2. SELEÇÃO DO BANCO
        # Dizemos ao MySQL: "Ei, todas as ordens a partir de agora são para este banco específico".
        curs.execute(f"USE {nome_banco};")

        # 3. CRIAÇÃO DA TABELA (A planilha de dados)
        # Aqui definimos as colunas: id, nome, email, telefone e data.
        curs.execute(
            f"""
               CREATE TABLE IF NOT EXISTS {nome_tabela}(
               id INT AUTO_INCREMENT PRIMARY KEY, -- ID único que cresce sozinho (1, 2, 3...)
               nome VARCHAR(120) NOT NULL,        -- Texto de até 120 letras, obrigatório
               email VARCHAR(250) NOT NULL,       -- Texto de até 250 letras, obrigatório
               telefone VARCHAR(30) NOT NULL,     -- Texto para números, obrigatório
               criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP -- Data/Hora automática
               ) ENGINE= InnoDB DEFAULT CHARACTER SET utf8mb4; 
            """
        )
        # Removi uma vírgula que estava depois de CURRENT_TIMESTAMP,
        # pois o último item de uma lista SQL não pode ter vírgula.

    return None