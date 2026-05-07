import tkinter as tk  # Importa a biblioteca Tkinter para criar a interface gráfica do usuário
from pydoc import text
# (GUI) do sistema de cadastro. Tkinter é uma biblioteca padrão do Python para desenvolvimento de interfaces gráficas.

from tkinter import ttk, messagebox, filedialog  # Importa módulos específicos da biblioteca Tkinter: ttk para widgets temáticos,
# messagebox para exibir mensagens de alerta e filedialog para abrir diálogos de seleção de arquivos.


from openpyxl import Workbook  # Importa a classe Workbook da biblioteca openpyxl, que é usada para criar e manipular arquivos do Excel (.xlsx).

from openpyxl.utils import get_column_letter  # Importa a função get_column_letter da biblioteca openpyxl.utils,
# que é usada para converter números de coluna em letras (por exemplo, 1 para 'A', 2 para 'B', etc.) ao trabalhar com arquivos do Excel.

from db import conectar  # Importa a função conectar do módulo db, que é responsável por estabelecer a conexão com o banco de dados MySQL.
from repo import PessoaRepo
from style import apply_style , apply_zebra_treeview, field_treeview


def validate(nome: str, telefone: str, email: str):
    # A função validate é responsável por validar os dados de entrada fornecidos pelo usuário para o cadastro de pessoas.
    # Ela verifica se os campos de nome, telefone e email estão preenchidos corretamente,
    # garantindo que os dados sejam válidos antes de serem processados pelo sistema de cadastro.

    if not nome:
        return False , "Erro de Validação", "O campo 'Nome' é obrigatório."

    if not telefone:
        return False, "Erro de Validação", "O campo 'Telefone' é obrigatório."

    if not email:
        return False, "Erro de Validação", "O campo 'Email' é obrigatório."

    if len(nome.strip()) < 3:
        return False , "Erro de Validação", "Informe um nome que contenha pelo menos 3 caracteres."

    if not "@" in email or not "." in email:
        return False, "Erro de Validação", "Informe um email válido."

    if len(telefone.strip()) < 8:
        return False,"Erro de Validação", "Informe um telefone válido, contendo apenas números e pelo menos 8 dígitos."

    return True  # Se todas as validações forem bem-sucedidas, a função retorna True, indicando que os dados de entrada são válidos
    # e podem ser processados pelo sistema de cadastro.


class AppCadastro(tk.Tk):
    def __init__(self):
        # A classe AppCadastro é a classe principal do aplicativo de cadastro de pessoas, que herda da classe tk.Tk (classe pai, por isso super) da biblioteca Tkinter.
        super().__init__()
        self.title(
            "Sistema de Cadastro de Pessoas - Tkinter + MySQL")  # Define o título da janela do aplicativo como "Sistema de Cadastro de Pessoas".

        self.minsize(900,
                     520)  # Define o tamanho mínimo da janela do aplicativo para 900 pixels de largura e 520 pixels de altura.

        apply_style(self)

        self.conn = conectar(usar_banco=True)

        self.repo = PessoaRepo(self.conn)

        self.var_id = tk.StringVar()

        self.var_nome = tk.StringVar()

        self.var_telefone = tk.StringVar()

        self.var_email = tk.StringVar()

        self.var_search = tk.StringVar()

        self.var_status = tk.StringVar(value="Pronto.")

        self.build_form()

        self.build_button()

        self.build_table()

        self.build_statusbar(

        self.allign_window())

        self.bind("<Control-n>" , lambda e: self.clean_fields())

        self.bind("<F5>" , lambda e: self.listAll())

        self.list_all()

        self.protocol("VM_DELETE_WINDOW" , lambda e: self._fechar_())

    def allign_window(self):

        self.update_idletasks()

        width = self.winfo_width()

        height = self.winfo_height()

        screen_w = self.winfo_screenwidth()

        screen_h = self.winfo_screenheight()

        x = (screen_w - width) // 2
        y = (screen_h - height) // 3

        self.geometry(f"f{width}x{height}+{x}+{y}")

    def build_form(self):

        form = ttk.Frame(self , text= "Dados da Pessoa")

        form.pack(side=tk.TOP, fill=tk.X , padx=10, pady=10)

        ttk.Label(form, text= "ID: ").grid(row=0, column=0, padx=10, pady=10, sticky = "e")

        ttk.Entry(form, textvariable= self.var_id, width=8, state="readonly").grid(row=0, column= 1, padx=5, pady=5, sticky = "w")

        ttk.Label(form, text="Nome:").grid(row=0, column=2, padx=5, pady=5, sticky= "e")

        ttk.Entry(form, textvariable= self.var_nome, width=40).grid(row=0, column= 3, padx=5, pady=5, sticky = "w")

        ttk.Label(form, text="E-mail:").grid(row=1, column=0, padx=5, pady=5, sticky= "e")

        ttk.Entry(form, textvariable= self.var_email, width=40).grid(row=1, column= 1, padx=5, pady=5, sticky = "w")

        ttk.Label(form, text="Telefone:").grid(row=1, column=2, padx=5, pady=5 , sticky= "e")

        ttk.Entry(form, textvariable=self.var_telefone, width=22).grid(row=1, column=3, padx=5, pady=5, sticky = "w")

        ttk.Label(form, text="Pesquisar: ").grid(row=2, column=0, padx=5, pady=5, sticky= "e")

        ttk.Entry(form, textvariable= self.var_search, width=60).grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky = "w")

        form.grid_columnconfigure(3, weight=1)

    def build_button(self):

        form = ttk.Frame(self)

        form.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        ttk.Button(form, text= "Cadastrar", command=self.auth).pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Button(form, text= "Atualizar" , command=self.update).pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Button(form, text="Excluir", command=self.exclude).pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Button(form, text= "Limpar (ou CNTRL + N)" , command=self.clean_fields).pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Button(form, text= "Pesquisar", command=self.search).pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Button(form, text= "Exportar para Excel" , command=self.export_excel).pack(side=tk.RIGHT, padx=5, pady=5)


    def build_table(self):

        form = ttk.Labelframe(self, text= "Registros")

        form.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        cols = ("id" , "nome" , "email" , "tel", "dateCreation" )

        self.tree = ttk.Treeview(form, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID", command= lambda: self.orderBy(0))

        self.tree.heading("nome", text="Nome", command= lambda: self.orderBy(1))

        self.tree.heading("email" , text= "Email", command= lambda: self.orderBy(2))

        self.tree.heading("tel" , text= "Telefone" , command= lambda: self.orderBy(3))

        self.tree.heading("dateCreation" , text= "Data de criação" , command= lambda: self.orderBy(4))

        self.tree.column("id", width=60, anchor="center")

        self.tree.column("nome" , width=260, anchor="w")

        self.tree.column("email", width=140, anchor="w")

        self.tree.column("tel" , width=260, anchor="center")

        self.tree.column("dateCreation" , width=160, anchor="center")

        vsb = ttk.Scrollbar(form, orient="vertical", command=self.tree.yview)

        hsb = ttk.Scrollbar(form, orient="horizontal", command=self.tree.xview)

        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        apply_zebra_treeview(self.tree)

        self.tree.bind("<Double-1>" , self.on_doubleClick)









