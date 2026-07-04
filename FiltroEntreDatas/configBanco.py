# Importa a biblioteca PyMySQL, que fornece recursos para conectar o programa
# Python a um servidor MySQL, e a biblioteca os para manipulação de caminhos e arquivos.
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


# Credenciais de acesso ao MySQL (busca do .env ou usa o padrão).
usuario = os.getenv('DB_USER', 'root')
senha = os.getenv('DB_PASSWORD', '$aluno123DB')

# Informações do servidor
host = os.getenv('DB_HOST', 'localhost')
porta = int(os.getenv('DB_PORT', '3306'))

# Nome do banco de dados principal
nomeBanco = 'agendaDatasBrDb'

# Pasta onde serão salvos os arquivos SQL exportados.
# Definido de forma dinâmica para funcionar em qualquer sistema (Windows, macOS ou Linux).
# Se resolve para a pasta 'SQLDump/' na raiz do repositório 'Projetos-Python'.
caminhoExportarSQL = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
    'SQLDump'
)


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
        db=banco if banco else None,    # Banco de dados utilizado
        charset='utf8mb4',              # Suporte completo a caracteres Unicode
        cursorclass=pymysql.cursors.DictCursor,  # Retorna resultados em formato de dicionário
        autocommit=False                # Exige commit manual das alterações
    )

    return conn
