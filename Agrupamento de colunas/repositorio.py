
# Importa os tipos List e Optional do módulo typing.
#
# List:
# Utilizado para indicar que uma função retorna
# ou recebe uma lista de objetos.
#
# Exemplo:
# List[Venda]
#
# Optional:
# Indica que um valor pode ser do tipo informado
# ou ser None.
#
# Exemplo:
# Optional[Venda]
# (A função pode retornar um objeto Venda ou None.)
from typing import List, Optional


# Importa as classes date e datetime do módulo datetime.
#
# date:
# Representa apenas uma data (dia, mês e ano).
#
# Exemplo:
# date(2025, 6, 20)
#
# datetime:
# Representa data e hora.
#
# Exemplo:
# datetime.now()
#
# Neste projeto:
# - date é utilizado para armazenar a data da venda.
# - datetime é utilizado para gerar a data e hora
#   da exportação do arquivo SQL.
from datetime import date, datetime


# Importa o módulo os.
#
# Esse módulo permite manipular arquivos e pastas
# do sistema operacional.
#
# Neste projeto ele é utilizado para:
# - criar diretórios;
# - montar caminhos de arquivos;
# - salvar o arquivo de exportação (.sql).
import os


# Importa informações e funções responsáveis
# pela conexão com o banco de dados.
#
# obtConexao:
# Cria e retorna uma conexão com o MySQL.
#
# nomeBanco:
# Nome do banco de dados utilizado pela aplicação.
#
# caminhoExportarSQL:
# Pasta onde será salvo o arquivo de backup (.sql).
from configBanco import (
    obtConexao,
    nomeBanco,
    caminhoExportarSQL
)


# Importa a classe Venda.
#
# Essa classe representa um registro da tabela
# de vendas do banco de dados.
#
# Cada objeto Venda possui informações como:
# - id
# - nome do cliente
# - cidade
# - setor
# - produto
# - quantidade
# - preço unitário
# - valor total
# - data da venda
from modelos import Venda

class RepoVendas:

    # Método construtor da classe.
    #
    # É executado automaticamente quando um objeto
    # da classe RepoVendas é criado.
    #
    # Sua função é preparar o repositório para uso,
    # garantindo que o banco de dados exista e
    # inserindo registros iniciais caso a tabela
    # esteja vazia.
    def __init__(self):

        # Garante que o banco de dados e a tabela
        # de vendas existam antes da aplicação
        # começar a utilizá-los.
        #
        # Caso não existam, eles serão criados.
        self.garantirBancoEtabela()

        # Verifica se já existem registros na tabela.
        #
        # Caso esteja vazia, insere automaticamente
        # alguns dados de exemplo para facilitar
        # os testes da aplicação.
        self.inserirDadosSeVazio()

    # Garante que o banco de dados e a tabela de vendas
    # existam antes da aplicação começar a utilizá-los.
    #
    # Caso o banco ou a tabela ainda não existam,
    # eles serão criados automaticamente.


    def garantirBancoEtabela(self):

        # Cria uma conexão com o servidor MySQL.
        #
        # Nesta conexão ainda não é necessário
        # selecionar um banco de dados, pois ele
        # pode não existir.
        raizConexao = obtConexao()

        try:

            # Cria um cursor para executar comandos SQL.
            #
            # O "with" garante que o cursor será fechado
            # automaticamente ao final da execução.
            with raizConexao.cursor() as cursor:

                # Cria o banco de dados caso ele ainda
                # não exista.
                #
                # IF NOT EXISTS evita erro caso o banco
                # já tenha sido criado anteriormente.
                #
                # utf8mb4 permite armazenar acentos,
                # caracteres especiais e emojis.
                cursor.execute(
                    f"""
                    CREATE DATABASE IF NOT EXISTS {nomeBanco}
                    DEFAULT CHARACTER SET utf8mb4;
                    """
                )

            # Salva a criação do banco de dados.
            #
            # OBS: O correto aqui é commit().
            # connect() apenas cria uma conexão.
            raizConexao.commit()

        finally:

            # Fecha a conexão com o servidor,
            # liberando os recursos utilizados.
            raizConexao.close()

        # Agora que o banco existe, cria uma nova
        # conexão já apontando diretamente para ele.
        conexao = obtConexao(nomeBanco)

        try:

            # Cria um cursor para executar comandos SQL.
            with conexao.cursor() as cursor:

                # Cria a tabela Vendas caso ela
                # ainda não exista.
                #
                # A tabela armazenará todas as
                # informações das vendas cadastradas
                # pela aplicação.
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS vendas (

                        -- Identificador único da venda.
                        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,

                        -- Nome do cliente.
                        nomeCliente VARCHAR(100) NOT NULL,

                        -- Valor total da venda.
                        total DECIMAL(12,2) NOT NULL,

                        -- Cidade onde a venda foi realizada.
                        cidade VARCHAR(80) NOT NULL,

                        -- Setor da empresa.
                        setor VARCHAR(60) NOT NULL,

                        -- Produto vendido.
                        produto VARCHAR(100) NOT NULL,

                        -- Quantidade vendida.
                        quantidade INT NOT NULL,

                        -- Valor de uma unidade do produto.
                        precoUnitario DECIMAL(12,2) NOT NULL,

                        -- Data em que a venda foi realizada.
                        dataVenda DATE NOT NULL,

                        -- Cria um índice para acelerar
                        -- pesquisas pelo nome do cliente.
                        INDEX indexCliente (nomeCliente),

                        -- Cria um índice para acelerar
                        -- pesquisas pela data da venda.
                        INDEX indexDataVenda (dataVenda)

                    )

                    -- Define o mecanismo de armazenamento
                    -- utilizado pela tabela.
                    ENGINE = InnoDB

                    -- Define o conjunto de caracteres
                    -- utilizado para armazenar textos.
                    DEFAULT CHARACTER SET utf8mb4;
                    """
                )

            # Salva definitivamente a criação da tabela.
            conexao.commit()

        finally:

            # Fecha a conexão com o banco de dados.
            conexao.close()

    # Verifica se a tabela de vendas já possui registros.
    #
    # Caso a tabela esteja vazia, serão inseridos
    # automaticamente dados de exemplo para facilitar
    # os testes da aplicação.
    #
    # Se já existirem registros, nenhuma inserção
    # será realizada, evitando a duplicação dos dados.
    def inserirDadosSeVazio(self) -> None:

        # Chama o método obtQntd(), que retorna a
        # quantidade de registros existentes na tabela.
        #
        # Se esse valor for maior que zero, significa
        # que a tabela já possui dados cadastrados.
        if self.obtQntd() > 0:
            # Encerra a função imediatamente.
            #
            # Como já existem registros, não é
            # necessário inserir os dados de exemplo.
            return

        dados = [
            # Empresa Alpha SA — duas vendas em São Paulo (setor Varejo)

            ("Alpha SA", 4500, "São Paulo", "Varejo", "Notebook 14", 5, 900.00, date(year=2025, month=1, day=10)),

            ("Alpha SA", 2100, "São Paulo", "Varejo", "Mouse sem fio", 30, 70.00, date(year=2025, month=1, day=12)),

            # Empresa Beta Ltda — duas vendas no Rio de Janeiro (setor Serviços)

            ("Beta Ltda", 7800, "Rio de Janeiro", "Serviços", "Servidor Torre", 2, 3900.00, date(year=2025, month=2, day=3)),

            ("Beta Ltda", 960, "Rio de Janeiro", "Serviços", "Teclado Mecânico", 12, 80.00, date(year=2025, month=2, day=5)),

            # Empresa Delta EPP — duas vendas em Curitiba (setor Atacado)

            ("Delta EPP", 6250, "Curitiba", "Atacado", "Monitor 27\"", 10, 625.00, date(year=2025, month=4, day=2)),

            ("Delta EPP", 480, "Curitiba", "Atacado", "Cabo HDMI 2m", 40, 12.00, date(year=2025, month=4, day=4)),

            # Empresa Gamma ME — duas vendas em Belo Horizonte (setor Indústria)

            ("Gamma ME", 3200, "Belo Horizonte", "Indústria", "Impressora Laser", 4, 800.00, date(year=2025, month= 3,day=15)),

            ("Gamma ME", 1540, "Belo Horizonte", "Indústria", "HD Externo 1TB", 14, 110.00, date(year=2025, month=3, day=22)),

            # Empresa Omega SA — duas vendas em Porto Alegre (setor Educação)

            ("Omega SA", 10350, "Porto Alegre", "Educação", "Chromebook", 15, 690.00, date(year=2025, month=4, day=18)),

            ("Omega SA", 2750, "Porto Alegre", "Educação", "Headset USB", 25, 110.00, date(year=2025, month=4, day=19)),

            # Empresa Sigma ME — duas vendas em Salvador (setor Saúde)

            ("Sigma ME", 4200, "Salvador", "Saúde", "Desktop Slim", 6, 700.00, date(year=2025, month=5, day=8)),

            ("Sigma ME", 1620, "Salvador", "Saúde", "Webcam HD", 18, 90.00, date(year=2025, month=5, day=12))
        ]

        # Cria uma conexão com o banco de dados.
        #
        # Como os dados serão inseridos na tabela
        # "vendas", é necessário conectar ao banco
        # onde essa tabela está armazenada.

        conn = obtConexao(nomeBanco)

        try:

            # Cria um cursor para executar comandos SQL.
            #
            # O "with" garante que o cursor será fechado
            # automaticamente ao final da execução.
            with conn.cursor() as cursor:

                # Insere vários registros de uma única vez
                # utilizando o comando INSERT.
                #
                # executemany() é utilizado quando desejamos
                # executar o mesmo comando SQL diversas vezes,
                # alterando apenas os valores.
                #
                # Em vez de inserir uma venda por vez,
                # ele percorre automaticamente a lista
                # "dados" e cadastra todas as vendas.
                cursor.executemany(
                    """
                    INSERT INTO vendas
                    (
                        nomeCliente,
                        total,
                        cidade,
                        setor,
                        produto,
                        quantidade,
                        precoUnitario,
                        dataVenda
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    dados
                )

            # Confirma definitivamente as inserções
            # realizadas no banco de dados.
            #
            # Sem o commit(), os registros podem não
            # ser gravados permanentemente.
            conn.commit()

        finally:

            # Fecha a conexão com o banco de dados,
            # liberando os recursos utilizados.
            conn.close()

        # Gera automaticamente um arquivo de backup
        # (.sql) contendo os registros da tabela.
        #
        # Esse arquivo poderá ser utilizado para
        # restaurar os dados futuramente, se necessário.
        self.exportarDumpSQL()

    # Retorna a quantidade de registros existentes
    # na tabela de vendas.
    #
    # Essa informação é utilizada para verificar,
    # por exemplo, se a tabela está vazia antes
    # de inserir os dados de exemplo.
    #
    # Retorno:
    # int -> quantidade de vendas cadastradas.
    def obtQntd(self) -> int:

        # Cria uma conexão com o banco de dados.
        conn = obtConexao(nomeBanco)

        try:

            # Cria um cursor para executar comandos SQL.
            #
            # O "with" garante que o cursor será fechado
            # automaticamente ao final da execução.
            with conn.cursor() as cursor:

                # Executa uma consulta SQL que conta
                # quantos registros existem na tabela "vendas".
                #
                # COUNT(*) conta todas as linhas da tabela.
                #
                # AS total cria um apelido (alias) para o
                # resultado da contagem, facilitando o acesso.
                cursor.execute(
                    "SELECT COUNT(*) AS total FROM vendas"
                )

                # Obtém o resultado da consulta.
                #
                # Como COUNT() sempre retorna apenas uma linha,
                # utiliza-se fetchone().
                row = cursor.fetchone()

                # Retorna o valor da contagem convertido
                # para inteiro.
                #
                # row["total"] acessa o valor retornado
                # pelo alias "total".
                #
                # Caso, por algum motivo, nenhuma linha
                # seja retornada, devolve 0.
                return int(row["total"]) if row else 0

        finally:

            # Fecha a conexão com o banco de dados,
            # liberando os recursos utilizados.
            conn.close()

    # Retorna uma lista contendo todas as vendas
    # cadastradas no banco de dados.
    #
    # Retorno:
    # List[Venda] -> lista de objetos da classe Venda.
    def listarTodosDados(self) -> List[Venda]:

        # Cria uma conexão com o banco de dados.
        conn = obtConexao(nomeBanco)

        try:

            # Cria um cursor para executar comandos SQL.
            #
            # O "with" garante que o cursor será fechado
            # automaticamente ao final da execução.
            with conn.cursor() as cursor:

                # Executa uma consulta SQL para buscar
                # todos os registros da tabela "vendas".
                #
                # SELECT define quais colunas serão retornadas.
                #
                # ORDER BY organiza os resultados primeiro
                # pelo nome do cliente, depois pela data da
                # venda e, por último, pelo id.
                cursor.execute(
                    """
                    SELECT
                        id,
                        nomeCliente,
                        total,
                        cidade,
                        setor,
                        produto,
                        quantidade,
                        precoUnitario,
                        dataVenda
                    FROM vendas
                    ORDER BY nomeCliente, dataVenda, id;
                    """
                )

                # Recupera todos os registros encontrados
                # pela consulta.
                #
                # fetchall() retorna uma lista contendo
                # todas as linhas retornadas pelo SELECT.
                rows = cursor.fetchall()

                # Percorre cada registro retornado pelo banco
                # e cria um objeto da classe Venda.
                #
                # Dessa forma, em vez de trabalhar com
                # dicionários retornados pelo MySQL,
                # a aplicação passa a trabalhar com objetos,
                # facilitando a leitura e a manutenção
                # do código.
                return [

                    Venda(

                        # Converte o id para inteiro.
                        id=int(row["id"]),

                        # Nome do cliente.
                        nomeCliente=row["nomeCliente"],

                        # Valor total da venda.
                        total=float(row["total"]),

                        # Cidade da venda.
                        cidade=row["cidade"],

                        # Setor da venda.
                        setor=row["setor"],

                        # Produto vendido.
                        produto=row["produto"],

                        # Quantidade vendida.
                        quantidade=int(row["quantidade"]),

                        # Preço unitário do produto.
                        precoUnitario=float(row["precoUnitario"]),

                        # Data em que a venda foi realizada.
                        dataVenda=row["dataVenda"]

                    )

                    # Repete esse processo para cada linha
                    # retornada pela consulta SQL.
                    for row in rows

                ]

        finally:

            # Fecha a conexão com o banco de dados.
            conn.close()

    # Procura e retorna uma venda específica
    # utilizando o seu identificador (ID).
    #
    # Parâmetro:
    # idVenda -> ID da venda que será pesquisada.
    #
    # Retorno:
    # Venda -> caso a venda seja encontrada.
    # None  -> caso não exista uma venda com esse ID.
    def obtPorId(self, idVenda: int) -> Optional[Venda]:

        # Cria uma conexão com o banco de dados.
        conn = obtConexao(nomeBanco)

        try:

            # Cria um cursor para executar comandos SQL.
            #
            # O "with" garante que o cursor seja fechado
            # automaticamente ao final da execução.
            with conn.cursor() as cursor:

                # Executa uma consulta SQL procurando
                # apenas a venda cujo ID seja igual
                # ao informado pelo usuário.
                #
                # O "%s" funciona como um parâmetro,
                # evitando SQL Injection e permitindo
                # que o valor seja inserido com segurança.
                cursor.execute(
                    """
                    SELECT
                        id,
                        nomeCliente,
                        total,
                        cidade,
                        setor,
                        produto,
                        quantidade,
                        precoUnitario,
                        dataVenda
                    FROM vendas
                    WHERE id = %s;
                    """,
                    (idVenda,)
                )

                # Recupera apenas uma linha da consulta,
                # pois o ID é único e somente uma venda
                # poderá ser encontrada.
                line = cursor.fetchone()

                # Verifica se nenhuma venda foi encontrada.
                #
                # Se line for None, significa que não existe
                # um registro com esse ID no banco.
                if not line:
                    return None

                # Cria e retorna um objeto da classe Venda
                # contendo os dados retornados pelo banco.
                return Venda(

                    id=int(line["id"]),

                    nomeCliente=line["nomeCliente"],

                    total=float(line["total"]),

                    cidade=line["cidade"],

                    setor=line["setor"],

                    produto=line["produto"],

                    quantidade=int(line["quantidade"]),

                    precoUnitario=float(line["precoUnitario"]),

                    dataVenda=line["dataVenda"]

                )

        finally:

            # Fecha a conexão com o banco de dados,
            # liberando os recursos utilizados.
            conn.close()

    # Insere uma nova venda no banco de dados.
    #
    # Parâmetros:
    # cliente -> nome do cliente.
    # cidade -> cidade onde a venda foi realizada.
    # setor -> setor da empresa.
    # produto -> nome do produto vendido.
    # quantidade -> quantidade de produtos vendidos.
    # precoUnitario -> preço de uma unidade do produto.
    # dataVenda -> data em que a venda foi realizada.
    #
    # Retorno:
    # int -> ID da venda recém-cadastrada.
    def inserirVenda(
            self,
            cliente: str,
            cidade: str,
            setor: str,
            produto: str,
            quantidade: int,
            precoUnitario: float,
            dataVenda: date
    ) -> int:

        # Calcula o valor total da venda.
        #
        # O total é obtido multiplicando a quantidade
        # pelo preço unitário.
        #
        # round(..., 2) arredonda o resultado para
        # duas casas decimais.
        total = round(quantidade * precoUnitario, 2)

        # Cria uma conexão com o banco de dados.
        conn = obtConexao(nomeBanco)

        try:

            # Cria um cursor para executar comandos SQL.
            #
            # O "with" garante que o cursor seja fechado
            # automaticamente ao final da execução.
            with conn.cursor() as cursor:

                # Executa um comando INSERT para cadastrar
                # uma nova venda na tabela.
                #
                # Os valores informados pelo usuário são
                # enviados para o banco utilizando parâmetros
                # (%s), tornando a consulta mais segura.
                cursor.execute(
                    """
                    INSERT INTO vendas
                    (
                        nomeCliente,
                        total,
                        cidade,
                        setor,
                        produto,
                        quantidade,
                        precoUnitario,
                        dataVenda
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    """,
                    (
                        cliente,
                        total,
                        cidade,
                        setor,
                        produto,
                        quantidade,
                        precoUnitario,
                        dataVenda
                    )
                )

                # Obtém o ID gerado automaticamente
                # pelo MySQL para o registro recém-inserido.
                novoId = cursor.lastrowid

            # Confirma definitivamente a inserção
            # da venda no banco de dados.
            conn.commit()

        finally:

            # Fecha a conexão com o banco de dados.
            conn.close()

        # Atualiza o arquivo de backup (.sql)
        # após a inclusão da nova venda.
        self.exportarDumpSQL()

        # Retorna o ID da venda cadastrada.
        return novoId

    # Atualiza os dados de uma venda já existente
    # no banco de dados.
    #
    # Parâmetros:
    # idVenda -> identificador da venda que será alterada.
    # nomeCliente -> novo nome do cliente.
    # cidade -> nova cidade da venda.
    # setor -> novo setor da venda.
    # produto -> novo produto vendido.
    # quantidade -> nova quantidade vendida.
    # precoUnitario -> novo preço unitário do produto.
    # dataVenda -> nova data da venda.
    #
    # Retorno:
    # None, pois a função apenas altera os dados
    # da venda no banco de dados.
    def atualizarVenda(
            self,
            idVenda: int,
            nomeCliente: str,
            cidade: str,
            setor: str,
            produto: str,
            quantidade: int,
            precoUnitario: float,
            dataVenda: date
    ) -> None:

        # Recalcula o valor total da venda.
        #
        # Caso a quantidade ou o preço unitário
        # tenham sido alterados, o total também
        # precisa ser atualizado.
        total = round(quantidade * precoUnitario, 2)

        # Cria uma conexão com o banco de dados.
        conn = obtConexao(nomeBanco)

        try:

            # Cria um cursor para executar comandos SQL.
            #
            # O "with" garante que o cursor seja fechado
            # automaticamente ao final da execução.
            with conn.cursor() as cursor:

                # Executa um comando UPDATE para alterar
                # os dados da venda cujo ID foi informado.
                #
                # Apenas o registro com esse ID será
                # modificado.
                cursor.execute(
                    """
                    UPDATE vendas
                    SET
                        nomeCliente = %s,
                        total = %s,
                        cidade = %s,
                        setor = %s,
                        produto = %s,
                        quantidade = %s,
                        precoUnitario = %s,
                        dataVenda = %s
                    WHERE id = %s;
                    """,
                    (
                        nomeCliente,
                        total,
                        cidade,
                        setor,
                        produto,
                        quantidade,
                        precoUnitario,
                        dataVenda.isoformat(),
                        idVenda
                    )
                )

            # Confirma definitivamente as alterações
            # realizadas no banco de dados.
            conn.commit()

        finally:

            # Fecha a conexão com o banco de dados.
            conn.close()

        # Atualiza o arquivo de backup (.sql)
        # para manter uma cópia da versão mais
        # recente do banco de dados.
        self.exportarDumpSQL()

    # Exclui uma venda do banco de dados utilizando
    # o seu identificador (ID).
    #
    # Parâmetro:
    # idVenda -> ID da venda que será removida.
    #
    # Retorno:
    # None, pois a função apenas remove o registro
    # do banco de dados.
    def excluirVenda(self, idVenda: int) -> None:

        # Cria uma conexão com o banco de dados.
        conn = obtConexao(nomeBanco)

        try:

            # Cria um cursor para executar comandos SQL.
            #
            # O "with" garante que o cursor seja fechado
            # automaticamente ao final da execução.
            with conn.cursor() as cursor:

                # Executa um comando DELETE para remover
                # da tabela "vendas" o registro cujo
                # ID seja igual ao informado.
                #
                # O parâmetro %s recebe o valor de
                # idVenda de forma segura, evitando
                # SQL Injection.
                cursor.execute(
                    "DELETE FROM vendas WHERE id = %s;",
                    (idVenda,)
                )

            # Confirma definitivamente a exclusão
            # do registro no banco de dados.
            conn.commit()

        finally:

            # Fecha a conexão com o banco de dados,
            # liberando os recursos utilizados.
            conn.close()

        # Atualiza o arquivo de backup (.sql),
        # refletindo a exclusão realizada no banco.
        self.exportarDumpSQL()

    # Exporta um arquivo de backup (.sql) contendo
    # toda a estrutura e os dados da tabela "vendas".
    #
    # Esse arquivo pode ser utilizado posteriormente
    # para restaurar o banco de dados.
    #
    # Retorno:
    # None.


    def exportarDumpSQL(self) -> None:
        # Cria a pasta onde o arquivo SQL será salvo.
        #
        # exist_ok=True evita erro caso a pasta
        # já exista.
        os.makedirs(caminhoExportarSQL, exist_ok=True)

        # Nome do arquivo principal do backup.
        base = "agrupamentoTabelaDBDumpSQL"

        # Monta o caminho completo onde o arquivo
        # principal será salvo.
        pPrincipal = os.path.join(
            caminhoExportarSQL,
            base
        )

        # Obtém a data e hora atuais.
        #
        # Essas informações serão utilizadas para
        # gerar um nome diferente para cada backup.
        carimbo = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Cria o caminho do arquivo de versão,
        # adicionando a data e hora ao nome.
        #
        # Assim cada exportação gera um novo arquivo,
        # preservando os backups anteriores.
        pVersao = os.path.join(
            caminhoExportarSQL,
            f"agrupamentoTabelaDBDump{carimbo}.sql"
        )

        # Cria uma conexão com o banco de dados.
        conn = obtConexao(nomeBanco)

        try:

            # Cria um cursor para executar comandos SQL.
            with conn.cursor() as cursor:

                # Busca todas as vendas cadastradas
                # no banco de dados.
                #
                # Os registros serão utilizados para
                # montar os comandos INSERT do backup.
                cursor.execute(
                    """
                    SELECT
                        id,
                        nomeCliente,
                        total,
                        cidade,
                        setor,
                        produto,
                        quantidade,
                        precoUnitario,
                        dataVenda
                    FROM vendas
                    ORDER BY id
                    """
                )

                # Recupera todos os registros retornados
                # pela consulta SQL.
                linhas = cursor.fetchall()

        finally:

            # Fecha a conexão com o banco de dados.
            conn.close()

        # Cria uma lista que armazenará todas
        # as linhas que formarão o arquivo SQL.
        #
        # A anotação List[str] informa que essa lista
        # armazenará apenas textos (strings)
        partes: List[str] = []

        # Adiciona um comentário contendo a data
        # e hora em que o backup foi gerado.
        partes.append(
            f"-- Dump gerado em {datetime.now().isoformat(sep=' ', timespec='seconds')} --"
        )

        # Define o conjunto de caracteres utilizado.
        partes.append("SET NAMES utf8mb4;")

        # Comando responsável por criar o banco
        # caso ele ainda não exista.
        partes.append(
            f"CREATE DATABASE IF NOT EXISTS {nomeBanco} DEFAULT CHARACTER SET utf8mb4;"
        )

        # Seleciona o banco que será utilizado.
        partes.append(
            f"USE {nomeBanco};"
        )

        partes.append("")

        # Remove a tabela caso ela já exista,
        # permitindo recriá-la do zero.
        partes.append(
            "DROP TABLE IF EXISTS vendas;"
        )

        # Adiciona o comando responsável por
        # recriar a tabela de vendas.
        partes.append(
            """
            CREATE TABLE vendas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nomeCliente VARCHAR(100) NOT NULL,
                total DECIMAL(12,2) NOT NULL,
                cidade VARCHAR(80) NOT NULL,
                setor VARCHAR(60) NOT NULL,
                produto VARCHAR(100) NOT NULL,
                quantidade INT NOT NULL,
                precoUnitario DECIMAL(12,2) NOT NULL,
                dataVenda DATE NOT NULL,
                INDEX indexCliente (nomeCliente),
                INDEX indexDataVenda (dataVenda)
            ) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4;
            """
        )

        partes.append("")

        # Verifica se existem registros na tabela.
        if linhas:

            # Inicia o comando INSERT que será utilizado
            # para recriar todos os registros do banco.
            partes.append(
                """
                INSERT INTO vendas
                (
                    nomeCliente,
                    total,
                    cidade,
                    setor,
                    produto,
                    quantidade,
                    precoUnitario,
                    dataVenda
                )
                VALUES
                """
            )

            # Lista utilizada para armazenar
            # os valores de cada venda.
            valores = []

            # Percorre todos os registros retornados
            # pela consulta realizada no banco de dados.
            #
            # A cada repetição, a variável "linha"
            # representa uma venda diferente.
            for linha in linhas:
                # Escapa a aspa simples DUPLICANDO-A ('' em vez de ').
                #
                # Por quê? No SQL, textos ficam entre aspas simples:
                # '...'. Se o próprio texto tiver uma aspa (ex: Sant'Ana),
                # ela encerraria a string no lugar errado e quebraria o
                # comando. A regra do SQL é: para representar UMA aspa
                # dentro do texto, escrevemos DUAS ('').
                #
                # Exemplo: Sant'Ana  ->  'Sant''Ana'  (o banco lê Sant'Ana)
                #
                # OBS: NÃO trocamos a aspa por aspa dupla ("), pois isso
                # mudaria o dado em si (corromperia o nome no backup).
                nomeCliente = linha["nomeCliente"].replace("'", "''")

                # Mesmo escape para a cidade.
                cidade = linha["cidade"].replace("'", "''")

                # Mesmo escape para o setor.
                setor = linha["setor"].replace("'", "''")

                # Mesmo escape para o produto.
                produto = linha["produto"].replace("'", "''")

                # Monta uma linha do comando INSERT contendo
                # os dados da venda atual.
                #
                # Essa linha será adicionada à lista "valores"
                # e fará parte do arquivo de backup (.sql).
                valores.append(

                    f"({int(linha['id'])}, "
                    f"'{nomeCliente}', "
                    f"{float(linha['total']):.2f}, "
                    f"'{cidade}', "
                    f"'{setor}', "
                    f"'{produto}', "
                    f"{int(linha['quantidade'])}, "
                    f"{float(linha['precoUnitario']):.2f}, "
                    f"'{linha['dataVenda'].isoformat()}')"

                )

            # Junta todos os comandos INSERT em um único texto,
            # separando cada registro por vírgula e quebra de linha.
            #
            # Ao final, adiciona ";" para indicar o término
            # do comando SQL.
            partes.append(
                ",\n".join(valores) + ";"
            )

        # Caso a tabela não possua registros,
        # adiciona um comentário informando
        # que ela está vazia.
        else:
            partes.append("-- Tabela vazia --")

        # Junta todas as linhas armazenadas na lista
        # "partes", formando o conteúdo completo
        # do arquivo SQL.
        texto = "\n".join(partes)

        # Cria (ou sobrescreve) o arquivo principal
        # contendo o backup do banco de dados.
        with open(
                pPrincipal,
                "w",
                encoding="utf-8"
        ) as f:

            # Escreve todo o conteúdo do backup
            # no arquivo.
            f.write(texto)

        # Cria uma segunda cópia do backup,
        # utilizando a data e hora no nome
        # do arquivo para manter um histórico
        # das exportações realizadas.
        with open(
                pVersao,
                "w",
                encoding="utf-8"
        ) as f:

            # Escreve o mesmo conteúdo no arquivo
            # de versão.
            f.write(texto)