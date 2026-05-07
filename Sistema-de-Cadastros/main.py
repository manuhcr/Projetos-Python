import app
from db import conectar, criar_banco_e_tabela
from app import AppCadastro

# Verifica se este arquivo está sendo executado diretamente (e não importado)
if __name__ == '__main__':

   try:
       # Tenta uma conexão inicial sem especificar o banco de dados.
       # Isso serve para garantir que o servidor MySQL está ativo.
       c = conectar(usar_banco = False)

       # Chama a função que verifica se o banco e as tabelas já existem.
       # Se não existirem, ela cria-os automaticamente.
       criar_banco_e_tabela()

       # Fecha essa conexão inicial após garantir que a estrutura está pronta.
       c.close()

   except Exception:
        # Caso ocorra qualquer erro na conexão ou criação (ex: banco fora do ar),
        # o programa ignora o erro e tenta seguir em frente.
        pass

   # Cria a instância principal da sua interface gráfica (o app em si)
   app = AppCadastro()

   # Inicia o loop do Tkinter, mantendo a janela aberta e escutando os cliques do usuário
   app.mainloop()
