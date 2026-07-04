# ----------------------------------------------------
# IMPORTAÇÕES
# ----------------------------------------------------

# Biblioteca principal do Tkinter.
#
# Contém os componentes básicos para
# criar interfaces gráficas.
import tkinter as tk

# ttk contém versões mais modernas
# dos componentes do Tkinter.
#
# Exemplo:
# • Button
# • Label
# • Entry
# • Treeview
#
# messagebox é utilizada para exibir
# janelas de mensagens, avisos,
# confirmações e erros.
from tkinter import ttk, messagebox

# datetime é utilizado para trabalhar
# com datas e horários.
#
# datetime:
# representa data + hora.
#
# date:
# representa apenas uma data.
from datetime import datetime, date

# Importa tipos utilizados para criar
# anotações de tipo (Type Hints).
#
# List:
# representa uma lista.
#
# Dict:
# representa um dicionário.
from typing import List, Dict

# Classe responsável por acessar
# o banco de dados.
#
# Nela estão os métodos de CRUD,
# pesquisa e consultas.
from repositorio import RepoProdutos

# Classe que representa um Produto.
#
# Cada objeto Produto corresponde
# a um registro da tabela produtos.
from modelos import Produto


# ----------------------------------------------------
# FUNÇÕES AUXILIARES
# ----------------------------------------------------

# Converte um número (float) para o
# formato monetário brasileiro.
#
# Exemplo:
#
# 1500.5
#
# ↓
#
# R$ 1.500,50
#
# Essa função será utilizada para
# exibir os preços ao usuário.
def formatarMoedaBR(valor: float) -> str:

    # Formata o número com duas
    # casas decimais.
    string = f"{valor:.2f}"

    # Troca os separadores para
    # o padrão brasileiro.
    #
    # "." → separador de milhares
    # "," → separador decimal
    return (
        f"R$ {string.replace(',', 'x')
                  .replace('.', ',')
                  .replace('x', '.')}"
    )


# Converte um preço digitado pelo
# usuário para float.
#
# Exemplo:
#
# "1.250,90"
#
# ↓
#
# 1250.90
#
# Isso é necessário porque o Python
# trabalha com ponto como separador
# decimal.
def converterPrecoBR(text: str) -> float:

    # Remove espaços no início
    # e no final da string.
    text = (text or "").strip()

    # Verifica se o usuário digitou
    # algum valor.
    if not text:
        raise ValueError(
            "Informe o preço do produto."
        )

    # Converte o número do formato
    # brasileiro para o formato aceito
    # pelo Python.
    #
    # Exemplo:
    #
    # 1.250,90
    #
    # ↓
    #
    # 1250.90
    text = (
        text.replace(".", "")
            .replace(",", ".")
    )

    return float(text)


# Converte um objeto date para uma
# string no formato brasileiro.
#
# Exemplo:
#
# date(2025, 8, 14)
#
# ↓
#
# "14/08/2025"
def formatarDataBR(data: date) -> str:

    return data.strftime("%d/%m/%Y")


# Converte uma data digitada pelo
# usuário para um objeto date.
#
# Exemplo:
#
# "14/08/2025"
#
# ↓
#
# date(2025, 8, 14)
#
# Isso facilita salvar a data
# corretamente no banco de dados.
def converterDataBR(text: str) -> date:

    return datetime.strptime(
        text.strip(),
        "%d/%m/%Y"
    ).date()

# Classe principal da aplicação.
#
# Ela herda de tk.Tk, ou seja,
# passa a ser uma janela do Tkinter.
#
# Todos os componentes da interface
# serão criados dentro dessa classe.
class appDestacarCelulas(tk.Tk):

    # ----------------------------------------------------
    # CORES UTILIZADAS PELA APLICAÇÃO
    # ----------------------------------------------------
    #
    # Essas variáveis pertencem à classe,
    # ou seja, todos os objetos criados
    # a partir dela utilizarão essas cores.
    #
    # Elas serão usadas para destacar
    # linhas, colunas e células da Treeview.
    corColunaBG = "#77D584"
    corColunaTXT = "#FAFFF1"

    corLinhaBG = "#B2FADB"
    corLinhaTXT = "#FAFFF1"

    corCelulaBG = "#A6979C"
    corCelulaTXT = "#FAFFF1"

    # Método construtor.
    #
    # É executado automaticamente quando
    # fazemos:
    #
    # app = appDestacarCelulas()
    #
    # Sua função é preparar toda a aplicação
    # antes da janela aparecer na tela.
    def __init__(self):
        # Executa o construtor da classe Tk.
        #
        # É essa linha que realmente cria
        # a janela da aplicação.
        #
        # Sem ela, a janela do Tkinter
        # não existiria.
        super().__init__()

        # Define o título exibido
        # na barra superior da janela.
        self.title(
            "Tabela: destaque de Linha e Coluna"
        )

        # Centraliza a janela
        # na tela do usuário.
        self.centralizarJanela(
            1280,
            680
        )

        # Define o tamanho mínimo.
        #
        # O usuário poderá aumentar
        # a janela, mas nunca diminuir
        # abaixo desse tamanho.
        self.minsize(
            1280,
            680
        )

        # Cria o objeto responsável por
        # acessar o banco de dados.
        #
        # Toda operação de CRUD será feita
        # através desse objeto.
        self.repo = RepoProdutos()

        # Lista onde serão armazenados
        # todos os produtos carregados
        # do banco de dados.
        #
        # Cada posição dessa lista
        # contém um objeto Produto.
        self.dadosLista: List[Produto] = []

        # Dicionário utilizado para localizar
        # rapidamente um produto através
        # do seu ID.
        #
        # Chave:
        # id do produto.
        #
        # Valor:
        # objeto Produto correspondente.
        self.mapearIdProd: Dict[str, Produto] = {}

        # Armazena qual coluna da
        # Treeview está selecionada.
        #
        # Inicialmente nenhuma coluna
        # foi selecionada.
        self.colunaSelecionada = None

        # Armazena qual linha da
        # Treeview está selecionada.
        #
        # Inicialmente nenhuma linha
        # foi selecionada.
        self.itemSelecionado = None

        # Configura os estilos da aplicação.
        #
        # Aqui são definidas cores,
        # fontes e aparência dos
        # componentes ttk.
        self.configurarEstilo()

        # ----------------------------------------------------
        # VARIÁVEIS DA INTERFACE
        # ----------------------------------------------------
        #
        # StringVar é uma variável especial
        # do Tkinter.
        #
        # Ela permite que um componente
        # da interface (como uma Entry)
        # fique sincronizado com uma
        # variável do programa.
        #
        # Quando o usuário digita em uma
        # Entry ligada a uma StringVar,
        # o valor da variável é atualizado
        # automaticamente.

        # Texto digitado na pesquisa.
        self.varBusca = tk.StringVar()

        # Categoria do produto.
        self.varCategoriaProduto = tk.StringVar()

        # Nome do produto.
        self.varNomeProduto = tk.StringVar()

        # Preço do produto.
        self.varPrecoProduto = tk.StringVar()

        # Quantidade em estoque.
        self.varEstoque = tk.StringVar()

        # Data de criação.
        self.varDataProduto = tk.StringVar()

        # Cria toda a interface gráfica.
        #
        # Aqui são criados:
        #
        # • Frames;
        # • Labels;
        # • Entrys;
        # • Botões;
        # • Treeview;
        # • Scrollbars.
        self.montarEstilo()

        # Carrega todos os produtos
        # existentes no banco de dados.
        self.carregarDados()

        # Insere os produtos carregados
        # dentro da Treeview.
        self.popularTabela()

        # Desenha o destaque inicial
        # da coluna selecionada.
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

        # Cria um Frame.
        #
        # Um Frame funciona como uma "caixa"
        # utilizada para organizar outros
        # componentes da interface.
        #
        # Ele não aparece como um botão ou
        # uma caixa de texto. Sua função é
        # apenas servir como um organizador.
        #
        # Neste caso, ele armazenará toda a
        # barra de pesquisa.
        barraBusca = ttk.Frame(self)

        # pack() posiciona o Frame na janela.
        #
        # fill="both"
        # Faz o Frame ocupar toda a largura
        # e altura disponíveis.
        #
        # padx
        # Espaçamento horizontal externo.
        #
        # pady
        # Espaçamento vertical externo.
        barraBusca.pack(fill="both", padx=12, pady=(12, 6))

        # Cria um Label.
        #
        # Label é um componente utilizado
        # apenas para exibir textos.
        #
        # Neste caso ele serve como uma
        # descrição para a caixa de pesquisa.
        ttk.Label(
            barraBusca,
            text="Pesquisar categoria ou nome do produto:"
        ).pack(side="left")

        # Cria uma Entry.
        #
        # Entry é uma caixa de texto onde o
        # usuário poderá digitar informações.
        #
        # O parâmetro textvariable conecta
        # essa Entry à variável self.varBusca.
        #
        # Assim, o texto digitado poderá ser
        # obtido futuramente utilizando:
        #
        # self.varBusca.get()
        entradaBusca = ttk.Entry(
            barraBusca,
            textvariable=self.varBusca,
            width=36
        )

        # Posiciona a Entry ao lado do Label.
        entradaBusca.pack(side="left", padx=6)

        # Cria o botão "Buscar".
        #
        # Button representa um botão clicável.
        #
        # Quando o usuário clicar nele,
        # será executado o método
        # buscarProduto().
        ttk.Button(
            barraBusca,
            text="Buscar",
            command=self.buscarProduto
        ).pack(side="right", padx=(8, 6))

        # Botão utilizado para limpar
        # o texto digitado na pesquisa.
        #
        # Ao clicar nele será executado
        # o método limparPesquisa().
        ttk.Button(
            barraBusca,
            text="Limpar barra de pesquisa",
            command=self.limparPesquisa
        ).pack(side="left")

        # Cria o Frame principal da aplicação.
        #
        # Esse Frame armazenará toda a área
        # central da interface.
        #
        # Dentro dele serão colocados:
        #
        # • A tabela (Treeview)
        # • As barras de rolagem
        # • Outros componentes da tela
        corpo = ttk.Frame(self)

        corpo.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 8)
        )

        # Cria um LabelFrame.
        #
        # LabelFrame é semelhante ao Frame,
        # porém possui uma borda e um título.
        #
        # É utilizado para separar visualmente
        # grupos de componentes.
        quadro = ttk.LabelFrame(
            corpo,
            text="Produtos (clique em uma célula para destacar coluna + linha)"
        )

        quadro.pack(
            side="left",
            fill="both",
            expand=True,
            pady=(0, 8)
        )

        # Frame utilizado apenas para
        # organizar a Treeview juntamente
        # com as barras de rolagem.
        tabelaContainer = ttk.Frame(quadro)

        tabelaContainer.pack(
            fill="both",
            expand=True,
            padx=6,
            pady=6
        )

        # Tupla contendo os nomes internos
        # das colunas da tabela.
        #
        # Esses nomes serão utilizados para
        # acessar cada coluna pelo código.
        #
        # Eles NÃO são os textos exibidos
        # ao usuário.
        self.colunas = (
            "categoriaProduto",
            "nomeProduto",
            "precoProduto",
            "estoque",
            "dataProduto"
        )

        # Cria uma Treeview.
        #
        # A Treeview é um componente do Tkinter
        # utilizado para exibir dados em formato
        # de tabela.
        #
        # Ela funciona de maneira semelhante
        # a uma planilha do Excel.
        #
        # Cada linha representa um produto.
        #
        # Cada coluna representa uma informação
        # desse produto.
        #
        # columns
        # Recebe a lista das colunas que
        # existirão na tabela.
        #
        # show="headings"
        # Exibe apenas os cabeçalhos,
        # escondendo a primeira coluna
        # interna da Treeview.
        #
        # selectmode="browse"
        # Permite selecionar apenas uma
        # linha por vez.
        self.tree = ttk.Treeview(
            tabelaContainer,
            columns=self.colunas,
            show="headings",
            selectmode="browse"
        )

        # Dicionário contendo os títulos
        # que aparecerão na parte superior
        # da Treeview.
        #
        # A chave representa o nome interno
        # da coluna.
        #
        # O valor representa o texto exibido
        # ao usuário.
        headers = {
            "categoriaProduto": "Categoria",
            "nomeProduto": "Nome do produto",
            "precoProduto": "Preço",
            "estoque": "Estoque",
            "dataProduto": "Data de criação"
        }

        # Percorre todas as colunas do
        # dicionário.
        #
        # Para cada coluna, define o texto
        # que aparecerá no cabeçalho.
        for coluna, texto in headers.items():
            self.tree.heading(
                coluna,
                text=texto
            )

        # Configura as propriedades das colunas.
        #
        # column() NÃO cria uma coluna.
        #
        # Ela apenas configura uma coluna
        # que já foi criada anteriormente
        # em "columns=self.colunas".
        #
        # width
        # Largura inicial da coluna.
        #
        # minwidth
        # Menor largura permitida.
        #
        # anchor
        # Alinhamento do conteúdo.
        #
        # "w" = esquerda
        # "center" = centro
        # "e" = direita
        #
        # stretch
        # Define se a coluna poderá aumentar
        # ou diminuir quando a janela for
        # redimensionada.
        self.tree.column(
            "categoriaProduto",
            width=180,
            minwidth=120,
            anchor="w",
            stretch=True
        )

        self.tree.column(
            "nomeProduto",
            width=340,
            minwidth=160,
            anchor="w",
            stretch=True
        )

        self.tree.column(
            "precoProduto",
            width=120,
            minwidth=90,
            anchor="e",
            stretch=False
        )

        self.tree.column(
            "estoque",
            width=110,
            minwidth=80,
            anchor="center",
            stretch=False
        )

        self.tree.column(
            "dataProduto",
            width=110,
            minwidth=80,
            anchor="center",
            stretch=False
        )

        # Cria uma Scrollbar vertical.
        #
        # Scrollbar é uma barra de rolagem.
        #
        # Ela permite visualizar linhas da
        # tabela que não cabem na área visível.
        #
        # O parâmetro command informa que,
        # sempre que a barra for movimentada,
        # será executado o método onVScroll().
        self.barraScrollVertical = ttk.Scrollbar(
            tabelaContainer,
            orient="vertical",
            command=self.onVScroll
        )

        # Cria a barra de rolagem horizontal.
        #
        # Ela será utilizada quando a largura
        # da tabela ultrapassar o espaço
        # disponível na janela.
        self.barraScrollHorizontal = ttk.Scrollbar(
            tabelaContainer,
            orient="horizontal",
            command=self.onHScroll
        )

        # Conecta a Treeview às barras
        # de rolagem.
        #
        # Quando a Treeview for movimentada,
        # esses métodos atualizarão a posição
        # das Scrollbars.
        #
        # Da mesma forma, quando o usuário
        # mover uma Scrollbar, a Treeview
        # também será movimentada.
        self.tree.configure(
            yscrollcommand=self.ysync,
            xscrollcommand=self.xsync
        )

        # rowconfigure() configura o comportamento
        # das linhas do grid.
        #
        # weight representa o "peso" da linha.
        #
        # Quanto maior o peso, mais espaço ela
        # poderá ocupar quando o Frame for
        # redimensionado.
        #
        # Como existe apenas uma linha (linha 0),
        # ela ficará responsável por ocupar todo
        # o espaço disponível.
        tabelaContainer.rowconfigure(0, weight=1)

        # columnconfigure() funciona da mesma forma,
        # porém para as colunas do grid.
        #
        # Aqui permitimos que a primeira coluna,
        # onde ficará a Treeview, aumente conforme
        # a janela for sendo redimensionada.
        tabelaContainer.columnconfigure(0, weight=1)

        # Posiciona a Treeview utilizando grid().
        #
        # row=0
        # Primeira linha do grid.
        #
        # column=0
        # Primeira coluna do grid.
        #
        # sticky="nsew"
        # Faz a Treeview ocupar toda a célula
        # do grid, expandindo para todas as
        # direções:
        #
        # n = North (cima)
        # s = South (baixo)
        # e = East (direita)
        # w = West (esquerda)
        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # Posiciona a barra de rolagem vertical.
        #
        # Ela ficará ao lado direito da Treeview.
        #
        # sticky="ns"
        # Faz a Scrollbar ocupar toda a altura
        # da célula.
        self.barraScrollVertical.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        # Posiciona a barra de rolagem horizontal.
        #
        # Ela ficará abaixo da Treeview.
        #
        # sticky="ew"
        # Faz a Scrollbar ocupar toda a largura.
        self.barraScrollHorizontal.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        # ----------------------------------------------------
        # CANVAS
        # ----------------------------------------------------
        #
        # O Canvas é um dos componentes mais
        # poderosos do Tkinter.
        #
        # Diferentemente da Treeview, ele NÃO
        # foi criado para armazenar informações.
        #
        # Pense nele como uma folha de papel
        # totalmente em branco.
        #
        # Nessa folha podemos desenhar:
        #
        # • linhas;
        # • retângulos;
        # • círculos;
        # • textos;
        # • imagens;
        # • qualquer elemento gráfico.
        #
        # Neste projeto o Canvas ficará
        # exatamente SOBRE a Treeview.
        #
        # O objetivo é desenhar o destaque
        # da linha e da coluna selecionadas,
        # algo que a Treeview sozinha não
        # consegue fazer.
        #
        # Visualmente ficará assim:
        #
        #     Canvas
        # ┌─────────────────────┐
        # │                     │
        # │     Treeview        │
        # │                     │
        # └─────────────────────┘
        #
        # O usuário continuará vendo apenas
        # a tabela, mas quem desenhará os
        # destaques será o Canvas.
        self.overlay = tk.Canvas(

            # O Canvas será criado como filho
            # da própria Treeview.
            self.tree,

            # Remove a borda padrão.
            highlightthickness=0,

            # Remove a borda 3D.
            bd=0,

            # Utiliza a mesma cor da Treeview,
            # fazendo com que o Canvas fique
            # praticamente invisível.
            bg=self.treeBGColor()
        )

        # place_forget() remove o Canvas da tela.
        #
        # Ele NÃO é destruído.
        #
        # Apenas deixa de aparecer até que
        # algum método utilize place() para
        # mostrá-lo novamente.
        self.overlay.place_forget()

        # ----------------------------------------------------
        # EVENTOS DO CANVAS
        # ----------------------------------------------------
        #
        # Como o Canvas está SOBRE a Treeview,
        # todos os cliques do usuário irão,
        # primeiro, para o Canvas.
        #
        # Isso faria a Treeview parar de
        # responder normalmente.
        #
        # Para resolver esse problema,
        # todos os eventos recebidos pelo
        # Canvas são imediatamente enviados
        # para a Treeview.
        #
        # Assim o usuário nem percebe que
        # existe um Canvas sobre a tabela.

        # lambda cria uma pequena função
        # temporária.
        #
        # Essa função existe apenas para
        # encaminhar o evento para a Treeview.
        #
        # event_generate() cria artificialmente
        # um evento.
        #
        # É como dizer:
        #
        # "Treeview, finja que esse clique
        # aconteceu diretamente em você."

        # Repassa o clique do botão esquerdo.
        self.overlay.bind(
            "<Button-1>",
            lambda e: self.tree.event_generate(
                "<Button-1>",
                x=e.x,
                y=e.y
            )
        )

        # Repassa o momento em que o usuário
        # solta o botão esquerdo.
        self.overlay.bind(
            "<ButtonRelease-1>",
            lambda e: self.tree.event_generate(
                "<ButtonRelease-1>",
                x=e.x,
                y=e.y
            )
        )

        # Repassa o duplo clique.
        self.overlay.bind(
            "<Double-Button-1>",
            lambda e: self.tree.event_generate(
                "<Double-Button-1>",
                x=e.x,
                y=e.y
            )
        )

        # Repassa a rolagem da roda do mouse.
        #
        # Isso permite continuar rolando
        # a Treeview normalmente.
        self.overlay.bind(
            "<MouseWheel>",
            lambda e: self.tree.event_generate(
                "<MouseWheel>",
                delta=e.delta
            )
        )

        # Em alguns sistemas Linux,
        # o scroll utiliza os eventos
        # Button-4 e Button-5.
        self.overlay.bind(
            "<Button-4>",
            lambda e: self.tree.event_generate("<Button-4>")
        )

        self.overlay.bind(
            "<Button-5>",
            lambda e: self.tree.event_generate("<Button-5>")
        )

        # ----------------------------------------------------
        # TAGS DA TREEVIEW
        # ----------------------------------------------------
        #
        # Uma tag funciona como uma "classe"
        # de estilo.
        #
        # Sempre que uma linha receber uma
        # determinada tag, ela assumirá
        # essa aparência.

        # Cor utilizada nas linhas ímpares.
        self.tree.tag_configure(
            "oddrow",
            background="#FFFFFF"
        )

        # Cor utilizada nas linhas pares.
        #
        # Alternar as cores facilita
        # bastante a leitura da tabela.
        self.tree.tag_configure(
            "evenrow",
            background="#D7FCEC"
        )

        # Cor utilizada para destacar
        # a linha atualmente selecionada.
        self.tree.tag_configure(
            "rowSel",
            background=self.corLinhaSel
        )

        # ----------------------------------------------------
        # EVENTOS DA TREEVIEW
        # ----------------------------------------------------

        # Sempre que o usuário clicar em
        # uma célula da tabela,
        # será executado o método onClick().
        #
        # Ele descobrirá exatamente qual
        # célula foi clicada.
        self.tree.bind(
            "<Button-1>",
            self.onClick
        )

        # <<TreeviewSelect>> é um evento
        # gerado automaticamente pelo Tkinter
        # quando uma linha é selecionada.
        #
        # Não é necessário chamar esse evento.
        #
        # A própria Treeview dispara esse
        # evento sempre que a seleção muda.
        self.tree.bind(
            "<<TreeviewSelect>>",
            self.onSelectRow
        )

        # <Configure> acontece sempre que a
        # Treeview muda de tamanho.
        #
        # Como o Canvas desenha um destaque
        # sobre a tabela, é necessário
        # redesenhá-lo quando o tamanho mudar,
        # evitando que fique desalinhado.
        self.tree.bind(
            "<Configure>",
            lambda e: self.desenharColuna()
        )

        # Sempre que o usuário utilizar a roda
        # do mouse, redesenha o destaque para
        # mantê-lo sincronizado com a tabela.
        self.bind(
            "<MouseWheel>",
            lambda e: self.desenharColuna()
        )

        # Eventos equivalentes ao scroll
        # em sistemas Linux.
        self.bind(
            "<Button-4>",
            lambda e: self.desenharColuna()
        )

        self.bind(
            "<Button-5>",
            lambda e: self.desenharColuna()
        )

        # ----------------------------------------------------
        # FORMULÁRIO
        # ----------------------------------------------------
        #
        # Cria um LabelFrame para armazenar
        # todos os campos do formulário.
        #
        # O LabelFrame funciona como um Frame
        # comum, porém possui uma borda e um
        # título, facilitando a organização
        # visual da interface.
        #
        # Neste formulário o usuário poderá:
        #
        # • cadastrar um produto;
        # • alterar um produto;
        # • excluir um produto.
        formulario = ttk.LabelFrame(
            corpo,
            text="Cadastrar Produto / Alterar Produto / Excluir Produto"
        )

        # Posiciona o formulário à direita
        # da janela.
        #
        # fill="y" faz o formulário ocupar
        # toda a altura disponível.
        formulario.pack(
            side="right",
            fill="y"
        )

        # Variável utilizada para controlar
        # a linha atual do grid.
        #
        # Em vez de escrever manualmente:
        #
        # row=0
        # row=1
        # row=2
        #
        # basta incrementar essa variável.
        #
        # Isso facilita adicionar ou remover
        # componentes futuramente.
        r = 0

        # ----------------------------------------------------
        # CATEGORIA
        # ----------------------------------------------------

        # Texto descritivo do campo.
        ttk.Label(
            formulario,
            text="Categoria do produto:"
        ).grid(
            row=r,
            column=0,
            sticky="w",
            padx=6,
            pady=(10, 4)
        )

        # Caixa onde o usuário informará
        # a categoria do produto.
        #
        # O parâmetro textvariable conecta
        # essa Entry à variável
        # self.varCategoriaProduto.
        #
        # Assim, o texto digitado poderá ser
        # obtido utilizando:
        #
        # self.varCategoriaProduto.get()
        ttk.Entry(
            formulario,
            textvariable=self.varCategoriaProduto,
            width=28,
            style="Form.TEntry"
        ).grid(
            row=r,
            column=1,
            padx=6,
            pady=(10, 4)
        )

        # Avança para a próxima linha
        # do formulário.
        r += 1

        # ----------------------------------------------------
        # NOME DO PRODUTO
        # ----------------------------------------------------

        ttk.Label(
            formulario,
            text="Nome do produto:"
        ).grid(
            row=r,
            column=0,
            sticky="w",
            padx=6,
            pady=4
        )

        ttk.Entry(
            formulario,
            textvariable=self.varNomeProduto,
            width=28,
            style="Form.TEntry"
        ).grid(
            row=r,
            column=1,
            padx=6,
            pady=4
        )

        r += 1

        # ----------------------------------------------------
        # PREÇO
        # ----------------------------------------------------

        ttk.Label(
            formulario,
            text="Preço do produto:"
        ).grid(
            row=r,
            column=0,
            sticky="w",
            padx=6,
            pady=4
        )

        ttk.Entry(
            formulario,
            textvariable=self.varPrecoProduto,
            width=14,
            style="Form.TEntry"
        ).grid(
            row=r,
            column=1,
            padx=6,
            pady=4,
            sticky="w"
        )

        r += 1

        # ----------------------------------------------------
        # ESTOQUE
        # ----------------------------------------------------

        ttk.Label(
            formulario,
            text="Estoque:"
        ).grid(
            row=r,
            column=0,
            sticky="w",
            padx=6,
            pady=4
        )

        ttk.Entry(
            formulario,
            textvariable=self.varEstoque,
            width=14,
            style="Form.TEntry"
        ).grid(
            row=r,
            column=1,
            padx=6,
            pady=4,
            sticky="w"
        )

        r += 1

        # ----------------------------------------------------
        # DATA
        # ----------------------------------------------------

        ttk.Label(
            formulario,
            text="Data de criação do produto:"
        ).grid(
            row=r,
            column=0,
            sticky="w",
            padx=6,
            pady=4
        )

        ttk.Entry(
            formulario,
            textvariable=self.varDataProduto,
            width=14,
            style="Form.TEntry"
        ).grid(
            row=r,
            column=1,
            padx=6,
            pady=4,
            sticky="w"
        )

        r += 1

        # ----------------------------------------------------
        # SEPARADOR
        # ----------------------------------------------------
        #
        # Separator cria uma linha visual
        # utilizada para dividir grupos
        # de componentes.
        #
        # Aqui ela separa os campos do
        # formulário dos botões de ação.
        ttk.Separator(formulario).grid(
            row=r,
            column=0,
            columnspan=2,
            padx=6,
            pady=10,
            sticky="ew"
        )

        r += 1

        # ----------------------------------------------------
        # BOTÕES
        # ----------------------------------------------------

        # Botão responsável por cadastrar
        # um novo produto no banco de dados.
        ttk.Button(
            formulario,
            text="Cadastrar produto",
            style="Form.Button",
            command=self.cadastrarProduto
        ).grid(
            row=r,
            column=0,
            sticky="ew",
            padx=6,
            pady=4
        )

        r += 1

        # Atualiza o produto atualmente
        # selecionado na Treeview.
        ttk.Button(
            formulario,
            text="Alterar produto (linha selecionada)",
            style="Form.Button",
            command=self.alterarProduto
        ).grid(
            row=r,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=6,
            pady=4
        )

        r += 1

        # Remove do banco o produto
        # atualmente selecionado.
        ttk.Button(
            formulario,
            text="Excluir produto (linha selecionada)",
            style="Form.Button",
            command=self.excluirProduto
        ).grid(
            row=r,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=6,
            pady=4
        )

        r += 1

        # Limpa todos os campos do formulário,
        # permitindo iniciar um novo cadastro.
        ttk.Button(
            formulario,
            text="Limpar formulário",
            style="Form.Button",
            command=self.limparFormulario
        ).grid(
            row=r,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=6,
            pady=(4, 10)
        )

    # Por que esse método existe?
    #
    # O Canvas será desenhado sobre a Treeview.
    #
    # Se o Canvas possuir uma cor diferente,
    # ele aparecerá como um retângulo por cima
    # da tabela.
    #
    # Por isso precisamos descobrir qual é a
    # cor da Treeview e utilizar exatamente
    # essa mesma cor no Canvas.
    #
    # Assim o Canvas fica "invisível" e o
    # usuário enxerga apenas o destaque da
    # linha e da coluna.
    #
    # O problema é que o Tkinter possui
    # diversos temas (Themes), como:
    #
    # • clam
    # • vista
    # • alt
    # • default
    #
    # Cada tema pode armazenar suas cores
    # de maneira diferente.
    #
    # Por isso não existe um único comando
    # que sempre funcione.
    #
    # O método tenta descobrir a cor em
    # diferentes lugares até conseguir
    # encontrá-la.
    def treeBGColor(self):

        # Cria um objeto Style.
        #
        # Style é o responsável por armazenar
        # toda a aparência visual dos
        # componentes ttk.
        #
        # É semelhante ao CSS de uma página
        # HTML, contendo informações como:
        #
        # • cor de fundo;
        # • cor do texto;
        # • fonte;
        # • bordas;
        # • aparência dos botões;
        # • aparência da Treeview.
        estilo = ttk.Style(self)

        # lookup() procura uma propriedade
        # visual de um componente.
        #
        # Neste caso estamos perguntando:
        #
        # "Qual é a cor de fundo da Treeview?"
        #
        # Se o tema utilizado possuir essa
        # informação, ela será armazenada
        # na variável background.
        background = estilo.lookup(
            "Treeview",
            "background"
        )

        # Alguns temas não respondem essa
        # consulta utilizando lookup().
        #
        # Caso isso aconteça, tenta outra
        # maneira de descobrir a cor.
        if not background:

            try:

                # tk.call() envia um comando
                # diretamente ao mecanismo
                # interno do Tkinter (Tcl/Tk).
                #
                # É uma forma mais "profunda"
                # de consultar informações do
                # componente.
                background = self.tree.tk.call(
                    "ttk::style",
                    "lookup",
                    "Treeview",
                    "background"
                )

            # Caso nem o mecanismo interno
            # consiga informar essa cor,
            # apenas continua a execução.
            except tk.TclError:

                background = ""

        # Se ainda não foi possível descobrir
        # a cor da Treeview...
        if not background:

            try:

                # Utiliza como alternativa a
                # cor de fundo da própria janela.
                #
                # cget() significa
                # "Configuration GET",
                # ou seja:
                #
                # "obtenha o valor dessa
                # configuração".
                background = self.cget(
                    "background"
                )

            except Exception:

                # Se todas as tentativas
                # falharem, utiliza branco
                # como cor padrão.
                background = "#FFFFFF"

        # Retorna a cor encontrada.
        return background

    def buscarProduto(self):

        texto = self.varBusca.get().strip() or None

        self.carregarDados(texto)

        self.popularTabela()

        self.desenharColuna()

    def limparPesquisa(self):

        self.varBusca.set("")

        self.buscarProduto()

    # Carrega os produtos do banco de dados.
    #
    # O parâmetro texto é opcional.
    #
    # Caso seja informado, apenas os produtos
    # que correspondem à pesquisa serão
    # retornados.
    #
    # Caso seja None, todos os produtos
    # serão carregados.
    def carregarDados(self, texto: str | None = None):

        # Solicita ao repositório a lista
        # de produtos.
        #
        # O método listarTudo() faz a consulta
        # no banco de dados e retorna uma lista
        # de objetos Produto.
        #
        # Exemplo:
        #
        # [
        #     Produto(...),
        #     Produto(...),
        #     Produto(...)
        # ]
        self.dados = self.repo.listarTudo(
            texto=texto
        )

        # Cria um dicionário para localizar
        # rapidamente um produto pelo seu ID.
        #
        # A chave será o id do produto
        # convertido para string.
        #
        # O valor será o próprio objeto Produto.
        #
        # Exemplo:
        #
        # {
        #     "1": Produto(...),
        #     "2": Produto(...),
        #     "3": Produto(...)
        # }
        #
        # Isso evita percorrer toda a lista
        # sempre que for necessário encontrar
        # um produto específico.
        self.mapearIdProd = {
            str(prod.idProduto): prod
            for prod in self.dados
        }

    # Exibe na Treeview todos os produtos
    # armazenados na lista self.dados.
    #
    # Esse método NÃO consulta o banco.
    #
    # Ele apenas pega os objetos que já
    # estão carregados em self.dados e
    # os coloca na tabela.
    def popularTabela(self):

        # get_children() retorna todas as
        # linhas atualmente existentes na
        # Treeview.
        #
        # Antes de inserir os novos dados,
        # removemos todas as linhas antigas,
        # evitando que os registros fiquem
        # duplicados.
        for item in self.tree.get_children():
            # Remove uma linha da Treeview.
            self.tree.delete(item)

        # Percorre todos os produtos
        # armazenados na lista self.dados.
        #
        # enumerate() devolve duas informações:
        #
        # indice → posição do produto na lista.
        # prod   → objeto Produto.
        #
        # Exemplo:
        #
        # indice = 0
        # prod = Produto(...)
        #
        # indice = 1
        # prod = Produto(...)
        for indice, prod in enumerate(self.dados):
            # Alterna a cor das linhas.
            #
            # indice % 2 verifica se o índice
            # é par ou ímpar.
            #
            # Se o resto da divisão por 2
            # for diferente de zero,
            # significa que o índice é ímpar.
            #
            # Exemplo:
            #
            # índice 0 → evenrow
            # índice 1 → oddrow
            # índice 2 → evenrow
            # índice 3 → oddrow
            #
            # Isso melhora a visualização
            # da tabela.
            tag = "oddrow" if indice % 2 else "evenrow"

            # Insere uma nova linha
            # na Treeview.
            self.tree.insert(

                # "" indica que a linha será
                # inserida na raiz da Treeview.
                #
                # Como não existem subitens
                # (árvore), todas as linhas
                # ficam diretamente na tabela.
                "",

                # tk.END informa que a nova
                # linha será adicionada no
                # final da tabela.
                tk.END,

                # iid significa Item ID.
                #
                # É o identificador único de uma linha
                # dentro da Treeview.
                #
                # Sempre que uma linha for selecionada,
                # alterada ou removida, a Treeview
                # utilizará esse identificador para
                # saber exatamente qual linha está
                # sendo manipulada.
                #
                # Neste projeto utilizamos o próprio
                # ID do produto no banco de dados,
                # facilitando localizar o objeto
                # correspondente posteriormente.
                iid=str(prod.idProduto),

                # values representa os valores
                # que aparecerão nas colunas
                # da Treeview.
                #
                # A ordem deve ser exatamente
                # a mesma definida em:
                #
                # self.colunas
                values=(

                    # Categoria.
                    prod.categoriaProduto,

                    # Nome.
                    prod.nomeProduto,

                    # Preço formatado
                    # para moeda brasileira.
                    formatarMoedaBR(
                        prod.precoProduto
                    ),

                    # Estoque.
                    prod.estoque,

                    # Data formatada
                    # para o padrão brasileiro.
                    formatarDataBR(
                        prod.dataProduto
                    ),
                ),

                # Aplica a tag responsável
                # pela cor da linha.
                tags=(tag,)
            )

    # Executado sempre que o usuário
    # clicar na Treeview.
    #
    # Sua função é descobrir:
    #
    # • qual linha foi clicada;
    # • qual coluna foi clicada;
    #
    # Depois disso, atualiza a interface
    # destacando a linha, a coluna e
    # preenchendo o formulário com os
    # dados do produto selecionado.
    def onClick(self, evento):

        # identify() verifica em qual região
        # da Treeview o clique aconteceu.
        #
        # evento.x → posição horizontal do clique.
        # evento.y → posição vertical do clique.
        #
        # O retorno pode ser, por exemplo:
        #
        # "heading" → cabeçalho.
        # "cell"    → uma célula da tabela.
        # "tree"    → área da árvore.
        # "nothing" → espaço vazio.
        #
        # Neste projeto só nos interessam
        # os cliques nas células da tabela.
        regiao = self.tree.identify(
            "region",
            evento.x,
            evento.y
        )

        # Se o usuário clicou fora de uma
        # célula, não faz nada.
        if regiao not in ("cell", "tree"):
            return

        # Descobre qual linha foi clicada.
        #
        # Exemplo:
        #
        # "1"
        # "2"
        # "15"
        #
        # Esse valor corresponde ao iid da
        # linha na Treeview.
        rowId = self.tree.identify_row(
            evento.y
        )

        # Descobre qual coluna foi clicada.
        #
        # Exemplo:
        #
        # "#1"
        # "#2"
        # "#3"
        #
        # A Treeview numera internamente
        # suas colunas utilizando "#1",
        # "#2", "#3"...
        colId = self.tree.identify_column(
            evento.x
        )

        # Caso o clique não corresponda
        # a uma linha ou coluna válida,
        # encerra o método.
        if not rowId or not colId:
            return

        # Guarda qual linha foi
        # selecionada.
        #
        # Essa informação será utilizada
        # por outros métodos da aplicação.
        self.itemSelecionado = rowId

        # Guarda qual coluna foi
        # selecionada.
        self.colunaSelecionada = colId

        # Marca essa linha como
        # selecionada na Treeview.
        #
        # Isso faz aparecer o destaque
        # padrão de seleção.
        self.tree.selection_set(rowId)

        # Aplica a cor personalizada
        # na linha selecionada.
        self.aplicarTagNaLinha(rowId)

        # Preenche o formulário utilizando
        # os dados do produto correspondente
        # à linha selecionada.
        self.preencherFormPorIid(rowId)

        # Redesenha o Canvas responsável
        # pelo destaque da coluna.
        #
        # Como o usuário acabou de clicar
        # em outra coluna, o destaque
        # precisa ser atualizado.
        self.desenharColuna()

    # Executado sempre que uma linha da
    # Treeview é selecionada.
    #
    # Diferentemente do método onClick(),
    # aqui não importa onde o usuário clicou.
    #
    # O objetivo é apenas descobrir qual
    # linha está atualmente selecionada
    # e atualizar a interface.
    #
    # Esse método é chamado automaticamente
    # pelo evento <<TreeviewSelect>>.
    def onSelectedRow(self, evento=None):

        # selection() retorna uma lista
        # contendo os iids das linhas
        # atualmente selecionadas.
        #
        # Como a Treeview está configurada
        # para permitir apenas uma seleção
        # (selectmode="browse"),
        # essa lista terá no máximo um item.
        #
        # Exemplo:
        #
        # ["3"]
        selecionado = self.tree.selection()

        # Caso nenhuma linha esteja
        # selecionada, encerra o método.
        if not selecionado:
            return

        # Obtém o iid da linha selecionada.
        #
        # Como existe apenas uma seleção,
        # utilizamos o primeiro elemento
        # da lista.
        #
        # Exemplo:
        #
        # selecionado = ["5"]
        #
        # self.itemSelecionado = "5"
        self.itemSelecionado = selecionado[0]

        # Aplica a cor personalizada
        # na linha selecionada.
        self.aplicarTagNaLinha(
            self.itemSelecionado
        )

        # Localiza o objeto Produto
        # correspondente ao iid e preenche
        # os campos do formulário.
        self.preencherFormPorIid(
            self.itemSelecionado
        )

        # Redesenha o destaque da coluna.
        #
        # Isso mantém o Canvas sincronizado
        # com a seleção atual.
        self.desenharColuna()

    # Aplica a tag responsável por destacar
    # a linha selecionada.
    #
    # Como cada linha da Treeview pode
    # possuir várias tags ao mesmo tempo,
    # este método garante que apenas uma
    # delas tenha a tag "linhaSelecionada".
    #
    # Assim, sempre existirá apenas uma
    # linha destacada na tabela.
    def aplicarTagNaLinha(self, rowId: str):
        # Percorre todas as linhas
        # existentes na Treeview.
        #
        # O objetivo é procurar se alguma
        # delas ainda possui a tag
        # "linhaSelecionada".
        for iid in self.tree.get_children():

            # Obtém a lista de tags
            # atribuídas à linha.
            #
            # Exemplo:
            #
            # ["evenrow"]
            #
            # ou
            #
            # ["oddrow", "linhaSelecionada"]
            tags = list(
                self.tree.item(
                    iid,
                    "tags"
                )
            )

            # Verifica se essa linha
            # está destacada.
            if "linhaSelecionada" in tags:
                # Remove a tag responsável
                # pelo destaque.
                tags.remove(
                    "linhaSelecionada"
                )

                # Atualiza as tags da linha.
                #
                # tuple() é utilizado porque
                # a Treeview espera receber
                # uma tupla de tags.
                self.tree.item(
                    iid,
                    tags=tuple(tags)
                )

        # Obtém as tags da linha
        # que acabou de ser selecionada.
        tags = list(
            self.tree.item(
                rowId,
                "tags"
            )
        )

        # Caso essa linha ainda não esteja
        # destacada...
        if "linhaSelecionada" not in tags:
            # Adiciona a tag responsável
            # pelodest aque.
            tags.append(
                "linhaSelecionada"
            )

        # Atualiza as tags da linha,
        # aplicando o destaque visual.
        self.tree.item(
            rowId,
            tags=tuple(tags)
        )



























