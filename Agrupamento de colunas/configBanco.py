# Importa a biblioteca PyMySQL.
#
# Essa biblioteca fornece funções e classes que
# permitem conectar o Python a bancos de dados MySQL,
# executar consultas SQL e manipular registros.
#
# Sem essa biblioteca, o programa não conseguiria
# acessar, inserir, alterar ou excluir dados no banco
import pymysql

# Path (da biblioteca padrão pathlib) é usada para montar caminhos de arquivo
# que funcionam em qualquer sistema operacional (Windows, Mac, Linux).
from pathlib import Path

# Usuário utilizado para acessar o servidor MySQL.
usuario = 'root'

# Senha do usuário configurado no banco de dados.
senha = '$aluno123DB'

# Endereço do servidor MySQL.
# Como o banco está instalado na própria máquina,
# utiliza-se localhost.
host = 'localhost'

# Porta padrão utilizada pelo MySQL.
porta = 3306

# Nome do banco de dados principal da aplicação.
nomeBanco = 'agrupamentoTabelasDB'

# Diretório utilizado para armazenar arquivos
# de exportação SQL (dump do banco).
# Aponta para a pasta SQLDump/ na raiz do repositório, calculada de forma
# relativa a ESTE arquivo (Path(__file__)). Assim funciona em qualquer
# computador (Windows, Mac, Linux), sem caminho fixo de uma máquina específica.
caminhoExportarSQL = str(Path(__file__).resolve().parent.parent / "SQLDump")

# Função responsável por criar e retornar uma conexão
# com o servidor MySQL.
#
# O parâmetro "banco" é opcional:
# - Se um nome de banco for informado, a conexão será
#   criada já apontando para esse banco de dados.
# - Se nenhum banco for informado (None), a conexão
#   será criada apenas com o servidor MySQL, sem
#   selecionar um banco específico.
#
# Retorna um objeto do tipo Connection, que será
# utilizado para executar consultas SQL, inserir,
# alterar, excluir e consultar registros.
def obtConexao(
        banco: str | None = None
) -> pymysql.connections.Connection:

    # Cria uma conexão com o servidor MySQL utilizando
    # as configurações definidas anteriormente.
    conexao = pymysql.connect(

        # Endereço do servidor de banco de dados.
        host=host,

        # Usuário responsável pela autenticação.
        user=usuario,

        # Senha do usuário.
        password=senha,

        # Banco que será utilizado na conexão.
        # Caso nenhum banco seja informado,
        # a conexão será criada sem selecionar
        # um banco específico.
        database=banco if banco else None,

        # Define o conjunto de caracteres utilizado
        # para armazenar textos com acentos e caracteres especiais.
        charset='utf8mb4',

        # Faz com que as consultas retornem dicionários
        # em vez de tuplas.
        #Obs: Tupla é uma estrutura que guarda vários valores juntos, parecida com uma lista.
        cursorclass=pymysql.cursors.DictCursor,

        # As alterações só serão gravadas definitivamente
        # após a execução do comando commit().
        autocommit=False
    )

    # Retorna o objeto de conexão criado.
    return conexao