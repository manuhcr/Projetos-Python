# Importa a biblioteca PyMySQL, que fornece recursos para conectar o programa
# Python a um servidor MySQL. Com ela é possível criar conexões, executar
# consultas SQL (SELECT, INSERT, UPDATE e DELETE), manipular tabelas e
# acessar os dados armazenados no banco de dados.
import pymysql

# Credenciais de acesso ao MySQL
usuario = 'root'
senha = '$aluno123BD'

# Informações do servidor
host = 'localhost'
porta = 3306

# Nome do banco de dados principal
nomeBanco = 'agendaDatasBrDb'

# Pasta onde serão salvos os arquivos SQL exportados
caminhoExportarSQL = r'C:\Users\manoe\PycharmProjects\Projetos-Python\SQLDump'

def obterConexao(banco: str | None = None) -> pymysql.connections.Connection:
    """
    Cria e retorna uma conexão com o MySQL.

    Parâmetros:
        banco (str | None):
            Nome do banco a ser conectado.
            Se nenhum valor for informado, utiliza o banco padrão.

    Retorno:
        pymysql.connections.Connection:
            Objeto de conexão com o banco de dados.
    """

    conn = pymysql.connect(
        host=host,                      # Endereço do servidor MySQL
        user=usuario,                   # Usuário de acesso
        passwd=senha,                   # Senha de acesso
        db=nomeBanco if banco else None,# Banco de dados utilizado
        charset='utf8mb4',              # Suporte completo a caracteres Unicode
        cursorclass=pymysql.cursors.DictCursor,  # Retorna resultados em formato de dicionário
        autocommit=False                # Exige commit manual das alterações
    )

    return conn
