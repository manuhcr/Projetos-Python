import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime,date
from typing import List, Dict
from repositorio import RepoProdutos
from modelos import Produto


def formatarMoedaBR(valor: float) -> str:

    string = f"{valor:.2f}"

    return f"R$ {string.replace(',','x').replace('.',',')
    .replace('x', '.')}"

def converterPrecoBR(text: str) -> float:

    text = (text or "").strip()

    if not text:
        raise ValueError("Informe o preço do produto.")

    text = text.replace(',', '').replace(',', '.')


    return float(text)

def formatarDataBR(data: date) -> str:

    return data.strftime('%d/%m/%Y')

def converterDataBR(text: str) -> date:

    return datetime.strptime(text.strip(), '%d/%m/%Y').date()


class appDestacarCelulas(tk.Tk):

    corColunaBG = "#77D584"
    corColunaTXT = "#FAFFF1"
    corLinhaBG = "#B2FADB"
    corLinhaTXT = "#FAFFF1"
    corCelulaBG = "#A6979C"
    corCelulaTXT = "#FAFFF1"

    def __init__(self):

        super().__init__()

        self.title("Tabela: destaque de Linha e Coluna")
        self.centralizarJanela(1280, 680)
        self.minsize(1280, 680)
        self.repo = RepoProdutos()
        self.dadosLista: List[Produto] = []
        self.mapearIdProd: Dict[str, Produto] = {}
        self.colunaSelecionada = None
        self.itemSelecionado = None
        self.configurarEstilo()
        self.varBusca = tk.StringVar()
        self.varCategoriaProduto = tk.StringVar()
        self.varNomeProduto = tk.StringVar()
        self.varPrecoProduto = tk.StringVar()
        self.varEstoque = tk.StringVar()
        self.varDataProduto = tk.StringVar()
        self.montarEstilo()
        self.carregarDados()
        self.popularTabela()
        self.desenharColuna()


    def centralizarJanela(self, larg: int, alt: int):

        self.update_idletasks()

        telaLargura , telaAltura = self.winfo_screenwidth(), self.winfo_screenheight()

        x = (telaLargura // 2) - (larg // 2)
        y = (telaAltura // 2) - (alt // 2)

        self.geometry(f"{larg}x{alt}+{x}+{y}")

    def configurarEstilo(self):

        estilo = ttk.Style(self)

        try:
            estilo.theme_use(estilo.theme_use())

        except tk.TclError:
            pass

        estilo.configure("Treeview", font=("Jost", 11) , rowheight=28)
        estilo.configure("Treeview.Heading", font=("Jost", 11, "bold"))
        estilo.configure("Big.TButton", padding = (10,6))
        estilo.configure("Form.TEntry", padding = 4)

    def montarEstilo(self):

        barraBusca = ttk.Frame(self)

        barraBusca.pack(fill="both", padx = 12, pady = (12,6))

        ttk.Label(barraBusca, text="Pesquisar categoria ou nome do produto:").pack(side="left")

        entradaBusca = ttk.Entry(barraBusca, textvariable=self.varBusca, width = 36)

        entradaBusca.pack(side="left", padx = 6)

        ttk.Button(
            barraBusca,
            text = "Buscar",
            command = self.buscarProduto,
            style = "Big.TButton"

        ).pack(side="right", padx = (8, 6))

        ttk.Button(
            barraBusca,
            text="Limpar barra de pesquisa",
            command=self.limparPesquisa,
        ).pack(side="left")

        corpo = ttk.Frame(self)

        corpo.pack(fill="both", expand= True, padx = 12, pady = (0, 8))

        quadro = ttk.LabelFrame(
            corpo,
            text = "Produtos (clique em uma célula para destacar coluna + linha)"
        )

        quadro.pack(side="left", fill="both", expand= True, pady = (0, 8))

        tabelaContainer = ttk.Frame(quadro)

        tabelaContainer.pack(fill="both", expand= True, padx = 6, pady = 6)

        self.colunas = ("categoriaProduto" , "nomeProduto" , "precoProduto" ,
                        "estoque" , "dataProduto")

        self.tree = ttk.Treeview(tabelaContainer,
                                 columns= self.colunas,
                                 show="headings",
                                 selectmode = "browse")

        headers = {
            "categoriaProduto": "Categoria",
            "nomeProduto": "Nome do produto",
            "precoProduto": "Preço",
            "estoque": "Estoque",
            "dataProduto": "Data de criação"
        }

        for coluna, texto in headers.items():
            self.tree.heading(coluna, text=texto)

        self.tree.column("categoriaProduto", width=180, minwidth=120,
                         anchor = "w", stretch= True)
        self.tree.column("nomeProduto", width=340, minwidth=160,
                         anchor = "w", stretch= True)
        self.tree.column("precoProduto", width=120, minwidth=90,
                         anchor = "e", stretch= False)
        self.tree.column("estoque", width=110, minwidth=80,
                         anchor = "center", stretch= False)
        self.tree.column("dataProduto", width=110, minwidth=80,
                         anchor = "center", stretch= False)

        self.barraScrollVertical = ttk.Scrollbar(
            tabelaContainer,
            orient="vertical",
            command=self.onVScroll
        )

        self.barraScrollHorizontal = ttk.Scrollbar(
            tabelaContainer,
            orient="horizontal",
            command=self.onHScroll
        )

        self.tree.configure(
            yscrollcommand = self.ysync,
            xscrollcommand= self.xsync
        )

        tabelaContainer.rowconfigure(0, weight=1)

        tabelaContainer.columnconfigure(0, weight=1)

        self.tree.grid(row=0, column=0, sticky="nsew")

        self.barraScrollVertical.grid(row=0, column=1, sticky="ns")

        self.barraScrollHorizontal.grid(row=1, column=0, sticky="ew")

        self.overlay = tk.Canvas(
            self.tree,
            highlightthickness=0,
            bd=0,
            bg=self.treeBGColor()
        )

        self.overlay.place_forget()

        self.overlay.bind("<Button-1>",
                          lambda e: self.tree.event_generate("<Button-1>", x=e.x, y=e.y))

        self.overlay.bind("<ButtonRelease-1>",
                          lambda e: self.tree.event_generate("<ButtonRelease-1>", x=e.x, y=e.y))

        self.overlay.bind("<Double-Button-1>",
                          lambda e: self.tree.event_generate("Double-Button-1>", x=e.x, y=e.y))

        self.overlay.bind("<MouseWheel>",
                          lambda e: self.tree.event_generate("MouseWheel>", delta=e.delta))

        self.overlay.bind("<Button-4>", lambda e: self.tree.event_generate("<Button-4>"))

        self.overlay.bind("<Button-5>", lambda e: self.tree.event_generate("<Button-5>"))

        self.tree.tag_configure("oddrow", background= "#FFFFFF")

        self.tree.tag_configure("evenrow", background= "#D7FCEC")

        self.tree.tag_configure("rowSel" , background= self.corLinhaSel)

        self.tree.bind("<Button-1>", self.onClick)

        self.tree.bind("<<TreeviewSelect>>", self.onSelectRow)





