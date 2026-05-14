# --- IMPORTAÇÕES ---
from encodings import utf_8           # Importação para lidar com codificação de texto
from multiprocessing import connection # Ferramenta para gerenciar conexões (geralmente usada em sistemas paralelos)
from typing import List, Optional     # Tipagem: define que algo pode ser uma Lista ou ser Opcional (vazio)
import os                             # Biblioteca para mexer em pastas e arquivos do computador
from datetime import datetime         # Biblioteca para pegar data e hora atual

# Importações de outros arquivos do seu próprio projeto
from config_banco import getConn, nameBench, wayExportSql # Conexão, nome do banco e caminho do backup
from modelos import Local                                 # A classe/modelo que representa uma cidade


# --- INÍCIO DA CLASSE REPOLOCAL ---
# Aqui é definido o "projeto" do seu Repositório de Locais.
class repoLocal:

    # O __init__ é o "Nascimento": tudo o que está aqui dentro acontece
    # AUTOMATICAMENTE no momento em que você instancia a classe (ex: repo = repoLocal()) em main.py.
    # Quando você faz: repo = repoLocal()
    # O computador reserva um espaço na Memória RAM (a "mesa de trabalho" dele).
    # É o momento em que a "receita" vira um "bolo" de verdade.
    # Agora o 'repo' é um objeto REAL: ele gasta energia, ocupa memória e pode agir.
    def __init__(self):
        """
        O Construtor: É O 'START' AUTOMÁTICO:
        Tudo que está aqui dentro roda SOZINHO no segundo que você cria o objeto.
        Ele serve para configurar o sistema: se o banco não existe, ele cria;
        se está vazio, ele preenche.
        É o jeito de garantir que o código não vai travar por falta de banco ou tabela
        quando você for usar as outras funções.
        """

        # 1. "Primeiro, vou garantir que o banco de dados e a tabela existem."
        # É como construir a loja física e colocar as prateleiras.
        self.warrantyOfBenchAndTable()

        # 2. "Agora que a loja existe, vou ver se ela está vazia."
        # Se estiver vazia, eu coloco aquele estoque inicial de cidades (Brasil, Portugal, etc.).
        # Se já tiver coisa lá, eu não faço nada para não bagunçar.
        self.insertInitialDataIfBlank()


def warrantyOfBenchAndTable(self) -> None:
    # 1. "Vou abrir uma conexão 'vazia' com o servidor de banco de dados."
    # É como bater no portão do prédio antes de saber em qual sala vou entrar.
    connWithoutBench = getConn()

    try:
        with connWithoutBench.cursor() as curs:
            # 2. "Digo ao servidor: 'Crie o banco de dados com este nome, se ele não existir ainda'."
            # O utfmb4 é para garantir que a gente consiga escrever nomes com acento e emojis.
            curs.execute(f"CREATE DATABASE IF NOT EXISTS {nameBench} "
                         f"DEFAULT CHARACTER SET utfmb4;")
    finally:
        # 3. "Terminei de criar o banco (ou conferir)? Então fecho essa conexão genérica."
        connWithoutBench.close()

    # 4. "Agora que o banco existe com certeza, abro uma conexão nova direto dentro dele."
    # É como se agora eu tivesse a chave da sala específica.
    connect = getConn(nameBench)

    try:
        with connect.cursor() as curs:
            # 5. "Mando o comando para construir a tabela 'local' se ela não estiver lá."
            curs.execute(
                """
                CREATE TABLE IF NOT EXISTS local (
                 id INT AUTO_INCREMENT PRIMARY KEY, -- O RG da linha: o banco gera o número sozinho.
                 country VARCHAR(255) NOT NULL,     -- Coluna para o País (texto de até 255 letras).
                 state VARCHAR(255) NOT NULL,       -- Coluna para o Estado.
                 city VARCHAR(255) NOT NULL,        -- Coluna para a Cidade.

                 -- Crio 'Índices' (como o índice de um livro) para o banco achar 
                 -- países e estados muito mais rápido quando a tabela tiver milhares de linhas.
                 INDEX iCountry(country),           
                 INDEX iCountryState(country, state) 
                )ENGINE=InnoDB DEFAULT CHARACTER SET utfmb4; """
            )
    finally:
        # 6. "Tudo pronto! Fecho a conexão para não deixar a porta aberta à toa."
        connect.close()


def insertInitialDataIfBlank() -> None:
    # 1. "Vou verificar se a prateleira está vazia."
    # Chamo a função que conta os registros. Se já tiver qualquer coisa (mais que 0),
    # eu paro por aqui (return) para não duplicar os dados.
    if self.getQuantity() > 0:
        return

    # 2. "Como está vazio, preparo a lista de carga."
    # Crio uma lista de 'pacotinhos' (tuplas), onde cada um tem (País, Estado, Cidade).
    dataSeed = [
        ("Brasil", "São Paulo", "São Paulo"),
        ("Brasil", "São Paulo", "Campinas"),
        ("Brasil", "São Paulo", "Santos"),
        ("Brasil", "Rio de Janeiro", "Rio de Janeiro"),
        ("Brasil", "Rio de Janeiro", "Niterói"),
        ("Brasil", "Minas Gerais", "Belo Horizonte"),
        ("Brasil", "Minas Gerais", "Uberlândia"),
        ("Brasil", "Minas Gerais", "Juiz de Fora"),

        ("Estados Unidos", "Califórnia", "Los Angeles"),
        ("Estados Unidos", "Califórnia", "San Diego"),
        ("Estados Unidos", "Nova Iorque", "Nova Iorque (Manhattan)"),
        ("Estados Unidos", "Nova Iorque", "Buffalo"),
        ("Estados Unidos", "Texas", "Houston"),
        ("Estados Unidos", "Texas", "Dallas"),

        ("Portugal", "Lisboa", "Lisboa"),
        ("Portugal", "Lisboa", "Sintra"),
        ("Portugal", "Porto", "Porto"),
        ("Portugal", "Porto", "Vila Nova de Gaia"),
        ("Portugal", "Setúbal", "Setúbal"),
        ("Portugal", "Setúbal", "Almada")
    ]

    # 3. "Abro a porta do banco de dados usando o nome correto dele."
    con = getConn(nameBench)

    try:
        with con.cursor() as curs:
            # 4. "Uso uma 'máquina' chamada executemany."
            # Em vez de inserir um por um, eu mando a lista inteira de uma vez.
            # O '%s' são os espaços vazios que serão preenchidos pelos dados da lista.
            curs.executemany(
                f"INSERT INTO local (country, state, city) VALUES (%s, %s, %s);",
                dataSeed
            )

        # 5. "Bato o carimbo final (commit) para o banco salvar tudo no disco."
        # Sem isso, as alterações podem ser perdidas quando a conexão fechar.
        con.commit()

    finally:
        # 6. "Fecho a porta do banco, independentemente de ter dado certo ou errado."
        con.close()


def getQuantity(self) -> int:  # 1. "Vou criar uma função para me dizer a quantidade total (um número inteiro)."
    con = getConn(nameBench)  # 2. "Primeiro, pego a chave e abro a porta do banco de dados."

    try:
        with con.cursor() as curs:  # 3. "Pego um funcionário (cursor) para anotar o que eu pedir."

            # 4. "Digo a ele: 'Vá na tabela local e conte quantas linhas tem lá. Chame esse resultado de total'."
            curs.execute("SELECT COUNT(*) AS total FROM local;")

            # 5. "Ele volta com a prancheta trazendo todos os resultados (fetchall)."
            # Como é uma contagem, só vem uma linha com o número.
            rows = curs.fetchall()

            # 6. "Aqui eu confiro: 'A prancheta tem informação (rows)?'"
            # Se tiver, eu pego o número que está na coluna 'total' e transformo em número inteiro.
            # Se a prancheta estiver vazia por algum erro, eu respondo 0.
            return int(rows['total'] if rows else 0)
    finally:
        # 7. "Independente de ter conseguido contar ou não, eu devolvo a chave e fecho a porta."
        con.close()

def list(self, country: Optional[str] = None, state: Optional[str] = None, city: Optional[str] = None) -> List[Local]:
    """Lista as cidades permitindo filtrar por país, estado ou cidade."""
    # 1. Começamos a frase principal.
    # O "WHERE 1=1" é como se eu escrevesse: "Procure as cidades onde o seguinte é verdade: (sempre sim)..."
    sql = "SELECT id, country, state, city FROM local WHERE 1=1"

    # 2. Agora vou decidir se coloco mais condições na minha frase.
    # É como se eu pensasse: "Bom, SE o usuário escolheu um país, eu acrescento isso na frase."
    if country:
        # Como já escrevi "WHERE 1=1" lá atrás, aqui eu só preciso grudar o "E" (AND).
        # A frase ficaria: "... WHERE 1=1 AND country = 'Brasil'"
        sql += " AND country = %s"

        # 3. Faço a mesma coisa para o estado.
    if state:
        # Repare: eu não preciso checar se o 'country' foi escrito antes.
        # Eu simplesmente grudo o "AND" porque o "1=1" já abriu o caminho.
        # Se tiver país, fica: "...1=1 AND country = %s AND state = %s"
        # Se NÃO tiver país, fica: "...1=1 AND state = %s" (O banco aceita os dois!)
        sql += " AND state = %s"

    # 4. E finalizo com a cidade, seguindo a mesma regra.
    if city:
        sql += " AND city = %s"

    # 5. No fim, coloco o ponto final da frase (a ordem alfabética).
    sql += " ORDER BY country, state, city;"

    # 6. Abre a porta do banco de dados específico (o nameBench).
    con = getConn(nameBench)

    try:
        with con.cursor() as curs:
            # 7. Manda o funcionário (cursor) executar a frase SQL que montamos antes.
            # O 'params' são os valores reais (tipo 'Brasil') que entram no lugar dos '%s'.
            curs.execute(sql, params)

            # 8. Pega todas as linhas que o banco encontrou e guarda na variável 'lines'.
            lines = curs.fetchall()

            # 9. TRADUÇÃO DE DADOS:
            # O banco devolve 'dicionários' (texto puro), mas o resto do seu programa quer 'Objetos'.
            # Essa linha percorre cada linha (l) que veio do banco e "fabrica" um objeto 'Local'
            # preenchendo o ID, País, Estado e Cidade.
            return [Local(id=l["id"], country=l["country"], state=l["state"], city=l["city"]) for l in lines]

    finally:
        # 10. Não importa se deu certo ou não, a porta tem que ser fechada aqui.
        con.close()


def getCountry(self) -> List[str]:
    """Busca a lista de todos os países únicos no banco."""
    # 1. Abre a conexão com o banco de dados.
    con = getConn(nameBench)

    try:
        with con.cursor() as curs:
            # 2. O 'DISTINCT' é o segredo aqui:
            # Ele serve para NÃO REPETIR. Se você tem 50 cidades do "Brasil",
            # ele olha para a lista e fala: "Só me dá o nome do país uma vez".
            curs.execute("SELECT DISTINCT country FROM local ORDER BY country;")

            # 3. Pego o resultado bruto e "limpo" ele:
            # O fetchall traz uma lista de pastas (dicionários).
            # Essa linha extrai apenas o texto do país de dentro de cada pasta.
            # No final, você recebe uma lista simples, tipo: ["Brasil", "EUA", "Portugal"]
            return [row["country"] for row in curs.fetchall()]
    finally:
        # 4. Fecha a conexão para não deixar o banco aberto sem motivo.
        con.close()


def getState(self, country: str) -> List[str]:
    """Busca a lista de estados únicos de um país específico."""
    # 1. Abre a conexão com o banco.
    con = getConn(nameBench)

    try:
        with con.cursor() as curs:
            # 2. A "PERGUNTA" AO BANCO:
            # "Me dê os estados (sem repetir - DISTINCT) que pertencem ao país X".
            # O '%s' é um buraco que será preenchido pelo nome do país que o usuário escolheu.
            curs.execute(
                "SELECT DISTINCT state FROM local WHERE country = %s ORDER BY state;",
                (country,)  # 3. O Python troca o %s pelo valor desta variável com segurança.
                # Repare que tem uma vírgula perdida ali: (country,). Isso não é erro!
                # Se eu escrevesse apenas (country), o Python acharia que são apenas
                # parênteses comuns, sem dados que devem ser guardados.
            )

            # 4. TRADUÇÃO:
            # Pega as linhas brutas do banco e extrai apenas o texto do estado.
            # Se o país for "Brasil", retorna algo como: ["Minas Gerais", "Rio de Janeiro", "São Paulo"]
            return [row["state"] for row in curs.fetchall()]
    finally:
        # 5. Fecha a porta do banco.
        con.close()

def getCity(self, country: str, state: str) -> List[str]:
    """Busca as cidades de um estado e país específicos."""
    # 1. Primeiro, abre a conexão com o banco
    con = getConn(nameBench)
    try:
        with con.cursor() as curs:
            # 2. DIZ AO BANCO:
            # "Me dê as cidades (sem repetir - DISTINCT) que pertencem ao país e ao estado X".
            # O '%s' é um buraco que será preenchido pelo nome do país e estado que o usuário escolheu.
            curs.execute(
                "SELECT DISTINCT city FROM local WHERE country = %s AND state = %s ORDER BY city;",
                (country, state) # 3. O Python preenche os '%s' na ordem: primeiro país, depois estado.
                # Passar os dados aqui (e não direto na frase) protege o banco de ataques (SQL Injection).
            )
            #4. Por fim, pega as linhas do banco, extrai e retorna apenas as cidades que tem o mesmo estado e pais
            return [row["city"] for row in curs.fetchall()]
    finally:
        #5. Fecha o banco para que os recursos do sistema não sejam desperdiçados.
        con.close()


def insert(self, country: str, state: str, city: str) -> int:
    """Insere uma nova cidade manualmente e retorna o novo ID."""
    # 1. Abre conexão com o banco de dados.
    con = getConn(nameBench)
    try:
        with con.cursor() as curs:
            # 2. O cursor é aberto e executa o comando INSERT
            # e garante que o banco só receba dados adequados e
            # seguros a partir do placeholder "%s".
            curs.execute(
                "INSERT INTO local (country, state, city) VALUES (%s, %s, %s);",
                (country, state, city)
            )
            # 3. Como o Banco (MySQL) gera o ID sozinho (com o AUTO_INCREMENT), o Python não sabe
            # que número foi esse. O 'lastrowid' serve para perguntar ao banco:
            # "Ei, qual foi o número de ID que você acabou de criar para essa linha?".
            # Ele traz essa resposta para podermos usar o ID correto no resto do programa.
            new_id = curs.lastrowid

        # 4. O Commit: Salva e confirma todas as atualizações no banco de forma permanente.
        con.commit()
    finally:
        # 5. Para evitar desperdício de recursos, fecha o banco sempre.
        con.close()

    # 6. Gera um novo backup automático (.sql) com as atualizações recentes.
    self.exportDumpSql()

    # 7. Retorna o número inteiro do novo ID criado para uso do sistema.
    return int(new_id)


def update(self, localId: int, country: str, state: str, city: str) -> None:
    """Altera os dados de uma cidade já existente pelo ID."""

    # 1. Abre a conexão com o banco.
    con = getConn(nameBench)

    try:
        with con.cursor() as curs:
            # 2. O curs executa o comando de ATUALIZAÇÃO:
            # CUIDADO: Se esquecer o WHERE, você altera a tabela INTEIRA de uma vez,
            # sem respeitar a sua excecao de ser APENAS e exatamente essa query, com o WHERE.
            curs.execute(
                "UPDATE local SET country = %s, state = %s, city = %s WHERE id = %s;",
                (country, state, city, localId) #Como foi feito em todas as partes do código e
                # para a segurança do banco, os valores são inseridos nos placeholders "%s"
            )

        # 3. Após tudo atualizado, confirma que a alteração deve ser salva permanentemente.
        con.commit()

    finally:
        # 4. Libera a conexão para não travar o banco (evitando também erros de excesso de memória).
        con.close()

    # 5. Como mudamos um dado, o arquivo de backup (.sql)
    # precisa ser gerado novamente para refletir a mudança.
    self.exportDumpSql()


def delete(self, localId: int) -> None:
    """Apaga uma cidade do banco de dados pelo ID."""

    # 1. Abre a conexão com o banco de dados.
    con = getConn(nameBench)
    try:
        with con.cursor() as curs:
            # 2. O cursor executa o comando DELETE:
            # Repare que temos novamente o "WHERE". Ele especifica ONDE
            # a exclusão deve ocorrer a partir do ID informado no placeholder "%s".
            # Sem esse filtro, o banco apagaria TODOS os registros da tabela local.
            curs.execute("DELETE FROM local WHERE id = %s;", (localId,))
            # Por que essa vírgula, está ali?
            # A vírgula em (localId,) é necessária porque o comando .execute()
            # exige que os dados sejam entregues numa "caixa" (Tupla).
            # Mesmo sendo UM único dado, ele precisa estar "empacotado" para o Python
            # não o confundir com um número comum entre parênteses. Sem a vírgula,
            # ele pode achar que é apenas um número comum entre parênteses
            # e dar erro.

        # 3. Confirma a exclusão permanentemente no banco de dados (Commit).
        con.commit()
    finally:
        # 4. Encerra a conexão para liberar os recursos do sistema e evitar uso desnecessário de memória.
        con.close()

    # 5. Gera um novo backup atualizado, agora sem o registro que acabamos de apagar.
    self.exportDumpSql()


def getById(self, localId: int) -> Optional[Local]:
    """Busca uma cidade específica usando o ID."""

    # 1. Abre a conexão para entrar no banco de dados.
    con = getConn(nameBench)

    try:
        with con.cursor() as curs:
            # 2. O comando SELECT (Busca):
            # Novamente, o ID vai dentro da "caixa" (localId,) por exigência do Python.
            curs.execute(
                "SELECT id, country, state, city FROM local WHERE id = %s;",
                (localId,)
            )

            # 3. O fetchone() pega apenas um ou nenhum:
            # Como o ID é único, o banco só vai achar 1 resultado ou NADA.
            # O fetchone() traz apenas essa linha encontrada.
            rows = curs.fetchone()

            # 4. Verificação de segurança:
            # Se o ID não existir (ex: buscar ID 999 num banco que só tem 10 cidades),
            # o 'rows' virá vazio. Aí retornamos None (nada encontrado).
            if not rows:
                return None

            # 5. Transformação (O "Nascimento" do modelo):
            # O banco devolve um dicionário/lista, mas o código Python usa
            # a classe 'Local'. Aqui transformamos os dados brutos em um objeto real.
            return Local(
                id=rows["id"],
                country=rows["country"],
                state=rows["state"],
                city=rows["city"]
            )
    finally:
        # 6. Fechamos a porta ao sair, sempre!
        con.close()


def exportDumpSql(self) -> None:
    """Gera um arquivo físico (.sql) com todos os dados atuais (Backup)."""
    con = getConn(nameBench)

    # 1. PREPARAÇÃO DO TERRENO:
    # Cria as pastas necessárias no seu computador. Se a pasta 'backup' não existir,
    # o 'os.makedirs' cria ela na hora para o código não dar erro de "caminho não encontrado".
    os.makedirs(wayExportSql, exist_ok=True)

    # 2. DEFINIÇÃO DOS NOMES:
    # 'mainWay': É o arquivo oficial, sempre com o mesmo nome (sobrescreve o anterior).
    # 'wayVersion': É uma cópia com "RG", contendo data e hora (timestamp).
    # Isso serve para você ter um histórico e não perder versões antigas.
    baseName = 'geoDbDump.sql'
    mainWay = os.path.join(wayExportSql, baseName)
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    wayVersion = os.path.join(wayExportSql, f"geoDbDump{stamp}.sql")

    # 3. COLETA DE DADOS:
    # Aqui usamos o 'fetchall()' porque queremos a tabela INTEIRA para o backup.
    try:
        with con.cursor() as curs:
            curs.execute("SELECT id, country, state, city FROM local ORDER BY country, state, city")
            lines = curs.fetchall()
    finally:
        con.close()

    # 4. MONTAGEM DO "ROTEIRO" (Script SQL):
    # O arquivo .sql nada mais é do que uma lista de comandos para o banco se reconstruir.
    content = []
    content.append(f"--- Dump gerado em {datetime.now().isoformat(sep=' ', timespec='seconds')}")
    content.append("SET NAMES utf8mb4;")  # Garante que acentos e emojis funcionem
    content.append(f"CREATE DATABASE IF NOT EXISTS {nameBench};")
    content.append(f"USE {nameBench};")
    content.append(f"DROP TABLE IF EXISTS local;")  # Limpa a mesa antes de reconstruir

    # Adiciona o comando de criação da estrutura (as colunas e índices)
    content.append(
        """ 
        CREATE TABLE local (
            id INT PRIMARY KEY AUTO_INCREMENT,
            country VARCHAR(60) NOT NULL,
            state VARCHAR(60) NOT NULL,
            city VARCHAR(80) NOT NULL,
            INDEX iCountry (country),
            INDEX iCountryState (country, state)
        ) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4;       
        """
    )

    # 5. O CORPO DOS DADOS:
    # Se existirem cidades no banco, vamos criar o comando INSERT para cada uma.
    if lines:
        content.append("INSERT INTO local (id, country, state, city) VALUES")
        valuesSql = []

        for l in lines:
            # LIMPEZA DE SEGURANÇA:
            # Se uma cidade se chamar "Sant'Ana", a aspa simples quebra o SQL.
            # O .replace("'", "''") duplica a aspa, que é o jeito do SQL entender
            # que aquilo é um texto e não o fim do comando.
            c = l["country"].replace("'", "''")
            s = l["state"].replace("'", "''")
            ci = l["city"].replace("'", "''")

            # Monta a linha: (1, 'Brasil', 'SP', 'São Paulo')
            valuesSql.append(f"({int(l['id'])}, '{c}', '{s}', '{ci}')")

        # Junta tudo com vírgulas e coloca o ponto e vírgula no final.
        content.append(',\n'.join(valuesSql) + ';')
    else:
        content.append("-- Tabela Vazia")

    # 6. GRAVAÇÃO FINAL (HD):
    # Transforma a lista de frases em um blocão de texto.
    text = "\n".join(content)

    # Salva o arquivo "Atual" e a "Cópia com Data" no seu computador.
    with open(mainWay, "w", encoding="utf-8") as f:
        f.write(text)
    with open(wayVersion, "w", encoding="utf-8") as f:
        f.write(text)