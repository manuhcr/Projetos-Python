


from typing import List, Tuple
# 'List' significa uma Lista (usamos colchetes [ ]). Ela guarda vários itens.
# 'Tuple' significa uma Tupla (usamos parênteses ( )). Ela guarda um grupo de dados fixos.
# Juntos, 'List[Tuple]' descrevem exatamente o formato de uma tabela de banco de dados.

from config import nome_tabela



 #A 'class' (Classe) funciona como um "Molde" ou uma "Planta de Arquitetura".
# Em vez de ter várias funções soltas, tudo o que é registro de pessoas pertence a um só lugar.
class PessoaRepo:
    """
    Esta classe centraliza todas as ações (CRUD) que podem ser feitas na tabela de pessoas.
    """

    def __init__(self, conn):
        # self.conn: O canal de comunicação aberto com o banco.
        self.conn = conn
        # self.curs: O executor de comandos. Pense nele como o "braço" que escreve o SQL.
        self.curs = conn.cursor()

    def insert_tabela(self, nome: str, email: str, telefone: str) -> None:
        # %s são placeholders. Eles dizem ao banco: "vai vir um dado aqui".
        # O valor real NÃO vai na string, vai no segundo argumento do execute.
        self.curs.execute(
            f"INSERT INTO {nome_tabela}(nome, email, telefone) VALUES (%s, %s, %s)",
            (nome, email, telefone) # O driver limpa esses dados antes de enviar
        )
    # Aqui você prepara o termo de busca.
    # Mesmo com o LIKE, o uso do %s garante que o usuário não 'saia' da busca
    # para tentar executar comandos maliciosos.
    def search_tabela(self, campo: str) -> List[Tuple]:

        # O '%' é o segredo do LIKE:
        # '%joao' -> Procura tudo que TERMINA com joao.
        # 'joao%' -> Procura tudo que COMEÇA com joao.
        # '%joao%' -> Procura tudo que CONTÉM joao em qualquer lugar.

        isLike = f"%{campo}%"  # Aqui você está dizendo: "busque o que o usuário digitou em qualquer parte da palavra"
        # O LIKE avisa o banco para não ser rígido na busca


        self.curs.execute(
            f"""SELECT id, nome, email, telefone, criado_em FROM {nome_tabela} 
            WHERE nome LIKE %s OR telefone LIKE %s OR email LIKE %s 
            ORDER BY id DESC 
            """,
            (isLike, isLike, isLike) # O valor entra como texto puro, nunca como comando
        )
        return self.curs.fetchall()

    def update(self, id_: int, nome: str, email: str, telefone: str) -> None:
        # O SQL Injection em Updates é perigoso porque poderia alterar a tabela toda.
        # Passando o id_ e os dados via %s, o banco valida os tipos (ex: id deve ser int).
        self.curs.execute(
            f"UPDATE {nome_tabela} SET nome = %s, email = %s, telefone = %s WHERE id = %s",
            (nome, email, telefone, id_)
        )

    def delete(self, id_: int) -> None:
        # Remove o registro da tabela baseado no ID fornecido
        self.curs.execute(
            f"DELETE FROM {nome_tabela} WHERE id = %s",

            # (id_,) -> Esta vírgula transforma o parênteses em uma TUPLA.
            # O método .execute() EXIGE que os valores sejam passados dentro de uma
            # coleção (lista ou tupla), mesmo que seja apenas UM único valor.
            # Sem essa vírgula, o Python leria apenas como um número comum e
            # o banco de dados retornaria um erro de programação.
            (id_,)
        )



