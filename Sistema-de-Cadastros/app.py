# Biblioteca principal utilizada para criar a interface
# gráfica da aplicação (janelas, campos, botões e tabelas).
import tkinter as tk

# ttk:
#     Componentes visuais modernos do Tkinter.
#
# messagebox:
#     Exibe mensagens de informação, aviso e erro.
#
# filedialog:
#     Permite selecionar arquivos e pastas através
#     de janelas do sistema operacional.
from tkinter import ttk, messagebox, filedialog

# Classe utilizada para criar e manipular
# planilhas do Excel (.xlsx).
from openpyxl import Workbook

# Converte números de colunas em letras do Excel.
#
# Exemplo:
# 1 -> A
# 2 -> B
# 27 -> AA
from openpyxl.utils import get_column_letter

# Importa a função conectar do módulo db, que é
# responsável por estabelecer a conexão com o
# banco de dados MySQL.
from db import conectar

# Classe responsável pelas operações de banco
# de dados relacionadas ao cadastro de pessoas
# (inserir, atualizar, excluir e consultar).
from repo import PessoaRepo

# Funções responsáveis pela personalização visual
# da interface e da tabela de registros.
from style import apply_style , apply_zebra_treeview, field_treeview

# Valida os dados informados pelo usuário antes
# de realizar operações de cadastro ou atualização.
#
# Retorna:
# True -> dados válidos
# False -> dados inválidos, juntamente com a
# mensagem que deverá ser exibida ao usuário.
def validate(nome: str, telefone: str, email: str):
    # Verifica se o campo nome foi preenchido.
    # O nome é obrigatório para identificar a pessoa.
    if not nome:
        return False, "Erro de Validação", "O campo 'Nome' é obrigatório."

    # Verifica se o campo telefone foi preenchido.
    # O telefone é obrigatório para contato.
    if not telefone:
        return False, "Erro de Validação", "O campo 'Telefone' é obrigatório."

    # Verifica se o campo e-mail foi preenchido.
    # O e-mail é obrigatório para contato e identificação.
    if not email:
        return False, "Erro de Validação", "O campo 'Email' é obrigatório."

    # Remove espaços em branco no início e no final
    # do texto e verifica se o nome possui pelo menos
    # 3 caracteres.
    #
    # Exemplo inválido:
    # "Jo"
    #
    # Exemplo válido:
    # "João"
    if len(nome.strip()) < 3:
        return False, "Erro de Validação", \
            "Informe um nome que contenha pelo menos 3 caracteres."

    # Verifica se o e-mail possui os caracteres
    # normalmente encontrados em endereços válidos.
    #
    # Exemplo válido:
    # usuario@email.com
    #
    # Exemplo inválido:
    # usuarioemailcom
    if not "@" in email or not "." in email:
        return False, "Erro de Validação", \
            "Informe um email válido."

    # Remove espaços em branco e verifica se o telefone
    # possui uma quantidade mínima de caracteres.
    #
    # Essa validação ajuda a evitar telefones incompletos.
    if len(telefone.strip()) < 8:
        return False, "Erro de Validação", \
            "Informe um telefone válido, contendo apenas números e pelo menos 8 dígitos."

    # Se todas as verificações forem aprovadas,
    # os dados são considerados válidos e a função
    # retorna True.
    return True

# Classe principal da aplicação.
#
# Herda de tk.Tk, tornando-se a janela principal
# do sistema de cadastro de pessoas.
class AppCadastro(tk.Tk):
    # Método construtor da classe.
    #
    # É executado automaticamente quando um objeto da
    # classe AppCadastro é criado.
    #
    # Sua responsabilidade é configurar a janela,
    # inicializar variáveis, conectar ao banco de dados,
    # criar os componentes da interface e carregar os
    # registros existentes.
    def __init__(self):
        # Executa o construtor da classe Tk, criando
        # a janela principal da aplicação.
        super().__init__()

        # Define o título exibido na barra superior da janela.
        self.title(
            "Sistema de Cadastro de Pessoas - Tkinter + MySQL"
        )

        # Define o tamanho mínimo permitido para a janela.
        # O usuário poderá aumentar a janela, mas não
        # diminuí-la abaixo dessas dimensões.
        self.minsize(
            900,
            520
        )

        # Aplica as configurações visuais da aplicação,
        # como cores, fontes e estilos personalizados.
        apply_style(self)

        # Cria uma conexão com o banco de dados.
        # Essa conexão será utilizada para realizar
        # consultas, inserções, alterações e exclusões.
        self.conn = conectar(usar_banco=True)

        # Cria um objeto responsável pelas operações
        # relacionadas ao cadastro de pessoas.
        self.repo = PessoaRepo(self.conn)

        # Variável vinculada ao campo ID.
        # Armazena o identificador da pessoa selecionada.
        self.var_id = tk.StringVar()

        # Variável vinculada ao campo nome.
        self.var_nome = tk.StringVar()

        # Variável vinculada ao campo telefone.
        self.var_telefone = tk.StringVar()

        # Variável vinculada ao campo e-mail.
        self.var_email = tk.StringVar()

        # Variável utilizada para armazenar o texto
        # informado no campo de pesquisa.
        self.var_search = tk.StringVar()

        # Variável utilizada na barra de status.
        # O valor inicial exibido será "Pronto."
        self.var_status = tk.StringVar(
            value="Pronto."
        )

        # Cria os campos do formulário.
        self.build_form()

        # Cria os botões da interface.
        self.build_button()

        # Cria a tabela de registros.
        self.build_table()

        # Cria a barra de status da aplicação.
        self.build_statusbar()

        # Centraliza a janela na tela.
        self.allign_window()

        # Cria um atalho de teclado.
        #
        # CTRL + N executa o método clean_fields(),
        # limpando os campos do formulário.
        self.bind(
            "<Control-n>",
            lambda e: self.clean_fields()
        )

        # Cria um atalho para atualizar a tabela.
        #
        # Ao pressionar F5, os registros serão
        # carregados novamente.
        self.bind(
            "<F5>",
            lambda e: self.list_all()
        )

        # Carrega os registros existentes no banco
        # e exibe os dados na tabela.
        self.list_all()

        # Define o comportamento executado quando
        # o usuário fecha a janela.
        #
        # Antes de encerrar a aplicação, o método
        # _fechar_() será executado.
        self.protocol(
            "WM_DELETE_WINDOW",
            self._fechar_
        )

    # Centraliza a janela da aplicação na tela do usuário.
    #
    # O método calcula o tamanho atual da janela e o
    # tamanho do monitor para determinar a posição
    # ideal onde a janela deve ser exibida.
    def allign_window(self):
        # Atualiza todos os componentes pendentes da interface.
        #
        # Isso garante que a janela já possua largura e altura
        # corretas antes dos cálculos de posicionamento.
        self.update_idletasks()

        # Obtém a largura atual da janela em pixels.
        width = self.winfo_width()

        # Obtém a altura atual da janela em pixels.
        height = self.winfo_height()

        # Obtém a largura total da tela do usuário.
        screen_w = self.winfo_screenwidth()

        # Obtém a altura total da tela do usuário.
        screen_h = self.winfo_screenheight()

        # Calcula a posição horizontal da janela.
        #
        # Subtrai a largura da janela da largura da tela
        # e divide o resultado por 2 para posicioná-la
        # no centro horizontalmente.
        x = (screen_w - width) // 2

        # Calcula a posição vertical da janela.
        #
        # Divide por 3 em vez de 2 para deixar a janela
        # um pouco mais próxima da parte superior da tela,
        # em vez de ficar exatamente centralizada.
        y = (screen_h - height) // 3

        # Define o tamanho e a posição da janela.
        #
        # Formato:
        # largura x altura + posiçãoX + posiçãoY
        #
        # Exemplo:
        # 900x520+200+100
        self.geometry(
            f"{width}x{height}+{x}+{y}"
        )

    # Cria e organiza os campos do formulário utilizados
    # para cadastrar, editar e pesquisar pessoas.
    #
    # Todos os componentes criados neste método serão
    # exibidos na parte superior da janela.
    def build_form(self):

        # Cria um Frame que servirá como contêiner para
        # todos os campos do formulário.
        #
        # Um Frame funciona como uma área de organização,
        # permitindo agrupar componentes relacionados.
        form = ttk.Frame(self)

        # Exibe o formulário na parte superior da janela.
        #
        # side=tk.TOP:
        #     Posiciona o frame na parte superior.
        #
        # fill=tk.X:
        #     Faz o frame ocupar toda a largura disponível.
        #
        # padx e pady:
        #     Adicionam espaçamento externo.
        form.pack(
            side=tk.TOP,
            fill=tk.X,
            padx=10,
            pady=10
        )

        # Cria um rótulo para identificar o campo ID.
        #
        # sticky="e":
        #     Alinha o texto à direita da célula.
        #     "e" significa East (Leste).
        ttk.Label(
            form,
            text="ID:"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="e"
        )

        # Cria o campo utilizado para exibir o ID da pessoa.
        #
        # textvariable=self.var_id:
        #     Vincula o campo à variável var_id.
        #
        # width=8:
        #     Define a largura do campo.
        #
        # state="readonly":
        #     Impede que o usuário altere o ID manualmente.
        #     O valor será preenchido pelo sistema.
        ttk.Entry(
            form,
            textvariable=self.var_id,
            width=8,
            state="readonly"
        ).grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky="w"
        )

        # Rótulo utilizado para identificar o campo nome.
        ttk.Label(
            form,
            text="Nome:"
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=5,
            sticky="e"
        )

        # Campo onde o usuário informa o nome da pessoa.
        #
        # O valor digitado será armazenado na variável
        # self.var_nome.
        ttk.Entry(
            form,
            textvariable=self.var_nome,
            width=40
        ).grid(
            row=0,
            column=3,
            padx=5,
            pady=5,
            sticky="w"
        )

        # Rótulo que identifica o campo de e-mail.
        ttk.Label(
            form,
            text="E-mail:"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="e"
        )

        # Campo utilizado para armazenar o e-mail da pessoa.
        #
        # O conteúdo digitado será armazenado em
        # self.var_email.
        ttk.Entry(
            form,
            textvariable=self.var_email,
            width=40
        ).grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
            sticky="w"
        )

        # Rótulo que identifica o campo telefone.
        ttk.Label(
            form,
            text="Telefone:"
        ).grid(
            row=1,
            column=2,
            padx=5,
            pady=5,
            sticky="e"
        )

        # Campo utilizado para informar o telefone.
        #
        # O valor digitado será armazenado em
        # self.var_telefone.
        ttk.Entry(
            form,
            textvariable=self.var_telefone,
            width=22
        ).grid(
            row=1,
            column=3,
            padx=5,
            pady=5,
            sticky="w"
        )

        # Rótulo utilizado para identificar o campo
        # de pesquisa.
        ttk.Label(
            form,
            text="Pesquisar:"
        ).grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky="e"
        )

        # Campo utilizado para pesquisar registros.
        #
        # O usuário poderá informar parte do nome,
        # e-mail ou outras informações utilizadas
        # na pesquisa.
        #
        # columnspan=3:
        #     Faz o campo ocupar três colunas da grade,
        #     permitindo uma área maior para digitação.
        ttk.Entry(
            form,
            textvariable=self.var_search,
            width=60
        ).grid(
            row=2,
            column=1,
            columnspan=3,
            padx=5,
            pady=5,
            sticky="w"
        )

        # Permite que a coluna 3 aumente ou diminua
        # automaticamente quando a janela for redimensionada.
        #
        # weight=1:
        #     Define que essa coluna pode receber
        #     parte do espaço extra disponível.
        form.grid_columnconfigure(
            3,
            weight=1
        )

    # Cria e organiza os botões responsáveis pelas
    # principais funcionalidades do sistema.
    #
    # Os botões permitem cadastrar, atualizar,
    # excluir, pesquisar registros, limpar os
    # campos do formulário e exportar os dados
    # para uma planilha Excel.
    def build_button(self):
        # Cria um Frame que servirá como contêiner
        # para todos os botões da aplicação.
        form = ttk.Frame(self)

        # Exibe o frame na parte superior da janela.
        #
        # side=tk.TOP:
        #     Posiciona o frame no topo da interface.
        #
        # fill=tk.X:
        #     Faz o frame ocupar toda a largura disponível.
        #
        # padx e pady:
        #     Adicionam espaçamento externo para melhorar
        #     a organização visual dos componentes.
        form.pack(
            side=tk.TOP,
            fill=tk.X,
            padx=10,
            pady=5
        )

        # Cria o botão responsável por cadastrar
        # uma nova pessoa no banco de dados.
        #
        # command=self.auth:
        #     Método executado quando o usuário
        #     clicar no botão.
        ttk.Button(
            form,
            text="Cadastrar",
            command=self.auth
        ).pack(
            side=tk.LEFT,
            padx=5,
            pady=5
        )

        # Cria o botão responsável por atualizar
        # os dados da pessoa selecionada.
        #
        # O método update() será executado quando
        # o usuário clicar no botão.
        ttk.Button(
            form,
            text="Atualizar",
            command=self.update
        ).pack(
            side=tk.LEFT,
            padx=5,
            pady=5
        )

        # Cria o botão responsável por excluir
        # a pessoa atualmente selecionada.
        #
        # O método exclude() será executado quando
        # o usuário clicar no botão.
        ttk.Button(
            form,
            text="Excluir",
            command=self.exclude
        ).pack(
            side=tk.LEFT,
            padx=5,
            pady=5
        )

        # Cria o botão responsável por limpar
        # todos os campos do formulário.
        #
        # Essa operação não remove registros
        # do banco de dados.
        #
        # Apenas limpa os campos da interface
        # para permitir um novo preenchimento.
        #
        # O mesmo comportamento também pode ser
        # executado através do atalho CTRL + N.
        ttk.Button(
            form,
            text="Limpar (ou CTRL + N)",
            command=self.clean_fields
        ).pack(
            side=tk.LEFT,
            padx=5,
            pady=5
        )

        # Cria o botão responsável por pesquisar
        # registros utilizando o texto informado
        # pelo usuário no campo de busca.
        #
        # O método search() será executado quando
        # o botão for pressionado.
        ttk.Button(
            form,
            text="Pesquisar",
            command=self.search
        ).pack(
            side=tk.LEFT,
            padx=5,
            pady=5
        )

        # Cria o botão responsável por exportar
        # os registros para um arquivo Excel (.xlsx).
        #
        # command=self.export_excel:
        #     Executa o método responsável pela
        #     geração da planilha.
        #
        # side=tk.RIGHT:
        #     Posiciona o botão no lado direito
        #     do frame, destacando-o dos demais.
        ttk.Button(
            form,
            text="Exportar para Excel",
            command=self.export_excel
        ).pack(
            side=tk.RIGHT,
            padx=5,
            pady=5
        )

    # Cria e configura a tabela responsável por exibir
    # os registros cadastrados no sistema.
    #
    # A tabela será utilizada para visualizar os dados,
    # selecionar registros e realizar ordenações.
    def build_table(self):
        # Cria um LabelFrame para agrupar visualmente
        # a tabela de registros.
        #
        # LabelFrame é um Frame com título, utilizado
        # para organizar componentes relacionados.
        form = ttk.LabelFrame(
            self,
            text="Registros"
        )

        # Exibe o LabelFrame na janela principal.
        #
        # side=tk.TOP:
        #     Posiciona o componente na parte superior.
        #
        # fill=tk.BOTH:
        #     Faz o componente ocupar toda a largura
        #     e altura disponíveis.
        #
        # expand=True:
        #     Permite que o componente cresça quando
        #     a janela for redimensionada.
        form.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10
        )

        # Define os identificadores internos das colunas.
        #
        # Esses nomes serão utilizados pelo Tkinter
        # para identificar cada coluna da Treeview.
        cols = (
            "id",
            "nome",
            "email",
            "tel",
            "dateCreation"
        )

        # Cria a Treeview.
        #
        # A Treeview funciona como uma tabela onde
        # serão exibidos os registros do banco.
        #
        # columns=cols:
        #     Define quais colunas existirão.
        #
        # show="headings":
        #     Exibe apenas os cabeçalhos e os dados,
        #     ocultando a coluna de árvore padrão
        #     da Treeview.
        #
        # selectmode="browse":
        #     Permite selecionar apenas uma linha
        #     por vez.
        self.tree = ttk.Treeview(
            form,
            columns=cols,
            show="headings",
            selectmode="browse"
        )

        # Configura o cabeçalho da coluna ID.
        #
        # text:
        #     Texto exibido no cabeçalho.
        #
        # command:
        #     Define uma ação executada quando
        #     o usuário clicar no título da coluna.
        #
        # lambda:
        #     Cria uma função temporária que será
        #     executada apenas no momento do clique.
        #
        # self.orderBy(0):
        #     Solicita a ordenação dos registros
        #     pela primeira coluna da tabela.
        self.tree.heading(
            "id",
            text="ID",
            command=lambda: self.orderBy(0)
        )

        # Cabeçalho da coluna Nome.
        #
        # Ao clicar em "Nome", a tabela será
        # ordenada pela coluna de nomes.
        self.tree.heading(
            "nome",
            text="Nome",
            command=lambda: self.orderBy(1)
        )

        # Cabeçalho da coluna Email.
        self.tree.heading(
            "email",
            text="Email",
            command=lambda: self.orderBy(2)
        )

        # Cabeçalho da coluna Telefone.
        self.tree.heading(
            "tel",
            text="Telefone",
            command=lambda: self.orderBy(3)
        )

        # Cabeçalho da coluna Data de criação.
        self.tree.heading(
            "dateCreation",
            text="Data de criação",
            command=lambda: self.orderBy(4)
        )

        # Configura a coluna ID.
        #
        # width:
        #     Define a largura da coluna em pixels.
        #
        # anchor="center":
        #     Centraliza o conteúdo da coluna.
        self.tree.column(
            "id",
            width=60,
            anchor="center"
        )

        # Configura a coluna Nome.
        #
        # anchor="w":
        #     Alinha o texto à esquerda.
        #     "w" significa West (Oeste).
        self.tree.column(
            "nome",
            width=260,
            anchor="w"
        )

        # Configura a coluna Email.
        self.tree.column(
            "email",
            width=140,
            anchor="w"
        )

        # Configura a coluna Telefone.
        self.tree.column(
            "tel",
            width=260,
            anchor="center"
        )

        # Configura a coluna Data de criação.
        self.tree.column(
            "dateCreation",
            width=160,
            anchor="center"
        )

        # Cria uma barra de rolagem vertical.
        #
        # orient="vertical":
        #     Define uma barra vertical.
        #
        # command=self.tree.yview:
        #     Quando o usuário movimentar a barra,
        #     a tabela será movimentada para cima
        #     ou para baixo.
        vsb = ttk.Scrollbar(
            form,
            orient="vertical",
            command=self.tree.yview
        )

        # Cria uma barra de rolagem horizontal.
        #
        # command=self.tree.xview:
        #     Permite mover a tabela para a esquerda
        #     ou para a direita quando necessário.
        hsb = ttk.Scrollbar(
            form,
            orient="horizontal",
            command=self.tree.xview
        )

        # Conecta a Treeview às barras de rolagem.
        #
        # Sempre que a tabela se movimentar,
        # as barras terão sua posição atualizada.
        self.tree.configure(
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )

        # Exibe a barra vertical no lado direito
        # da tabela.
        vsb.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        # Exibe a barra horizontal na parte inferior
        # da tabela.
        hsb.pack(
            side=tk.BOTTOM,
            fill=tk.X
        )

        # Exibe a tabela dentro do LabelFrame.
        #
        # fill=tk.BOTH:
        #     Faz a tabela ocupar toda a área disponível.
        #
        # expand=True:
        #     Permite que a tabela cresça quando
        #     a janela for redimensionada.
        self.tree.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        # Aplica um estilo de linhas alternadas
        # (efeito zebra), facilitando a leitura
        # dos registros exibidos.
        apply_zebra_treeview(self.tree)

        # Associa um evento à tabela.
        #
        # bind():
        #     Utilizado para vincular eventos da
        #     interface gráfica a métodos Python.
        #
        # "<Double-1>":
        #     Evento disparado quando o usuário
        #     realiza dois cliques consecutivos
        #     com o botão esquerdo do mouse.
        #
        # self.on_doubleClick:
        #     Método executado quando o evento ocorrer.
        #
        # Normalmente esse método recupera os dados
        # da linha selecionada e preenche os campos
        # do formulário para edição.
        self.tree.bind(
            "<Double-1>",
            self.on_doubleClick
        )









