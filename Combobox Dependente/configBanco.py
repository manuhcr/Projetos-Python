# Importa a biblioteca responsável pela conexão com o MySQL.
import pymysql


# Usuário do banco de dados.
user: str = 'root'

# Senha do banco de dados.
pwd: str = '$aluno123BD'

# Servidor onde o banco está rodando.
host: str = 'localhost'

# Porta padrão do MySQL.
port: int = 3306

# Nome do banco de dados utilizado pelo sistema.
nameBench: str = 'geo_db'

# Caminho onde os backups SQL serão exportados.
wayExportSql: str = r'C:\Users\manoe\OneDrive\Documents\BackupDumpSql'


# Cria e retorna uma conexão com o banco de dados.
def getConn(nameBench: str | None = None) -> pymysql.connections.Connection:

    conn = pymysql.connect(
        host=host,
        user=user,
        port=port,
        password=pwd,
        database=nameBench,

        # Define a codificação para suportar caracteres especiais.
        charset='utf8mb4',

        # Faz com que as consultas retornem dicionários
        # em vez de tuplas.
        cursorclass=pymysql.cursors.DictCursor,

        # Confirma automaticamente alterações no banco.
        autocommit=False
    )

    return conn