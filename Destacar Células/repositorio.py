# Importa tipos utilizados para criar
# anotações de tipo (type hints).
#
# List:
# Indica que uma variável ou retorno
# será uma lista de objetos.
#
# Optional:
# Indica que um valor pode ser de um
# determinado tipo ou None.
from typing import List, Optional

# Importa a classe utilizada para
# representar datas.
from datetime import date

# Importa a função responsável por criar
# conexões com o banco de dados e o nome
# do banco utilizado pela aplicação.
from configBanco import conectar, nomeDoBanco

# Importa o modelo Produto.
#
# Essa classe será utilizada para criar
# objetos Produto a partir dos registros
# encontrados no banco de dados.
from modelos import Produto


# Classe responsável por manipular os
# produtos no banco de dados.
#
# Ela contém os métodos responsáveis
# por cadastrar, listar, atualizar,
# excluir e consultar produtos.
class RepoProdutos:

    # self representa o próprio objeto
    # da classe.
    #
    # Ele permite acessar os atributos
    # e métodos pertencentes ao objeto
    # atual.
    #
    # Exemplo:
    #
    # self.garantiaDeBancoEtabela()
    # self.inserirDadosSeVazio()

    # Método construtor.
    #
    # É executado automaticamente sempre
    # que um objeto RepoProdutos é criado.
    # Exemplo:
    # Em appDestacarCelulas.py:
    #
    # self.repo = RepoProdutos()
    #
    # Nesse momento, o Python executa
    # automaticamente o método __init__().
    #
    # Inicializa o banco de dados da
    # aplicação.
    def __init__(self):

        # Cria o banco e a tabela,
        # caso ainda não existam.
        self.garantiaDeBancoEtabela()

        # Insere os dados iniciais,
        # caso a tabela esteja vazia.
        self.inserirDadosSeVazio()

    # Garante que o banco de dados e a tabela
    # da aplicação existam.
    #
    # Caso ainda não existam, eles serão criados.
    def garantiaDeBancoEtabela(self) -> None:

        # Cria uma conexão com o servidor MySQL,
        # sem selecionar um banco de dados.
        #
        # Isso é necessário porque o banco
        # pode ainda não existir.
        conexaoRoot = conectar()

        try:

            # Cria um cursor para executar
            # comandos SQL.
            with conexaoRoot.cursor() as cursor:

                # Cria o banco de dados caso
                # ele ainda não exista.
                cursor.execute(
                    f"CREATE DATABASE IF NOT EXISTS {nomeDoBanco} "
                    "DEFAULT CHARACTER SET utf8mb4;"
                )

                # Salva a criação do banco.
                conexaoRoot.commit()

        # Fecha a conexão, mesmo que ocorra erro.
        finally:
            conexaoRoot.close()

        # Agora cria uma conexão já utilizando
        # o banco de dados criado.
        conexaoRoot = conectar(nomeDoBanco)

        try:

            # Cria um cursor para executar
            # comandos SQL.
            with conexaoRoot.cursor() as cursor:

                # Cria a tabela produtos caso
                # ela ainda não exista.
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS produtos(
                        idProduto INT AUTO_INCREMENT PRIMARY KEY,
                        categoriaProduto VARCHAR(60) NOT NULL,
                        nomeProduto VARCHAR(120) NOT NULL,
                        precoProduto DECIMAL(12,2) NOT NULL,
                        estoque INT NOT NULL,
                        dataProduto DATE NOT NULL,

                        INDEX idxCategoria(categoriaProduto),
                        INDEX idxNome(nomeProduto)

                    ) ENGINE=InnoDB
                    DEFAULT CHARACTER SET utf8mb4;
                    """
                )

            # Salva a criação da tabela.
            conexaoRoot.commit()

        # Fecha a conexão com o banco.
        finally:
            conexaoRoot.close()

    # Insere os produtos iniciais no banco
    # de dados caso a tabela esteja vazia.
    def insercaoDeDadosSeVazio(self):

        # Verifica a quantidade de registros
        # existentes na tabela.
        #
        # Se já existir pelo menos um produto,
        # não é necessário inserir os dados
        # iniciais.
        if self.obterQuantidade() > 0:
            return

        # Lista contendo os produtos que serão
        # inseridos no banco de dados.
        #
        # Cada tupla representa um produto.
        dados = [
            ("Informática", "Notebook 14\"", 3500.00, 8, date(year=2025, month=1, day=10)),
            ("Informática", "Mouse sem fio", 70.00, 40, date(year=2025, month=1, day=12)),
            ("Informática", "Teclado mecânico", 80.00, 20, date(year=2025, month=2, day=5)),
            ("Periféricos", "Headset USB", 110.00, 25, date(year=2025, month=4, day=19)),
            ("Periféricos", "Webcam HD", 90.00, 14, date(year=2025, month=5, day=12)),
            ("Monitores", "Monitor 27\"", 625.00, 10, date(year=2025, month=4, day=2)),
            ("Armazen.", "HD Externo 1TB", 110.00, 18, date(year=2025, month=3, day=22)),
            ("Impressão", "Impressora Laser", 800.00, 4, date(year=2025, month=3, day=15)),
            ("Computação", "Chromebook", 690.00, 15, date(year=2025, month=4, day=18)),
            ("Desktops", "Desktop Slim", 700.00, 6, date(year=2025, month=5, day=8)),
        ]

        # Cria uma conexão com o banco
        # de dados da aplicação.
        conexaoRoot = conectar(nomeDoBanco)

        try:

            # Cria um cursor para executar
            # comandos SQL.
            with conexaoRoot.cursor() as cursor:

                # executemany() executa o mesmo
                # comando SQL várias vezes.
                #
                # Cada tupla da lista "dados"
                # será utilizada para inserir
                # um produto diferente.
                cursor.executemany(
                    "INSERT INTO produtos (categoriaProduto, nomeProduto, precoProduto,"
                    " estoque, dataProduto) VALUES (%s, %s, %s, %s, %s)",
                    dados
                )

            # Salva todas as inserções
            # realizadas no banco.
            conexaoRoot.commit()

        # Fecha a conexão, mesmo que
        # ocorra algum erro.
        finally:
            conexaoRoot.close()

    # Retorna a quantidade de registros
    # existentes na tabela produtos.
    def obterQuantidade(self) -> int:

        # Cria uma conexão com o banco
        # de dados da aplicação.
        conexaoRoot = conectar(nomeDoBanco)

        try:

            # Cria um cursor para executar
            # comandos SQL.
            with conexaoRoot.cursor() as cursor:

                # COUNT(*) conta quantos
                # registros existem na tabela.
                cursor.execute(
                    "SELECT COUNT(*) AS total FROM produtos"
                )

                # Obtém a primeira (e única)
                # linha retornada pela consulta.
                linha = cursor.fetchone()

                # Retorna a quantidade encontrada.
                #
                # Se nenhuma linha for retornada,
                # retorna 0.
                return int(linha["total"]) if linha else 0

        # Fecha a conexão com o banco,
        # mesmo que ocorra algum erro.
        finally:
            conexaoRoot.close()

    # Lista todos os produtos cadastrados.
    #
    # Caso um texto seja informado, realiza
    # uma pesquisa filtrando pela categoria
    # ou pelo nome do produto.
    def listarTudo(self, texto: str | None = None) -> list[Produto]:

        # Consulta SQL inicial.
        #
        # Seleciona todas as colunas que serão
        # utilizadas para criar os objetos Produto.
        querySQL = (
            "SELECT idProduto, categoriaProduto, nomeProduto, "
            "precoProduto, estoque, dataProduto FROM produtos "
        )

        # Lista que armazenará os parâmetros
        # utilizados na consulta SQL.
        #
        # Ela ficará vazia caso não exista filtro.
        parametros: list = []

        # Verifica se o usuário informou algum
        # texto para pesquisa.
        if texto and texto.strip():
            # Adiciona um filtro à consulta.
            #
            # O operador LIKE permite localizar
            # registros que contenham o texto
            # informado pelo usuário.
            querySQL += (
                "WHERE categoriaProduto LIKE %s "
                "OR nomeProduto LIKE %s "
            )

            # Adiciona o caractere curinga (%)
            # antes e depois do texto.
            #
            # Exemplo:
            # "mouse" -> "%mouse%"
            #
            # Dessa forma serão encontrados
            # produtos que contenham essa palavra.
            like = f"%{texto.strip()}%"

            # Adiciona os dois parâmetros da
            # consulta SQL (categoria e nome).
            parametros.extend([like, like])

        # Ordena os registros antes de retorná-los.
        querySQL += (
            "ORDER BY categoriaProduto, "
            "nomeProduto, idProduto;"
        )

        # Cria uma conexão com o banco de dados.
        conexaoRoot = conectar(nomeDoBanco)

        try:

            # Cria um cursor para executar
            # comandos SQL.
            with conexaoRoot.cursor() as cursor:

                # Executa a consulta SQL,
                # utilizando os parâmetros
                # informados (caso existam).
                cursor.execute(querySQL, parametros)

                # Obtém todos os registros
                # retornados pela consulta.
                linhas = cursor.fetchall()

                # Converte cada linha retornada
                # pelo banco em um objeto Produto.
                return [
                    Produto(
                        idProduto=int(linha["idProduto"]),
                        categoriaProduto=linha["categoriaProduto"],
                        nomeProduto=linha["nomeProduto"],
                        precoProduto=float(linha["precoProduto"]),
                        estoque=int(linha["estoque"]),
                        criadoEm=linha["criadoEm"]
                    )
                    for linha in linhas
                ]

        # Fecha a conexão com o banco,
        # mesmo que ocorra algum erro.
        finally:
            conexaoRoot.close()

    # Insere um novo produto no banco de dados.
    #
    # Retorna o ID gerado automaticamente
    # pelo MySQL para o novo registro.
    def inserirProduto(
            self,
            categoriaProd: str,
            nomeProd: str,
            precoProd: float,
            estoqueProd: int,
            dataProd: date
    ) -> int:

        # Cria uma conexão com o banco de dados.
        conexaoRoot = conectar(nomeDoBanco)

        try:

            # Cria um cursor para executar
            # comandos SQL.
            with conexaoRoot.cursor() as cursor:

                # Executa o comando INSERT,
                # adicionando um novo produto
                # na tabela.
                cursor.execute(
                    "INSERT INTO produtos "
                    "(categoriaProduto, nomeProduto, precoProduto, "
                    "estoque, dataProduto) "
                    "VALUES (%s, %s, %s, %s, %s)",

                    (
                        categoriaProd,
                        nomeProd,
                        precoProd,
                        estoqueProd,

                        # Converte a data para o
                        # formato aceito pelo MySQL
                        # (AAAA-MM-DD).
                        dataProd.isoformat()
                    )
                )

                # Obtém o ID gerado automaticamente
                # para o registro inserido.
                novoId = cursor.lastrowid

            # Salva a inserção no banco.
            conexaoRoot.commit()

            # Retorna o ID do novo produto.
            return int(novoId)

        # Fecha a conexão com o banco,
        # mesmo que ocorra algum erro.
        finally:
            conexaoRoot.close()

    # Atualiza os dados de um produto
    # já cadastrado no banco de dados.
    def atualizarProduto(
            self,
            idProd: int,
            categoriaProduto: str,
            nomeProduto: str,
            precoProduto: float,
            estoque: int,
            dataProd: date
    ) -> None:

        # Cria uma conexão com o banco de dados.
        conexaoRoot = conectar(nomeDoBanco)

        try:

            # Cria um cursor para executar
            # comandos SQL.
            with conexaoRoot.cursor() as cursor:

                # Atualiza os dados do produto
                # correspondente ao ID informado.
                cursor.execute(
                    """
                    UPDATE produtos
                    SET categoriaProduto = %s,
                        nomeProduto = %s,
                        precoProduto = %s,
                        estoque = %s,
                        criadoEm = %s
                    WHERE idProduto = %s
                    """,
                    (
                        categoriaProduto,
                        nomeProduto,
                        precoProduto,
                        estoque,

                        # Converte a data para
                        # o formato AAAA-MM-DD.
                        dataProd.isoformat(),

                        idProd
                    )
                )

            # Salva as alterações realizadas
            # no banco de dados.
            conexaoRoot.commit()

        # Fecha a conexão, mesmo que
        # ocorra algum erro.
        finally:
            conexaoRoot.close()

    # Exclui um produto do banco de dados
    # utilizando o ID informado.
    def excluirProduto(self, idProd: int) -> None:

        # Cria uma conexão com o banco de dados.
        conexaoRoot = conectar(nomeDoBanco)

        try:

            # Cria um cursor para executar
            # comandos SQL.
            with conexaoRoot.cursor() as cursor:

                # Executa o comando DELETE,
                # removendo o produto cujo
                # ID foi informado.
                cursor.execute(
                    "DELETE FROM produtos WHERE idProduto = %s",
                    (idProd,)
                )

            # Salva a exclusão no banco de dados.
            conexaoRoot.commit()

        # Fecha a conexão com o banco,
        # mesmo que ocorra algum erro.
        finally:
            conexaoRoot.close()

    # Procura um produto utilizando o ID informado.
    #
    # Se encontrar o produto, retorna um
    # objeto Produto.
    #
    # Caso contrário, retorna None.
    def obterProdutoPorId(self, idProd: int) -> Optional[Produto]:

        # Cria uma conexão com o banco de dados.
        conexaoRoot = conectar(nomeDoBanco)

        try:

            # Cria um cursor para executar
            # comandos SQL.
            with conexaoRoot.cursor() as cursor:

                # Procura um produto cujo ID
                # seja igual ao informado.
                cursor.execute(
                    "SELECT idProduto, categoriaProduto, nomeProduto, "
                    "precoProduto, estoque, dataProduto FROM produtos "
                    "WHERE idProduto = %s",
                    (idProd,)
                )

                # Obtém a primeira linha
                # retornada pela consulta.
                linha = cursor.fetchone()

                # Se nenhum produto foi encontrado,
                # retorna None.
                if not linha:
                    return None

                # Converte a linha retornada pelo
                # banco em um objeto Produto.
                return Produto(
                    idProduto=int(linha["idProduto"]),
                    categoriaProduto=linha["categoriaProduto"],
                    nomeProduto=linha["nomeProduto"],
                    precoProduto=float(linha["precoProduto"]),
                    estoque=int(linha["estoque"]),
                    dataProduto=linha["dataProduto"]
                )

        # Fecha a conexão com o banco,
        # mesmo que ocorra algum erro.
        finally:
            conexaoRoot.close()




