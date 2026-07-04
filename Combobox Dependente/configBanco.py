# Importa as bibliotecas responsáveis pela conexão e manipulação de arquivos/pastas.
import pymysql
import os


# Função para carregar variáveis do arquivo .env de forma manual,
# sem exigir a instalação de bibliotecas externas adicionais (como python-dotenv).
def carregar_env() -> None:
    # Caminhos possíveis onde o arquivo .env pode estar localizado
    caminhos = [
        os.path.join(os.getcwd(), '.env'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    ]
    for caminho in caminhos:
        if os.path.exists(caminho):
            try:
                with open(caminho, 'r', encoding='utf-8') as f:
                    for linha in f:
                        linha = linha.strip()
                        # Ignora comentários e linhas vazias
                        if not linha or linha.startswith('#'):
                            continue
                        if '=' in linha:
                            chave, valor = linha.split('=', 1)
                            # Remove espaços e aspas extras dos valores
                            os.environ[chave.strip()] = valor.strip().strip("'").strip('"')
                break  # Encontrou e carregou com sucesso, pode encerrar a busca
            except Exception:
                pass

# Dispara a função para carregar o .env antes de definir as variáveis
carregar_env()


# Usuário do banco de dados (busca do .env ou usa o padrão).
user: str = os.getenv('DB_USER', 'root')

# Senha do banco de dados (busca do .env ou usa o padrão).
pwd: str = os.getenv('DB_PASSWORD', '$aluno123DB')

# Servidor onde o banco está rodando (busca do .env ou usa o padrão).
host: str = os.getenv('DB_HOST', 'localhost')

# Porta padrão do MySQL (busca do .env ou usa o padrão).
port: int = int(os.getenv('DB_PORT', '3306'))

# Nome do banco de dados utilizado pelo sistema.
nameBench: str = 'geo_db'

# Caminho onde os backups SQL serão exportados.
# Definido de forma dinâmica para que funcione tanto no Windows quanto no macOS/Linux!
# Se resolve para a pasta 'SQLDump/' na raiz do repositório 'Projetos-Python'.
wayExportSql: str = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
    'SQLDump'
)


# Cria e retorna uma conexão com o banco de dados.
def getConn(banco: str | None = None) -> pymysql.connections.Connection:
    """Cria e retorna uma conexão com o MySQL.

    - getConn()         -> conecta ao SERVIDOR, sem selecionar um banco.
                           Útil para criar o banco antes de ele existir.
    - getConn("geo_db") -> conecta diretamente a um banco específico.

    Obs.: o parâmetro se chama 'banco' (e não 'nameBench') de propósito,
    para não se confundir com a variável global nameBench = 'geo_db'.
    """

    conn = pymysql.connect(
        host=host,
        user=user,
        port=port,
        password=pwd,
        database=banco,

        # Define a codificação para suportar caracteres especiais.
        charset='utf8mb4',

        # Faz com que as consultas retornem dicionários
        # em vez de tuplas.
        cursorclass=pymysql.cursors.DictCursor,

        # Confirma automaticamente alterações no banco.
        autocommit=False
    )

    return conn
