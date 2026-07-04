# Importa os tipos List e Optional da biblioteca typing.
# List é usado para indicar listas tipadas.
# Optional indica que um valor pode ser do tipo informado ou None.
from typing import List, Optional

# Importa classes para trabalhar com datas e horários.
# date representa apenas uma data.
# datetime representa data e hora completas.
from datetime import date, datetime

# Biblioteca utilizada para manipulação de arquivos e diretórios.
import os

# Importa o caminho onde os arquivos de backup SQL serão armazenados.
from configBanco import caminhoExportarSQL

# Importa a função responsável pela conexão com o banco
# e as configurações utilizadas na conexão.
from configBanco import (
    obterConexao,
    nomeBanco,
    host,
    porta,
    usuario,
    senha
)

# Importa a classe Evento, utilizada como modelo
# para representar os registros da tabela de eventos.
from modelos import Evento

# Classe responsável por realizar todas as operações
# de acesso e manipulação dos dados da tabela eventos.
class RepoEventos:
    # Metodo construtor da classe.
    # É executado automaticamente quando um objeto da classe é criado.
    # Garante a existência do banco/tabela e insere dados iniciais.
    def __init__(self):

       # Cria o banco e a tabela caso não existam.
       self.garantirBancoEtabela()

       # Insere registros iniciais caso a tabela esteja vazia.
       self.insertSeedSeVazio()

    # Método responsável por garantir que toda a estrutura
    # necessária para o funcionamento da aplicação exista.
    # Primeiro cria o banco de dados (caso ainda não exista)
    # e, em seguida, cria a tabela de eventos utilizada pelo sistema.
    def garantirBancoEtabela(self) -> None:
        # Abre uma conexão com o servidor MySQL sem selecionar
        # um banco específico. Isso permite criar o banco de dados
        # caso ele ainda não tenha sido criado.
        connRoot = obterConexao()

        try:

           # Cria um cursor para executar comandos SQL.
           with connRoot.cursor() as curs:

              # Executa o comando responsável por criar o banco
              # de dados caso ele ainda não exista no servidor.
              # O banco será criado utilizando a codificação utf8mb4,
              # que suporta caracteres especiais, acentos e emojis.
              curs.execute(
                f" CREATE DATABASE IF NOT EXISTS {nomeBanco} DEFAULT CHARACTER SET utf8mb4;"
              )

           # Confirma a execução do comando no banco.
           connRoot.commit()

        finally:

           # Fecha a conexão com o servidor,
           # liberando os recursos utilizados.
           connRoot.close()

        # Abre uma nova conexão, agora utilizando
        # o banco de dados criado anteriormente.
        conn = obterConexao(nomeBanco)

        try:
            # Cria um cursor para executar comandos SQL.
            with conn.cursor() as curs:

               # Cria a tabela "eventos" caso ela ainda não exista.
               # Estrutura da tabela:
               # - id: identificador único do evento
               # - descricao: descrição ou nome do evento
               # - dataEvento: data em que o evento ocorrerá
               # Também é criado um índice para otimizar
               # pesquisas realizadas pela data do evento.
               curs.execute(
                """
                CREATE TABLE IF NOT EXISTS eventos
                (
                    id
                    INT
                    AUTO_INCREMENT
                    PRIMARY
                    KEY,
                    descricao
                    VARCHAR
                (
                    200
                ) NOT NULL,
                    dataEvento DATE NOT NULL,
                    INDEX indexDataEvento
                (
                    dataEvento
                )
                    ) ENGINE InnoDB DEFAULT CHARACTER SET utf8mb4;
                """
                )

               # Confirma a criação da tabela.
               conn.commit()

        finally:

           # Fecha a conexão com o banco de dados.
           # Isso evita consumo desnecessário de recursos
           # e possíveis problemas com conexões abertas.
           conn.close()

    # Insere dados iniciais (seed) na tabela de eventos.
    # Esse método é executado durante a inicialização da aplicação
    # e tem como objetivo popular automaticamente o banco de dado
    # com registros de exemplo quando a tabela estiver vazia.
    # Os registros inseridos servem para testes, demonstrações
    # e validação das funcionalidades do sistema.

    def insertSeedSeVazio(self) -> None:

       # Verifica se já existem registros cadastrados na tabela.
       # Caso a quantidade de registros seja maior que zero,
       # significa que o banco já foi populado anteriormente
       # e não é necessário inserir os dados de exemplo novamente.
       if self.obterQuantidade() > 0:

        return

       # Lista contendo os eventos iniciais que serão inseridos
       # automaticamente na tabela eventos.
       # Cada item da lista é formado por:
       # - descrição do evento
       # - data do evento
       seed = [
            ("Workshop Excel Avançado", date(2024, 11, 15)),  # Treinamento avançado de Excel para equipe
            ("Implantação Power BI Loja A", date(year=2024, month=12, day=3)),  # Implantação do Power BI na Loja A
            ("Revisão Relatório Vendas Q4", date(year=2024, month=12, day=28)), # Revisão do relatório trimestral de vendas
            ("Virada de Ano - Planejamento 2030", date(year=2024, month=12, day=31)), # Planejamento estratégico para o novo ciclo

            ("Reunião Kickoff Projetos 2030", date(year=2030, month=1, day=6)),  # Reunião de início dos projetos do ano
            ("Entrega Dashboard Financeiro", date(year=2030, month=1, day=20)),  # Entrega do painel financeiro
            ("Treinamento Python p/ Dados", date(year=2030, month=2, day=10)),   # Curso de Python voltado para análise de dados
            ("Sprint BI - Sem. 1", date(year=2030, month=2, day=17)),  # Primeira sprint da equipe de Business Intelligence
            ("Sprint BI - Sem. 2", date(year=2030, month=2, day=24)),  # Segunda sprint da equipe de Business Intelligence

            ("Auditoria de Indicadores", date(year=2030, month=3, day=12)),  # Verificação dos indicadores e métricas do negócio
            ("Palestra: Boas Práticas SQL", date(year=2030, month=3, day=25)),  # Palestra técnica sobre SQL
            ("Fechamento Q1", date(year=2030, month=3, day=31)),  # Encerramento e consolidação do primeiro trimestre

            ("Oficina: Tkinter na Prática", date(year=2030, month=4, day=8)),
            # Oficina prática de desenvolvimento com Tkinter
            ("Atualização KPIs Comercial", date(year=2030, month=4, day=19)),  # Atualização dos indicadores comerciais
            ("Revisão Meta Trimestral", date(year=2030, month=4, day=30)),  # Revisão das metas do trimestre

            ("Entrega Relatório Semestral", date(year=2030, month=6, day=30)),  # Entrega de relatório de meio de ano
            ("Kickoff Campanha Black Friday", date(year=2030, month=9, day=1)),  # Início da campanha promocional
            ("Prévia Black Friday (Stress Test)", date(year=2030, month=10, day=15)),
            # Teste de carga antes da campanha
            ("Black Friday", date(year=2030, month=11, day=28)),  # Data principal do evento de vendas
            ("Pós-Mortem Black Friday", date(year=2030, month=12, day=5)),  # Análise dos resultados da campanha

            ("Onboarding Novos Analistas", date(year=2026, month=1, day=15)),   # Integração e treinamento de novos analistas
            ("Workshop: Modelagem de Dados", date(year=2026, month=2, day=4)),  # Workshop técnico sobre modelagem de dados
            ("Hackday Automação Relatórios", date(year=2026, month=3, day=10)), # Evento interno de inovação e automação

            ("Planejamento 2026", date(year=2025, month=12, day=20)),  # Planejamento estratégico para o próximo ano
       ]

       # Abre uma conexão com o banco de dados.
       conn = obterConexao(nomeBanco)

       try:
          # Cria um cursor para execução de comandos SQL.
          with conn.cursor() as curs:
             # Realiza a inserção de todos os registros da lista
             # utilizando executemany(), que executa a mesma instrução SQL várias vezes
             # de forma otimizada. Isso é mais eficiente do que executar vários INSERTs individuais.
             curs.executemany(
                "INSERT INTO eventos(descricao, dataEvento) VALUES (%s, %s)",
                [(d, dt.isoformat()) for d, dt in seed]
             )
          # Confirma todas as inserções realizadas.
          # Sem o commit(), os registros podem não ser gravados definitivamente no banco.
          conn.commit()
       finally:
          # Fecha a conexão independentemente de ocorrer erro ou não.
          # Isso evita desperdício de recursos e conexões abertas.
          conn.close()
       # Atualiza os arquivos de backup SQL após a inserção dos registros iniciais.
       # Dessa forma, o dump permanece sincronizado com # os dados atualmente armazenados[
       # no banco.
       self.exportarDumpSQL()

    # Método responsável por contar quantos registros existem
    # na tabela "eventos" do banco de dados
    # Retorna um número inteiro contendo a quantidade
    # total de eventos cadastrados.
    def obterQuantidade(self) -> int:

        # Abre uma conexão com o banco de dados informado.
        conn = obterConexao(nomeBanco)

        try:

            # Cria um cursor, que é o objeto utilizado
            # para executar comandos SQL no banco.
            with conn.cursor() as curs:

                # Executa uma consulta SQL que conta
                # quantos registros existem na tabela eventos.
                #
                # COUNT(*) conta todas as linhas da tabela.
                # AS total cria um apelido para o resultado.
                curs.execute(
                    "SELECT COUNT(*) AS total FROM eventos;"
                )

                # Recupera o resultado da consulta.
                #
                # Como COUNT(*) retorna apenas uma linha,
                # usamos fetchone() para obter somente um registro.
                rows = curs.fetchone()

                # Se existir resultado, converte o valor para inteiro
                # e retorna a quantidade encontrada.
                # Exemplo: {"total": 15}
                # Retorno: 15
                # Caso não exista resultado, retorna 0.
                return int(rows["total"]) if rows else 0

        finally:

            # Fecha a conexão com o banco de dados,
            # independentemente de ter ocorrido erro ou não.
            #
            # Isso evita vazamento de conexões e melhora
            # o desempenho da aplicação.
            conn.close()

    # Lista os eventos cadastrados no banco de dados.
    # Permite aplicar filtros opcionais por:
    # - Data inicial
    # - Data final
    # - Descrição do evento
    # Retorna uma lista contendo objetos da classe Evento.
    def listar(
            self,
            dataIni: Optional[date] = None,
            dataFim: Optional[date] = None,
            textoDesc: Optional[str] = None
    ) -> List[Evento]:

       # Consulta SQL base utilizada para recuperar os eventos.
       # O "WHERE 1=1" facilita a concatenação dos filtros.
       sql = "SELECT id, descricao, dataEvento FROM eventos WHERE 1=1"

       # Lista de parâmetros utilizados na consulta SQL.
       params = []

       # Adiciona filtro de data inicial.
       # Retorna apenas eventos posteriores à data informada.
       if dataIni:
          sql += " AND dataEvento >= %s"

          params.append(dataIni.isoformat())

       # Adiciona filtro de data final.
       # Retorna apenas eventos anteriores ou iguais à data informada.
       if dataFim:
          sql += " AND dataEvento <= %s"

          params.append(dataFim.isoformat())

       # Adiciona filtro por descrição.
       # Permite pesquisar eventos pelo texto informado.
       if textoDesc and textoDesc.strip():
         sql += " AND descricao LIKE %s"

         params.append(f"%{textoDesc.strip()}%")

       # Define a ordenação dos resultados.
       sql += " ORDER BY dataEvento, id;"

       # Abre conexão com o banco de dados.
       conn = obterConexao(nomeBanco)

       try:

          # Cria cursor para execução dos comandos SQL.
          with conn.cursor() as curs:

             # Executa a consulta utilizando os filtros informados.
             curs.execute(sql, params)

             # Recupera todos os registros encontrados.
             linhas = curs.fetchall()

             # Converte os registros retornados pelo banco em objetos da classe Evento.
             return [
                Evento(
                    id=int(linha["id"]),
                    descricao=linha["descricao"],
                    dataEvento=linha["dataEvento"],
                )
                for linha in linhas
             ]

       finally:

          # Fecha a conexão com o banco de dados.
          conn.close()

    # Insere um novo evento no banco de dados.
    # Recebe a descrição e a data do evento , realiza a inserção na tabela eventos
    # e retorna o ID gerado automaticamente.
    def inserir(self, descricao: str, dataEvento: date) -> int:

       # Abre conexão com o banco de dados.
       conn = obterConexao(nomeBanco)

       try:

          # Cria cursor para execução dos comandos SQL.
          with conn.cursor() as curs:

             # Executa o comando de inserção do novo evento.
             # Os valores são enviados através de parâmetros,
             # evitando problemas de segurança e SQL Injection.
             curs.execute(
                """
                INSERT INTO eventos(descricao, dataEvento)
                VALUES (%s, %s)
                """,
                (descricao, dataEvento.isoformat())
             )
             # Recupera o ID gerado automaticamente pelo banco
             # após a inserção do registro.
             novoId = curs.lastrowid

             # Confirma a gravação do registro no banco.
             conn.commit()

       finally:
          # Fecha a conexão com o banco de dados,
          # independentemente de ocorrer erro ou não.
          conn.close()

       # Atualiza os arquivos de backup SQL
       # após a inclusão do novo registro.
       self.exportarDumpSQL()

       # Retorna o ID do evento recém-criado.
       return int(novoId)

    # Atualiza os dados de um evento já existente.
    # Recebe o ID do evento que será alterado, a nova descrição e a nova data do evento.
    def atualizar(
                self,
                idEvento: int,
                descricao: str,
                dataEvento: date
                ) -> None:

       # Abre conexão com o banco de dados.
       conn = obterConexao(nomeBanco)

       try:

          # Cria cursor para execução dos comandos SQL.
          with conn.cursor() as curs:

             # Atualiza os dados do evento informado.
             # O registro é localizado através do ID
             # e recebe os novos valores de descrição e data.
             curs.execute(
            """
            UPDATE eventos
            SET descricao = %s,
                dataEvento = %s
            WHERE id = %s;
            """,
            (
                descricao,
                dataEvento.isoformat(),
                idEvento
            )
          )

             # Confirma a alteração realizada.
             conn.commit()

       finally:

         # Fecha a conexão com o banco de dados.
         conn.close()

       # Atualiza os arquivos de backup após a modificação.
       self.exportarDumpSQL()

    # Remove um evento do banco de dados.
    # Recebe o ID do evento que será excluído
    # e remove permanentemente o registro da tabela.
    def excluir(self, idEvento: int) -> None:
       # Abre conexão com o banco de dados.
       conn = obterConexao(nomeBanco)

       try:

          # Cria cursor para execução dos comandos SQL.
          with conn.cursor() as curs:

             # Executa o comando de exclusão.
             # O registro será localizado através do ID informado.
             curs.execute(
                "DELETE FROM eventos WHERE id = %s;",
                (idEvento,)
             )

             # Confirma a exclusão no banco de dados.
             conn.commit()

       finally:

           # Fecha a conexão com o banco de dados,
           # independentemente de ocorrer erro ou não.
           conn.close()

       # Atualiza os arquivos de backup SQL após a exclusão.
       self.exportarDumpSQL()

    # Busca um evento específico no banco de dados.
    # Recebe o ID do evento como parâmetro e retorna
    # um objeto da classe Evento caso o registro exista.
    # Se nenhum registro for encontrado com o ID informado,
    # o método retorna None.
    def obterPorId(self, idEvento: int) -> Optional[Evento]:

       # Abre conexão com o banco de dados.
       conn = obterConexao(nomeBanco)

       try:

          # Cria cursor para execução dos comandos SQL.
          with conn.cursor() as curs:

             # Executa consulta para localizar o evento
             # correspondente ao ID informado.
             curs.execute(
                "SELECT id, descricao, dataEvento FROM eventos WHERE id = %s;",
                (idEvento,)
             )

             # Recupera o primeiro registro encontrado.
             rows = curs.fetchone()

             # Verifica se nenhum registro foi encontrado.
             # Nesse caso, retorna None.
             if not rows:
                return None

             # Converte o resultado retornado pelo banco
             # em um objeto da classe Evento.
             return Evento(
                id=int(rows["id"]),
                descricao=rows["descricao"],
                dataEvento=rows["dataEvento"]
             )

       finally:

        # Fecha a conexão com o banco de dados,
        # independentemente de ocorrer erro ou não.
        conn.close()

    # Método responsável por gerar arquivos de backup (dump SQL)
    # contendo toda a estrutura da tabela eventos e todos os
    # registros atualmente cadastrados no banco de dados.
    # São gerados dois arquivos:
    # 1. Um arquivo principal, sempre sobrescrito com a versão mais recente.
    # 2. Um arquivo versionado contendo data e hora da geração do backup,
    #    permitindo manter um histórico das exportações realizadas.
    def exportarDumpSQL(self):

        # Cria automaticamente a pasta onde os backups serão armazenados.
        # Caso a pasta já exista, nenhum erro será gerado.
        os.makedirs(caminhoExportarSQL, exist_ok=True)

        # Nome do arquivo principal de backup.
        # Esse arquivo sempre conterá a versão mais recente.
        base = "agendaDatasBRDbDump.sql"

        # Monta o caminho completo do arquivo principal.
        pPrincipal = os.path.join(caminhoExportarSQL, base)

        # Gera um identificador baseado na data e hora atual.
        # Esse identificador será utilizado para criar arquivos
        # de backup versionados.
        carimbo = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Monta o caminho completo do arquivo versionado.
        pVersao = os.path.join(
            caminhoExportarSQL,
            f"agendaDatasBRDbDump{carimbo}.sql"
        )

        # Abre conexão com o banco de dados.
        conn = obterConexao(nomeBanco)

        try:

            # Cria cursor para execução dos comandos SQL.
            with conn.cursor() as curs:

                # Recupera todos os eventos cadastrados.
                # Os registros são ordenados por data e ID.
                curs.execute(
                    "SELECT id, descricao, dataEvento "
                    "FROM eventos "
                    "ORDER BY dataEvento, id;"
                )

                # Armazena todos os registros encontrados.
                linhas = curs.fetchall()

        finally:

            # Fecha a conexão com o banco de dados.
            conn.close()

        # Lista utilizada para montar todo o conteúdo
        # do arquivo de backup SQL.
        partes: List[str] = []

        # Adiciona ao início do arquivo a data e hora
        # em que o backup foi gerado.
        partes.append(
            f"-- Dump gerado em "
            f"{datetime.now().isoformat(sep=' ', timespec='seconds')} --"
        )

        # Define a codificação utilizada pelo banco.
        partes.append("SET NAMES utf8mb4;")

        # Comando responsável por criar o banco de dados
        # caso ele ainda não exista.
        partes.append(
            f"CREATE DATABASE IF NOT EXISTS {nomeBanco} "
            f"DEFAULT CHARACTER SET utf8mb4;"
        )

        # Define qual banco será utilizado durante a execução
        # dos comandos do dump.
        partes.append(f"USE {nomeBanco};")

        # Adiciona uma linha em branco para organização visual.
        partes.append("")

        # Remove a tabela caso ela já exista.
        partes.append("DROP TABLE IF EXISTS eventos;")

        # Adiciona o script responsável por recriar a tabela.
        partes.append(
            """
            CREATE TABLE eventos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                descricao VARCHAR(200) NOT NULL,
                dataEvento DATE NOT NULL,
                INDEX indexDataEvento (dataEvento)
            ) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4;
            """
        )

        # Adiciona uma linha em branco para organização.
        partes.append("")

        # Verifica se existem registros cadastrados.
        if linhas:

            # Inicia o comando SQL de inserção dos dados.
            partes.append(
                "INSERT INTO eventos(id, descricao, dataEvento) VALUES"
            )

            # Lista que armazenará os registros formatados.
            values = []

            # Percorre todos os registros retornados pelo banco.
            for linha in linhas:

                # Escapa aspas simples para evitar erros
                # de sintaxe durante a restauração do backup.
                descricao = linha["descricao"].replace("'", "''")

                # Converte a data para formato texto.
                dataIso = linha["dataEvento"].isoformat()

                # Monta o registro no formato SQL.
                values.append(
                    f"({int(linha['id'])}, '{descricao}', '{dataIso}')"
                )

            # Adiciona todos os registros ao comando INSERT.
            partes.append(",\n".join(values) + ";")

        else:

            # Caso não existam registros, adiciona uma observação.
            partes.append("-- Tabela vazia --")

        # Junta todas as partes do dump em um único texto.
        texto = "\n".join(partes)

        # Salva o arquivo principal de backup.
        with open(pPrincipal, "w", encoding="utf-8") as arquivo:
            arquivo.write(texto)

        # Salva o arquivo versionado de backup.
        with open(pVersao, "w", encoding="utf-8") as arquivo:
            arquivo.write(texto)

