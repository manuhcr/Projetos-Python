import pymysql

# ==============================
# CONFIGURAÇÕES DO BANCO
# ==============================

# Usuário do MySQL
user = 'root'

# Senha do MySQL
pwd = '$aluno123BD'

# Endereço do servidor MySQL
# localhost = banco rodando no próprio computador
host = 'localhost'

# Porta padrão do MySQL
port = 3306

# Nome do banco de dados
nameBench = 'geo_db'

# Caminho onde arquivos SQL podem ser exportados
# O "r" evita problemas com barras "\" do Windows
wayExportSql = r'C:\Users\edgle\OneDrive\Documentos\GitHub\Projetos-Python\Combobox Dependente'


# ==============================
# FUNÇÃO DE CONEXÃO
# ==============================

# Cria uma função chamada getConn
#
# Essa função serve para abrir uma conexão com o MySQL
#
# "bench" é um parâmetro opcional
#
# str | None significa:
#
# str  -> pode receber um texto
# None -> pode não receber nada
#
# Exemplos:
#
# get_conn("geo_db")
# → conecta usando o banco geo_db
#
# get_conn()
# → conecta sem selecionar banco
#
# "= None" define o valor padrão
#
# Se nada for passado:
#
# bench = None
#
# automaticamente
#
# "-> pymysql.connections.Connection"
#
# significa que a função retorna
# um objeto de conexão do PyMySQL
#
# Esse objeto permite usar:
#
# conn.cursor()
# conn.commit()
# conn.close()
#
# Exemplo:
#
# conn = getConn()
#
# Agora "conn" é uma conexão MySQL pronta
def getConn(bench: str | None = None) -> pymysql.connections.Connection:

    # Cria conexão com o servidor MySQL
    conn = pymysql.connect(

        # Endereço do servidor
        host=host,

        # Usuário do banco
        user=user,

        # Porta do MySQL
        port=port,

        # Senha do banco
        password=pwd,

        # Banco que será utilizado
        #
        # Se "bench" tiver valor:
        # usa o valor recebido
        #
        # Senão:
        # usa None (sem banco)
        #
        # Exemplo:
        #
        # getConn("geo_db")
        # → conecta usando geo_db
        #
        # getConn()
        # → conecta sem selecionar banco
        database=bench if bench else None,

        # Charset UTF8 completo
        #
        # Permite:
        # - acentos
        # - emojis
        # - caracteres especiais
        charset='utf8mb4',

        # Tipo de cursor
        #
        # DictCursor retorna os dados em formato de dicionário
        #
        # Exemplo:
        #
        # {
        #    "id": 1,
        #    "nome": "Manoela"
        # }
        #
        # Sem DictCursor seria:
        #
        # (1, "Manoela")
        cursorclass=pymysql.cursors.DictCursor,

        # autocommit=False
        #
        # O banco NÃO salva alterações automaticamente
        #
        # Você precisa usar:
        #
        # conn.commit()
        #
        # após INSERT, UPDATE ou DELETE
        autocommit=False
    )

    # Retorna a conexão pronta
    return conn