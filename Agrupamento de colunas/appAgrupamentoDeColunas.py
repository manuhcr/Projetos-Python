# Importa a biblioteca Tkinter, responsável pela criação
# da interface gráfica (GUI) da aplicação.
#
# O apelido "tk" facilita a utilização das classes
# e funções da biblioteca ao longo do código.
import tkinter as tk

# Importa componentes específicos do Tkinter.
#
# ttk:
# Contém widgets modernos, como Button, Label,
# Entry, Treeview, Frame e LabelFrame.
#
# messagebox:
# Utilizado para exibir caixas de diálogo,
# como mensagens de erro, confirmação,
# avisos e informações ao usuário.
from tkinter import ttk, messagebox

# Importa classes da biblioteca datetime.
#
# datetime:
# Utilizada para obter data e hora atuais
# e realizar conversões entre texto e datas.
#
# date:
# Representa apenas uma data (dia, mês e ano),
# sem armazenar horário.
from datetime import datetime, date

# Importa a classe responsável por acessar
# o banco de dados.
#
# O repositório concentra todas as operações
# de consulta, cadastro, alteração, exclusão
# e exportação das vendas.
from repositorio import RepoVendas

# Importa a classe Venda.
#
# Essa classe representa um registro da tabela
# de vendas, armazenando informações como
# cliente, produto, cidade, preço, quantidade,
# total e data da venda.
from modelos import Venda


# Formata um valor numérico para o padrão
# monetário brasileiro.
#
# Exemplo:
# 1234.56 -> 1.234,56
#
# Retorno:
# String contendo o valor formatado.
def formataMoedaBR(valor: float) -> str:

    # Converte o número para texto utilizando
    # o padrão americano.
    #
    # :,.2f significa:
    # ,  -> separador de milhares
    # .2 -> duas casas decimais
    # f  -> número em ponto flutuante
    #
    # Exemplo:
    # 1234.56 -> "1,234.56"
    string = f"{valor:,.2f}"

    # Converte o formato americano para
    # o formato brasileiro.
    #
    # 1º: troca a vírgula dos milhares por "X".
    #     1,234.56 -> 1X234.56
    #
    # 2º: troca o ponto decimal por vírgula.
    #     1X234.56 -> 1X234,56
    #
    # 3º: troca o "X" por ponto.
    #     1X234,56 -> 1.234,56
    return string.replace(",", "X").replace(".", ",").replace("X", ".")


# Converte um preço informado no formato brasileiro
# para um número decimal (float).
#
# Exemplo:
# "15,90" -> 15.90
#
# Retorno:
# float contendo o valor numérico.
#
# Caso o campo esteja vazio, uma exceção
# ValueError será gerada.
def parsePrecoBR(string: str) -> float:

    # Remove espaços em branco do início e do fim
    # do texto informado.
    #
    # O operador "or" garante que, caso o valor
    # recebido seja None ou vazio, seja utilizada
    # uma string vazia.
    texto = (string or "").strip()

    # Verifica se o usuário informou algum valor.
    #
    # Caso o campo esteja vazio, interrompe
    # a execução da função informando o erro.
    if not texto:
        raise ValueError("Informe o preço")

    # Remove os pontos utilizados como separador
    # de milhares e substitui a vírgula decimal
    # por ponto, formato aceito pela função float().
    #
    # Exemplos:
    # "1.234,56" -> "1234.56"
    # "15,90"    -> "15.90"
    texto = texto.replace(".", "").replace(",", ".")
    return float(texto)

    # Converte o texto em um número decimal
    # e retorna esse valor.
    return float(texto)

# Converte uma data para o formato brasileiro.
#
# Recebe um objeto do tipo date e retorna
# uma string no formato dd/mm/aaaa.
#
# Exemplo:
# date(2025, 7, 2) -> "02/07/2025"
def formataDataBR(data: date) -> str:

    # strftime() ("string format time") converte
    # um objeto date em uma string seguindo
    # o padrão informado.
    #
    # %d -> dia com dois dígitos.
    # %m -> mês com dois dígitos.
    # %Y -> ano com quatro dígitos.
    return data.strftime("%d/%m/%Y")

# Converte uma data informada em formato de texto
# para um objeto do tipo date.
#
# Recebe uma string no formato brasileiro
# (dd/mm/aaaa) e retorna uma data.
#
# Exemplo:
# "02/07/2025" -> date(2025, 7, 2)
def parseDataBR(string: str) -> date:

    # Remove espaços em branco do início
    # e do final da string.
    #
    # strptime() ("string parse time") converte
    # uma string em um objeto datetime utilizando
    # o formato especificado.
    #
    # %d -> dia com dois dígitos.
    # %m -> mês com dois dígitos.
    # %Y -> ano com quatro dígitos.
    #
    # Como o sistema utiliza apenas a data,
    # o método .date() extrai somente dia,
    # mês e ano, descartando a parte do horário.
    return datetime.strptime(
        string.strip(),
        "%d/%m/%Y"
    ).date()

# Classe principal da aplicação.
#
# Herda da classe tk.Tk, tornando este objeto
# a janela principal do sistema.
#
# Toda a interface gráfica, como botões,
# tabela, formulários e eventos, será criada
# e controlada por esta classe.
class appAgrupamentoDeColunas(tk.Tk):

    def __init__(self):
        # Chama o construtor da classe pai (tk.Tk),
        # inicializando a janela principal da aplicação.
        #
        # Sem essa chamada, a interface gráfica
        # não seria criada corretamente.
        super().__init__()

        # Define o título exibido na barra superior da janela.
        self.title("Tabela de Agrupamento de colunas")

        # Centraliza a janela na tela utilizando
        # a largura e altura informadas.
        self.alinharAoCentro(1240, 640)

        # Define o tamanho mínimo permitido para a janela.
        # O usuário não poderá redimensioná-la para um
        # tamanho menor que este.
        self.minsize(1120, 560)

        # Cria uma instância da classe responsável por
        # acessar o banco de dados e realizar operações
        # de cadastro, consulta, alteração e exclusão.
        self.repo = RepoVendas()

        # Lista que armazenará todos os objetos Venda
        # carregados do banco de dados.
        #
        # Essa lista é utilizada para preencher a tabela
        # da interface e realizar ordenações.
        self.dados: list[Venda] = []

        # Indica se o grupo "Detalhes do Cliente"
        # está expandido (True) ou recolhido (False).
        self.grupoClienteAberto = False

        # Indica se o grupo "Detalhes da Venda"
        # está expandido (True) ou recolhido (False).
        self.grupoVendaAberto = False

        # Armazena o nome da coluna atualmente utilizada
        # para ordenar a tabela.
        #
        # Enquanto nenhuma ordenação for realizada,
        # o valor permanece None.
        self.ordemColuna = None

        # Indica o sentido da ordenação.
        #
        # False = ordem crescente.
        # True = ordem decrescente.
        self.ordemReverse = False

        # Aplica todas as configurações visuais
        # da interface, como fontes, estilos e botões.
        self.configEstilo()

        # Variável associada ao campo "Nome do Cliente".
        #
        # O texto digitado pelo usuário será armazenado
        # automaticamente nesta StringVar.
        self.varNomeCliente = tk.StringVar()

        # Variável associada ao campo "Cidade".
        self.varCidade = tk.StringVar()

        # Variável associada ao campo "Setor".
        self.varSetor = tk.StringVar()

        # Variável associada ao campo "Produto".
        self.varProduto = tk.StringVar()

        # Variável associada ao campo "Quantidade".
        self.varQuantidade = tk.StringVar()

        # Variável associada ao campo
        # "Preço Unitário".
        self.varPrecoUnit = tk.StringVar()

        # Variável associada ao campo
        # "Data da Venda".
        self.varData = tk.StringVar()

        # Armazena o preço total calculado
        # automaticamente conforme a quantidade
        # e o preço unitário informados.
        self.varPrecoTotal = tk.StringVar(value="R$ 0,00")

        # Armazena o ID da venda atualmente
        # selecionada na tabela.
        #
        # Enquanto nenhuma linha estiver selecionada,
        # o valor será None.
        self.idSelecionado: int | None = None

        # Cria todos os componentes da interface gráfica,
        # como botões, tabela, formulários e rótulos.
        self.montaUI()

        # Carrega todas as vendas existentes
        # no banco de dados.
        self.carregaDados()

        # Preenche a tabela da interface
        # com os registros carregados.
        self.populaTabela()

        # Atualiza as informações exibidas
        # no rodapé da janela, como quantidade
        # de registros e soma total das vendas.
        self.atualizaRodape()

    # Centraliza a janela na tela.
    #
    # Recebe a largura e a altura desejadas
    # para calcular a posição da janela
    # em relação ao tamanho do monitor.
    def alinharAoCentro(self, largura: int, altura: int):

        # Atualiza a interface antes de obter
        # informações sobre a janela.
        #
        # Isso garante que os cálculos de tamanho
        # sejam realizados corretamente.
        self.update_idletasks()

        # Obtém a largura (sw) e a altura (sh)
        # da tela do computador.
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()

        # Calcula a posição horizontal (eixo X)
        # para que a janela fique centralizada.
        x = (sw // 2) - (largura // 2)

        # Calcula a posição vertical (eixo Y)
        # para que a janela fique centralizada.
        y = (sh // 2) - (altura // 2)

        # Define o tamanho da janela e sua posição
        # na tela utilizando o formato:
        #
        # largura x altura + posiçãoX + posiçãoY
        #
        # Exemplo:
        # 1240x640+340+180
        self.geometry(f"{largura}x{altura}+{x}+{y}")

    # Configura a aparência dos componentes
    # da interface gráfica.
    #
    # Neste método são definidos o tema da aplicação,
    # a fonte utilizada, o tamanho das linhas da tabela
    # e os estilos personalizados de alguns widgets.
    def configEstilo(self):

        # Cria o objeto responsável por gerenciar
        # todos os estilos da biblioteca ttk.
        estilo = ttk.Style(self)

        # Define o tema visual da aplicação.
        #
        # Caso o tema informado não exista no sistema,
        # o programa continuará utilizando o tema padrão.
        try:
            estilo.theme_use("default")

        except tk.TclError:
            pass

        # Configura a aparência da tabela (Treeview).
        #
        # font:
        # Define a fonte utilizada nas linhas da tabela.
        #
        # rowheight:
        # Define a altura de cada linha da tabela.
        estilo.configure(
            "Treeview",
            font=("Roboto-Blue", 12, "bold"),
            rowheight=28
        )

        # Configura a aparência dos cabeçalhos
        # das colunas da tabela.
        estilo.configure(
            "Treeview.Heading",
            font=("Roboto-Blue", 12, "bold")
        )

        # Cria um estilo personalizado para os botões
        # maiores da aplicação.
        #
        # padding adiciona um espaçamento interno,
        # deixando o botão mais confortável visualmente.
        estilo.configure(
            "Big.TButton",
            padding=(10, 6)
        )

        # Cria um estilo para os campos de entrada
        # (Entry), adicionando um pequeno espaçamento
        # interno para melhorar a aparência.
        estilo.configure(
            "Form.TEntry",
            padding=4
        )

    # Cria toda a interface gráfica da aplicação.
    #
    # Neste método são criados todos os componentes
    # visuais do sistema, como painéis, tabela,
    # formulário, botões, barras de rolagem e rodapé.
    def montaUI(self):

        # Cria um LabelFrame que agrupa os botões
        # responsáveis por expandir e recolher
        # os grupos de colunas da tabela.
        #
        # Um LabelFrame é semelhante a um Frame,
        # porém possui um título visível.
        top = ttk.LabelFrame(
            self,
            text="Agrupamentos"
        )

        # Posiciona o painel na parte superior
        # da janela.
        #
        # fill="x":
        # Faz o painel ocupar toda a largura.
        #
        # padx:
        # Adiciona espaçamento nas laterais.
        #
        # pady:
        # Adiciona espaçamento acima e abaixo.
        top.pack(
            fill="x",
            padx=12,
            pady=(12, 8)
        )

        # Cria o botão responsável por expandir
        # ou ocultar as colunas relacionadas
        # aos dados do cliente.
        #
        # text:
        # Texto exibido no botão.
        #
        # style:
        # Utiliza o estilo personalizado
        # criado no método configEstilo().
        #
        # command:
        # Método executado quando o botão
        # for pressionado.
        self.btnGrupoCliente = ttk.Button(
            top,
            text="+ Detalhes do cliente",
            style="Big.TButton",
            command=self.toggleGrupoCliente
        )

        # Posiciona o botão utilizando
        # o gerenciador de layout Grid.
        #
        # row:
        # Linha onde o botão será colocado.
        #
        # column:
        # Coluna onde o botão será colocado.
        #
        # sticky="w":
        # Alinha o botão à esquerda da célula.
        self.btnGrupoCliente.grid(
            row=0,
            column=0,
            padx=(12, 6),
            pady=6,
            sticky="w"
        )

        # Cria o botão responsável por expandir
        # ou ocultar as colunas relacionadas
        # às informações da venda.
        self.btnGrupoVenda = ttk.Button(
            top,
            text="+ Detalhes da venda",
            style="Big.TButton",
            command=self.toggleGrupoVenda
        )

        # Posiciona o botão ao lado
        # do botão anterior.
        self.btnGrupoVenda.grid(
            row=0,
            column=1,
            padx=6,
            pady=6,
            sticky="w"
        )

        # Permite que a terceira coluna do painel
        # aumente automaticamente quando a janela
        # for redimensionada.
        #
        # weight=1 indica que essa coluna pode
        # crescer para ocupar o espaço livre.
        top.grid_columnconfigure(
            2,
            weight=1
        )

        # Cria o painel principal da aplicação.
        #
        # Esse painel servirá como contêiner para
        # a tabela de vendas e o formulário.
        body = ttk.Frame(self)

        # Posiciona o painel principal.
        #
        # expand=True faz o painel crescer
        # junto com a janela.
        body.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 8)
        )

        # Cria um LabelFrame para agrupar
        # a tabela de vendas.
        #
        # O título informa ao usuário que
        # as colunas podem ser expandidas
        # e recolhidas através dos botões.
        frameTabela = ttk.LabelFrame(
            body,
            text="Vendas (expanda/colapse colunas pelos agrupamentos)"
        )

        # Posiciona a tabela no lado esquerdo
        # da janela.
        frameTabela.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        # Cria um Frame interno que armazenará
        # a Treeview e suas barras de rolagem.
        #
        # Essa separação facilita a organização
        # dos componentes.
        tabelaContainer = ttk.Frame(frameTabela)

        tabelaContainer.pack(
            fill="both",
            expand=True,
            padx=6,
            pady=6
        )

        # Define todas as colunas existentes
        # na Treeview.
        #
        # Inicialmente apenas Nome do Cliente
        # e Total ficam visíveis.
        #
        # As demais colunas serão exibidas
        # quando o usuário clicar nos botões
        # de agrupamento.
        self.colunas = (
            "nomeCliente",
            "cidade",
            "setor",
            "produto",
            "quantidade",
            "precoUnitario",
            "dataVenda",
            "total"
        )

        # Cria a tabela responsável por exibir
        # todas as vendas cadastradas.
        #
        # tabelaContainer:
        # Frame onde a tabela será inserida.
        #
        # columns:
        # Lista contendo todas as colunas.
        #
        # show="headings":
        # Exibe apenas os cabeçalhos,
        # ocultando a primeira coluna
        # padrão do Treeview.
        #
        # height:
        # Define aproximadamente quantas
        # linhas serão exibidas.
        #
        # selectmode="browse":
        # Permite selecionar apenas
        # uma linha por vez.
        self.tree = ttk.Treeview(
            tabelaContainer,
            columns=self.colunas,
            show="headings",
            height=18,
            selectmode="browse"
        )

        # Dicionário que relaciona o nome interno de cada
        # coluna ao texto que será exibido no cabeçalho
        # da tabela.
        #
        # Chave:
        # Nome utilizado internamente pelo Treeview.
        #
        # Valor:
        # Texto apresentado ao usuário.
        headers = {
            "nomeCliente": "Nome do cliente",
            "cidade": "Cidade",
            "setor": "Setor",
            "produto": "Produto",
            "quantidade": "Quantidade",
            "precoUnitario": "Preço Unitário",
            "dataVenda": "Data da Venda",
            "total": "Total"
        }

        # Percorre todas as colunas definidas no
        # dicionário de cabeçalhos.
        #
        # Em cada repetição:
        # coluna -> nome interno da coluna.
        # texto  -> título exibido ao usuário.
        for coluna, texto in headers.items():

            # Configura o cabeçalho da coluna.
            #
            # text:
            # Define o texto exibido no cabeçalho.
            #
            # command:
            # Define a função executada quando o
            # usuário clicar no nome da coluna.
            #
            # O lambda cria uma pequena função
            # anônima que chama ordenaPorColuna(),
            # enviando o nome da coluna clicada.
            self.tree.heading(
                coluna,
                text=texto,
                command=lambda coluna=coluna: self.ordenaPorColuna(coluna),
            )

        # Configura a coluna "Nome do Cliente".
        #
        # width:
        # Largura inicial da coluna.
        #
        # minwidth:
        # Menor largura permitida.
        #
        # anchor="w":
        # Alinha o texto à esquerda (West).
        #
        # stretch=True:
        # Permite que a coluna aumente ou diminua
        # de tamanho quando a janela for redimensionada.
        self.tree.column(
            "nomeCliente",
            width=260,
            minwidth=120,
            anchor="w",
            stretch=True
        )

        # Configura a coluna "Total".
        #
        # anchor="e":
        # Alinha os valores à direita (East),
        # facilitando a leitura de valores monetários.
        #
        # stretch=False:
        # Impede que a largura seja alterada
        # automaticamente.
        self.tree.column(
            "total",
            width=140,
            minwidth=100,
            anchor="e",
            stretch=False
        )

        # Inicialmente as demais colunas ficam ocultas.
        #
        # Elas serão exibidas somente quando o usuário
        # clicar nos botões de agrupamento.
        for col in (
            "cidade",
            "setor",
            "produto",
            "quantidade",
            "precoUnitario",
            "dataVenda"
        ):

            self.tree.column(
                col,
                width=0,
                minwidth=0,
                stretch=False,
                anchor="center"
            )

        # Cria a barra de rolagem vertical da tabela.
        #
        # command=self.tree.yview faz com que a barra
        # controle a movimentação vertical do Treeview.
        barraScrollVertical = ttk.Scrollbar(
            tabelaContainer,
            orient="vertical",
            command=self.tree.yview,
        )

        # Cria a barra de rolagem horizontal.
        #
        # command=self.tree.xview controla
        # o deslocamento horizontal da tabela.
        barraScrollHorizontal = ttk.Scrollbar(
            tabelaContainer,
            orient="horizontal",
            command=self.tree.xview,
        )

        # Associa as barras de rolagem ao Treeview.
        #
        # Sempre que a tabela for movimentada,
        # as barras atualizarão automaticamente
        # sua posição.
        self.tree.configure(
            yscrollcommand=barraScrollVertical.set,
            xscrollcommand=barraScrollHorizontal.set,
        )

        # Permite que a primeira linha e a primeira
        # coluna do Frame cresçam automaticamente
        # quando a janela for redimensionada.
        tabelaContainer.rowconfigure(0, weight=1)
        tabelaContainer.columnconfigure(0, weight=1)

        # Posiciona a Treeview dentro do Frame.
        #
        # sticky="nsew":
        # Faz a tabela ocupar todo o espaço disponível
        # (Norte, Sul, Leste e Oeste).
        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # Posiciona a barra de rolagem vertical
        # ao lado direito da tabela.
        barraScrollVertical.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        # Posiciona a barra de rolagem horizontal
        # abaixo da tabela.
        barraScrollHorizontal.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        # Define a aparência das linhas ímpares
        # da tabela.
        self.tree.tag_configure(
            "oddrow",
            background="#FFFFFF"
        )

        # Define a aparência das linhas pares.
        #
        # A alternância de cores facilita
        # a leitura dos registros.
        self.tree.tag_configure(
            "evenrow",
            background="#DCE7EE"
        )

        # Associa o evento de seleção da Treeview
        # ao método capturaSelecao().
        #
        # Sempre que o usuário selecionar uma linha,
        # os dados serão carregados automaticamente
        # para o formulário.
        self.tree.bind(
            "<<TreeviewSelect>>",
            self.capturaSelecao
        )

        # Cria o painel que contém o formulário
        # de cadastro, alteração e exclusão
        # das vendas.
        frameForm = ttk.LabelFrame(
            body,
            text="Cadastrar (Nova Venda) / Alterar (venda selecionada) / Excluir (venda selecionada)"
        )

        # Posiciona o formulário no lado direito
        # da janela.
        #
        # fill="y" faz o painel ocupar toda
        # a altura disponível.
        frameForm.pack(
            side="right",
            fill="y"
        )

        # Variável utilizada para controlar a linha
        # atual do formulário.
        #
        # A cada novo campo criado, o valor de "r"
        # é incrementado para posicionar os próximos
        # componentes na linha seguinte.
        r = 0

        # ============================
        # Campo: Nome do Cliente
        # ============================

        # Os componentes do formulário são organizados
        # utilizando o gerenciador de layout grid().
        #
        # O grid() funciona como uma tabela, dividida
        # em linhas (row) e colunas (column).
        #
        # Neste formulário:
        #
        # Coluna 0 -> Rótulos (Labels).
        # Coluna 1 -> Campos de entrada (Entry).
        #
        # A variável "r" controla a linha atual.
        # Sempre que um campo é criado, r é incrementado
        # para posicionar o próximo componente na linha
        # seguinte.
        #
        # Exemplo:
        #
        # row=0, column=0 -> primeira linha, primeira coluna.
        # row=0, column=1 -> primeira linha, segunda coluna.
        # row=1, column=0 -> segunda linha, primeira coluna.
        #
        # Os principais parâmetros utilizados são:
        #
        # sticky:
        # Alinha o componente dentro da célula.
        # "w" = esquerda
        # "e" = direita
        # "n" = cima
        # "s" = baixo
        #
        # padx:
        # Espaçamento horizontal.
        #
        # pady:
        # Espaçamento vertical.
        #
        # columnspan:
        # Faz o componente ocupar mais de uma coluna.
        # Neste formulário os botões utilizam
        # columnspan=2 para ocupar toda a largura.

        # Rótulo que identifica o campo
        # de nome do cliente.
        ttk.Label(frameForm, text="Nome do cliente:").grid(
            row=r, column=0, sticky="w", padx=6, pady=(10, 4)
        )

        # Campo onde o usuário informa
        # o nome do cliente.
        ttk.Entry(
            frameForm,
            textvariable=self.varNomeCliente,
            width=28,
            style="Form.TEntry"
        ).grid(
            row=r, column=1, padx=6, pady=(10, 4)
        )

        r += 1

        # ============================
        # Campo: Cidade
        # ============================

        ttk.Label(frameForm, text="Cidade:").grid(
            row=r, column=0, sticky="w", padx=6, pady=4
        )

        ttk.Entry(
            frameForm,
            textvariable=self.varCidade,
            width=28,
            style="Form.TEntry"
        ).grid(
            row=r, column=1, padx=6, pady=4
        )

        r += 1

        # ============================
        # Campo: Setor
        # ============================

        ttk.Label(frameForm, text="Setor:").grid(
            row=r, column=0, sticky="w", padx=6, pady=4
        )

        ttk.Entry(
            frameForm,
            textvariable=self.varSetor,
            width=28,
            style="Form.TEntry"
        ).grid(
            row=r, column=1, padx=6, pady=4
        )

        r += 1

        # ============================
        # Campo: Produto
        # ============================

        ttk.Label(frameForm, text="Produto:").grid(
            row=r, column=0, sticky="w", padx=6, pady=4
        )

        ttk.Entry(
            frameForm,
            textvariable=self.varProduto,
            width=28,
            style="Form.TEntry"
        ).grid(
            row=r, column=1, padx=6, pady=4
        )

        r += 1

        # ============================
        # Campo: Quantidade
        # ============================

        ttk.Label(frameForm, text="Quantidade:").grid(
            row=r, column=0, sticky="w", padx=6, pady=4
        )

        ttk.Entry(
            frameForm,
            textvariable=self.varQuantidade,
            width=12,
            style="Form.TEntry"
        ).grid(
            row=r, column=1, padx=6, pady=4, sticky="w"
        )

        r += 1

        # ============================
        # Campo: Preço Unitário
        # ============================

        ttk.Label(frameForm, text="Preço Unitário (ex: 1.234,56):").grid(
            row=r, column=0, sticky="w", padx=6, pady=4
        )

        ttk.Entry(
            frameForm,
            textvariable=self.varPrecoUnit,
            width=12,
            style="Form.TEntry"
        ).grid(
            row=r, column=1, padx=6, pady=4, sticky="w"
        )

        r += 1

        # ============================
        # Campo: Data da Venda
        # ============================

        ttk.Label(frameForm, text="Data (dd/mm/aaaa):").grid(
            row=r, column=0, sticky="w", padx=6, pady=4
        )

        ttk.Entry(
            frameForm,
            textvariable=self.varData,
            width=12,
            style="Form.TEntry"
        ).grid(
            row=r, column=1, padx=6, pady=4, sticky="w"
        )

        r += 1

        # ============================
        # Campo: Preço Total
        # ============================
        #
        # Esse valor não é digitado pelo usuário.
        # Ele é calculado automaticamente conforme
        # a quantidade e o preço unitário informados.

        ttk.Label(frameForm, text="Preço Total (calculado):").grid(
            row=r, column=0, sticky="w", padx=6, pady=(6, 2)
        )

        ttk.Label(
            frameForm,
            textvariable=self.varPrecoTotal,
            foreground="#10225A"
        ).grid(
            row=r, column=1, sticky="w", padx=6, pady=(6, 2)
        )

        r += 1

        # Cria uma linha separadora entre
        # os campos do formulário e os botões.
        ttk.Separator(frameForm).grid(
            row=r, column=0, columnspan=2, sticky="ew", padx=6, pady=10
        )

        r += 1

        # ============================
        # Botões de operações (CRUD)
        # ============================

        # Insere uma nova venda.
        ttk.Button(
            frameForm,
            text="Cadastrar",
            style="Big.TButton",
            command=self.cadastrar
        ).grid(
            row=r, column=0, columnspan=2, sticky="ew", padx=6, pady=4
        )

        r += 1

        # Atualiza a venda selecionada.
        ttk.Button(
            frameForm,
            text="Alterar (Linha selecionada)",
            style="Big.TButton",
            command=self.alteraLinha
        ).grid(
            row=r, column=0, columnspan=2, sticky="ew", padx=6, pady=4
        )

        r += 1

        # Exclui a venda selecionada.
        ttk.Button(
            frameForm,
            text="Excluir (Linha selecionada)",
            style="Big.TButton",
            command=self.excluiLinha
        ).grid(
            row=r, column=0, columnspan=2, sticky="ew", padx=6, pady=4
        )

        r += 1

        # Limpa todos os campos do formulário.
        ttk.Button(
            frameForm,
            text="Limpar formulário",
            style="Big.TButton",
            command=self.limpaForm
        ).grid(
            row=r, column=0, columnspan=2, sticky="ew", padx=6, pady=(4, 10)
        )

        # Sempre que o conteúdo da variável
        # "Quantidade" for alterado, o método
        # recalculaTotal() será executado
        # automaticamente.
        #
        # trace_add():
        # Permite monitorar alterações em uma
        # StringVar.
        #
        # "write":
        # Indica que o evento será disparado
        # quando um novo valor for escrito.
        #
        # lambda *_:
        # Cria uma função anônima apenas para
        # chamar recalculaTotal().
        #
        # O caractere * captura os parâmetros
        # enviados automaticamente pelo trace_add,
        # mesmo que eles não sejam utilizados.

        self.varQuantidade.trace_add(
            "write",
            lambda *_: self.recalculaTotal()
        )

        # Também recalcula o valor total sempre
        # que o preço unitário for alterado.
        self.varPrecoUnit.trace_add(
            "write",
            lambda *_: self.recalculaTotal()
        )

        # Cria o painel localizado na parte
        # inferior da janela (rodapé).
        rodape = ttk.Frame(self)

        # Posiciona o rodapé na janela.
        #
        # fill="x":
        # Faz o Frame ocupar toda a largura.
        rodape.pack(
            fill="x",
            padx=12,
            pady=(0, 12)
        )

        # Cria um Label responsável por exibir
        # informações sobre a tabela, como:
        #
        # • Quantidade de registros.
        # • Soma total das vendas.
        #
        # Esses valores são atualizados
        # automaticamente pelo método
        # atualizaRodape().
        self.labelInfo = ttk.Label(
            rodape,
            text="0 linha(s) | Soma total: R$ 0,00"
        )

        # Posiciona o Label no lado direito
        # do rodapé.
        self.labelInfo.pack(side="right")

    # Carrega todas as vendas cadastradas
    # no banco de dados.
    #
    # Os registros retornados pelo repositório
    # são armazenados na lista self.dados.
    #
    # Caso exista uma ordenação ativa,
    # ela é aplicada novamente após o carregamento.
    def carregaDados(self):

        # Obtém todos os registros do banco.
        self.dados = self.repo.listarTodosDados()

        # Verifica se existe alguma coluna
        # sendo utilizada para ordenação.
        if self.ordemColuna:
            # Reaplica a ordenação atual.
            self.ordenaLista(
                self.ordemColuna,
                self.ordemReverse
            )

    # Preenche a Treeview com todos
    # os registros armazenados em self.dados.
    def populaTabela(self):

        # Remove todas as linhas existentes
        # na tabela antes de inserir
        # os novos registros.
        for isso in self.tree.get_children():
            self.tree.delete(isso)

        # Percorre todos os objetos Venda
        # armazenados na lista.
        #
        # enumerate() retorna:
        # indice -> posição do registro.
        # valor  -> objeto Venda.
        for indice, valor in enumerate(self.dados):
            # Alterna a cor das linhas,
            # criando o efeito "zebra".
            #
            # Linhas pares:
            # oddrow
            #
            # Linhas ímpares:
            # evenrow
            tag = "oddrow" if indice % 2 == 0 else "evenrow"

            # Insere uma nova linha na Treeview.
            #
            # '':
            # Indica que a linha será inserida
            # na raiz da árvore.
            #
            # tk.END:
            # Adiciona o registro no final
            # da tabela.
            #
            # iid:
            # Identificador único da linha,
            # utilizando o ID da venda.
            #
            # values:
            # Valores exibidos em cada coluna.
            #
            # tags:
            # Define qual estilo visual
            # será aplicado à linha.
            self.tree.insert(
                "",
                tk.END,
                iid=str(valor.id),
                values=(
                    valor.nomeCliente,
                    valor.cidade,
                    valor.setor,
                    valor.produto,
                    valor.quantidade,
                    formataMoedaBR(valor.precoUnitario),
                    formataDataBR(valor.dataVenda),
                    formataMoedaBR(valor.total)
                ),
                tags=(tag,)
            )

    # Atualiza as informações exibidas
    # no rodapé da aplicação.
    #
    # São mostrados:
    # • Quantidade de registros.
    # • Soma total das vendas.
    def atualizaRodape(self):

        # Calcula a soma do valor total
        # de todas as vendas cadastradas.
        #
        # sum() percorre a lista self.dados
        # e soma o atributo total de cada objeto.
        soma = sum(
            valor.total
            for valor in self.dados
        )

        # Atualiza o texto exibido
        # no Label do rodapé.
        self.labelInfo.config(
            text=f"{len(self.dados)} linha(s) | "
                 f"Soma total: {formataMoedaBR(soma)}"
        )

    # Expande ou recolhe as colunas
    # referentes aos dados do cliente.
    def toggleGrupoCliente(self):

        # Inverte o estado atual.
        #
        # False -> True
        # True -> False
        self.grupoClienteAberto = not self.grupoClienteAberto

        # Se o grupo estiver aberto,
        # exibe as colunas Cidade e Setor.
        if self.grupoClienteAberto:

            self.tree.column(
                "cidade",
                width=160,
                minwidth=80,
                anchor="w",
                stretch=True
            )

            self.tree.column(
                "setor",
                width=160,
                minwidth=80,
                anchor="center",
                stretch=True
            )

            # Atualiza o texto do botão
            # indicando que o grupo pode
            # ser recolhido.
            self.btnGrupoCliente.config(
                text="- Detalhes do cliente"
            )

        # Caso contrário, oculta novamente
        # as colunas do grupo.
        else:

            self.tree.column(
                "cidade",
                width=0,
                minwidth=0,
                stretch=False
            )

            self.tree.column(
                "setor",
                width=0,
                minwidth=0,
                stretch=False
            )

            # Atualiza o texto do botão
            # indicando que o grupo pode
            # ser expandido.
            self.btnGrupoCliente.config(
                text="+ Detalhes do cliente"
            )

    # Expande ou recolhe as colunas relacionadas
    # aos detalhes da venda.
    #
    # Quando o grupo estiver expandido, as colunas
    # Produto, Quantidade, Preço Unitário e Data
    # da Venda serão exibidas.
    #
    # Quando estiver recolhido, essas colunas
    # ficarão ocultas.
    def toggleGrupoVenda(self):

        # Inverte o estado atual do grupo.
        #
        # False -> True
        # True  -> False
        self.grupoVendaAberto = not self.grupoVendaAberto

        # Se o grupo estiver aberto,
        # exibe as colunas da venda.
        if self.grupoVendaAberto:

            self.tree.column(
                "produto",
                width=220,
                minwidth=100,
                anchor="w",
                stretch=True
            )

            self.tree.column(
                "quantidade",
                width=80,
                minwidth=50,
                anchor="center",
                stretch=False
            )

            self.tree.column(
                "precoUnitario",
                width=120,
                minwidth=90,
                anchor="e",
                stretch=False
            )

            self.tree.column(
                "dataVenda",
                width=120,
                minwidth=90,
                anchor="center",
                stretch=False
            )

            # Atualiza o texto do botão.
            self.btnGrupoVenda.config(
                text="- Detalhes da venda"
            )

        # Caso contrário, oculta todas
        # as colunas do grupo.
        else:

            self.tree.column(
                "produto",
                width=0,
                minwidth=0,
                stretch=False
            )

            self.tree.column(
                "quantidade",
                width=0,
                minwidth=50,
                stretch=False
            )

            self.tree.column(
                "precoUnitario",
                width=0,
                minwidth=0,
                stretch=False
            )

            self.tree.column(
                "dataVenda",
                width=0,
                minwidth=0,
                stretch=False
            )

            # Atualiza o texto do botão.
            self.btnGrupoVenda.config(
                text="+ Detalhes da venda"
            )

    # Ordena os registros da tabela
    # conforme a coluna selecionada.
    #
    # Se o usuário clicar novamente
    # na mesma coluna, a ordem é invertida
    # (crescente/decrescente).
    def ordenaPorColuna(self, coluna: str):

        # Ordem crescente por padrão.
        reverse = False

        # Se a coluna clicada já estiver
        # sendo utilizada na ordenação,
        # inverte o sentido.
        if self.ordemColuna == coluna:
            reverse = not self.ordemReverse

        # Ordena a lista.
        self.ordenaLista(
            coluna,
            reverse
        )

        # Atualiza a tabela.
        self.populaTabela()

        # Armazena a coluna utilizada
        # na ordenação atual.
        self.ordemColuna = coluna

        # Salva o sentido da ordenação.
        self.ordemReverse = reverse

    # Ordena a lista self.dados
    # de acordo com a coluna informada.
    #
    # Utiliza o método sort() da lista.
    def ordenaLista(self, coluna: str, reverse: bool):

        # Variável que armazenará a função
        # utilizada para comparar os objetos
        # durante a ordenação.
        keyfunction = None

        if coluna == "nomeCliente":

            # lambda cria uma função sem nome
            # (função anônima).
            #
            # É equivalente a escrever:
            #
            # def ordenar(valor):
            #     return valor.nomeCliente.lower()
            #
            # Essa função recebe um objeto Venda
            # e devolve o nome do cliente em
            # letras minúsculas.
            #
            # O método sort() utilizará esse
            # valor para comparar e ordenar
            # todos os objetos da lista.
            #
            # lower() converte o texto para
            # minúsculas, evitando diferenças
            # entre letras maiúsculas e
            # minúsculas na ordenação.
            keyfunction = lambda valor: valor.nomeCliente.lower()

        elif coluna == "cidade":

            # Ordena utilizando a cidade.
            keyfunction = lambda valor: valor.cidade.lower()

        elif coluna == "setor":

            # Ordena utilizando o setor.
            keyfunction = lambda valor: valor.setor.lower()

        elif coluna == "produto":

            # Ordena utilizando o produto.
            keyfunction = lambda valor: valor.produto.lower()

        elif coluna == "quantidade":

            # Ordena utilizando a quantidade.
            keyfunction = lambda valor: valor.quantidade

        elif coluna == "precoUnitario":

            # Ordena utilizando o preço unitário.
            keyfunction = lambda valor: valor.precoUnitario

        elif coluna == "dataVenda":

            # Ordena utilizando a data da venda.
            keyfunction = lambda valor: valor.dataVenda

        elif coluna == "total":

            # Ordena utilizando o valor total.
            keyfunction = lambda valor: valor.total

        # Se uma função de comparação foi criada,
        # ordena a lista de objetos Venda.
        if keyfunction:
            # sort() reorganiza os elementos da lista.
            #
            # key:
            # Define qual informação será utilizada
            # para comparar os objetos.
            #
            # reverse:
            # False -> ordem crescente.
            # True  -> ordem decrescente.
            self.dados.sort(
                key=keyfunction,
                reverse=reverse
            )

    # Recalcula automaticamente o valor total da venda.
    #
    # Esse método é chamado sempre que o usuário altera
    # a quantidade ou o preço unitário.
    #
    # O cálculo realizado é:
    #
    # Total = Quantidade × Preço Unitário
    def recalculaTotal(self):

        try:

            # Obtém o texto digitado no campo Quantidade.
            #
            # get() retorna o conteúdo da StringVar.
            #
            # strip() remove espaços no início e no fim.
            #
            # Se o campo estiver vazio, utiliza 0
            # para evitar erro na conversão.
            quantidadeTotal = (
                int(self.varQuantidade.get())
                if self.varQuantidade.get().strip()
                else 0
            )

            # Obtém o preço digitado.
            #
            # parsePrecoBR() converte um texto
            # no formato brasileiro (1.234,56)
            # para um número decimal (float).
            #
            # Se o campo estiver vazio,
            # utiliza 0.0.
            preco = (
                parsePrecoBR(self.varPrecoUnit.get())
                if self.varPrecoUnit.get().strip()
                else 0.0
            )

            # Multiplica a quantidade pelo preço
            # unitário e exibe o resultado no
            # Label "Preço Total".
            #
            # formataMoedaBR() converte o número
            # para o formato monetário brasileiro.
            self.varPrecoTotal.set(
                formataMoedaBR(
                    quantidadeTotal * preco
                )
            )

        # Caso o usuário digite algum valor
        # inválido (como letras), a conversão
        # gera uma exceção.
        #
        # Nesse caso o total exibido volta
        # para R$ 0,00.
        except Exception:

            self.varPrecoTotal.set("R$ 0,00")

    # Valida todos os campos do formulário
    # antes de cadastrar ou alterar uma venda.
    #
    # O método retorna uma tupla contendo:
    #
    # bool  -> informa se a validação foi bem-sucedida.
    # str   -> nome do cliente.
    # str   -> cidade.
    # str   -> setor.
    # str   -> produto.
    # int   -> quantidade.
    # float -> preço unitário.
    # date  -> data da venda.
    def validaFormulario(self) -> tuple[bool, str, str, str, str, int, float, date]:

        try:

            # Obtém os textos digitados pelo usuário.
            #
            # strip() remove espaços extras.
            nomeCliente = self.varNomeCliente.get().strip()
            cidade = self.varCidade.get().strip()
            setor = self.varSetor.get().strip()
            produto = self.varProduto.get().strip()

            # Verifica se algum dos campos obrigatórios
            # ficou vazio.
            #
            # O operador "and" retorna False
            # caso qualquer campo esteja vazio.
            if not (nomeCliente and cidade and setor and produto):
                # raise cria manualmente uma exceção.
                #
                # A execução é interrompida e enviada
                # para o bloco except.
                raise ValueError(
                    "Preencha o Nome do Cliente, Cidade, Setor e Produto."
                )

            # Converte a quantidade para inteiro.
            qntd = int(
                self.varQuantidade.get().strip()
            )

            # Quantidade deve ser positiva.
            if qntd <= 0:
                raise ValueError(
                    "Quantidade deve ser um inteiro positivo."
                )

            # Converte o preço informado
            # para float.
            preco = parsePrecoBR(
                self.varPrecoUnit.get().strip()
            )

            # O preço deve ser maior que zero.
            if preco <= 0:
                raise ValueError(
                    "Preço unitário deve ser maior que zero."
                )

            # Converte o texto digitado
            # para um objeto date.
            data = parseDataBR(
                self.varData.get().strip()
            )

            # Se todas as validações passaram,
            # retorna True juntamente com todos
            # os valores convertidos.
            return (
                True,
                nomeCliente,
                cidade,
                setor,
                produto,
                qntd,
                float(preco),
                data
            )

        # Captura apenas erros de validação.
        except ValueError as error:

            # Exibe a mensagem de erro
            # para o usuário.
            messagebox.showerror(
                "Validação",
                str(error)
            )

            # Retorna False indicando
            # que o formulário é inválido.
            #
            # Os demais valores retornam
            # vazios apenas para manter
            # o padrão da tupla.
            return (
                False,
                "",
                "",
                "",
                "",
                0,
                0.0,
                date.today()
            )

    # Realiza o cadastro de uma nova venda.
    def cadastrar(self):

        # Primeiro valida todos os dados
        # digitados no formulário.
        #
        # A função retorna:
        #
        # ok -> informa se tudo está válido.
        # Os demais valores são os dados
        # convertidos para seus respectivos tipos.
        ok, nomeCliente, cidade, setor, produto, qntd, preco, data = (
            self.validaFormulario()
        )

        # Caso exista algum erro,
        # interrompe o cadastro.
        if not ok:
            return

        try:

            # Envia os dados para o repositório,
            # que será responsável por inserir
            # o registro no banco de dados.
            #
            # O método retorna o ID gerado
            # automaticamente pelo banco.
            novoId = self.repo.inserirVenda(
                nomeCliente,
                cidade,
                setor,
                produto,
                qntd,
                preco,
                data
            )

            # Exibe mensagem de sucesso.
            messagebox.showinfo(
                "Sucesso",
                f"Registro inserido com sucesso (ID: {novoId})"
            )

            # Recarrega os dados do banco.
            self.carregaDados()

            # Atualiza a Treeview.
            self.populaTabela()

            # Atualiza as informações
            # do rodapé.
            self.atualizaRodape()

            # Limpa todos os campos
            # do formulário.
            self.limpaForm()

        # Captura qualquer erro ocorrido
        # durante o cadastro.
        except Exception as error:

            messagebox.showerror(
                "Erro ao inserir",
                str(error)
            )

    # Altera os dados da venda atualmente
    # selecionada na tabela.
    def alteraLinha(self):

        # Verifica se existe algum registro
        # selecionado.
        #
        # idSelecionado recebe o ID da venda
        # quando o usuário clica em uma linha
        # da Treeview.
        #
        # Se nenhum registro foi selecionado,
        # não é possível realizar a alteração.
        if self.idSelecionado is None:
            # Exibe uma mensagem de aviso.
            messagebox.showwarning(
                "Atenção!",
                "Selecione uma linha para alterar."
            )

            # Encerra a execução do método.
            return

        # Valida todos os campos do formulário.
        #
        # Caso algum dado seja inválido,
        # ok será False.
        ok, nomeCliente, cidade, setor, produto, qntd, preco, data = (
            self.validaFormulario()
        )

        # Interrompe a alteração caso
        # existam erros de validação.
        if not ok:
            return

        try:

            # Envia os novos dados para o
            # repositório, que será responsável
            # por atualizar o registro no banco.
            self.repo.atualizarVenda(
                self.idSelecionado,
                nomeCliente,
                cidade,
                setor,
                produto,
                qntd,
                preco,
                data
            )

            # Informa que a alteração foi realizada.
            messagebox.showinfo(
                "Sucesso.",
                f"Registro de ID {self.idSelecionado} "
                f"atualizado com sucesso."
            )

            # Recarrega os dados atualizados
            # do banco de dados.
            self.carregaDados()

            # Atualiza a tabela exibida.
            self.populaTabela()

            # Atualiza as informações do rodapé.
            self.atualizaRodape()

            # Limpa o formulário para um
            # novo cadastro ou seleção.
            self.limpaForm()

        # Captura qualquer erro ocorrido
        # durante a atualização.
        except Exception as error:

            messagebox.showerror(
                "Erro ao atualizar!",
                str(error)
            )

    # Exclui a venda atualmente
    # selecionada na tabela.
    def excluiLinha(self):

        # Verifica se existe uma linha
        # selecionada.
        if self.idSelecionado is None:
            messagebox.showwarning(
                "Atenção!",
                "Selecione uma linha para excluir."
            )

            return

        # Exibe uma caixa de confirmação.
        #
        # askyesno() retorna:
        #
        # True  -> usuário clicou em "Sim".
        # False -> usuário clicou em "Não".
        #
        # O operador "not" verifica se o
        # usuário recusou a exclusão.
        if not messagebox.askyesno(
                "Confirmação",
                f"Deseja mesmo excluir o registro de ID "
                f"{self.idSelecionado}?"
        ):
            # Cancela a operação.
            return

        try:

            # Solicita ao repositório
            # que remova o registro
            # do banco de dados.
            self.repo.excluirVenda(
                self.idSelecionado
            )

            # Exibe mensagem de sucesso.
            messagebox.showinfo(
                "Sucesso",
                f"Registro de ID {self.idSelecionado} "
                f"excluído com sucesso."
            )

            # Atualiza os dados carregados
            # do banco.
            self.carregaDados()

            # Atualiza a tabela.
            self.populaTabela()

            # Atualiza o rodapé.
            self.atualizaRodape()

            # Limpa os campos do formulário.
            self.limpaForm()

        # Captura qualquer erro ocorrido
        # durante a exclusão.
        except Exception as error:

            messagebox.showerror(
                "Erro ao excluir!",
                str(error)
            )

    # Limpa todos os campos do formulário
    # e remove a seleção atual.
    def limpaForm(self):

        # Nenhuma venda ficará selecionada.
        self.idSelecionado = None

        # Limpa os campos de texto.
        #
        # set("") atribui uma string vazia
        # à StringVar, apagando o conteúdo
        # exibido na interface.
        self.varNomeCliente.set("")

        self.varCidade.set("")

        self.varSetor.set("")

        self.varProduto.set("")

        self.varQuantidade.set("")

        self.varPrecoUnit.set("")

        self.varData.set("")

        # Reinicia o preço total para
        # o valor padrão.
        self.varPrecoTotal.set("R$ 0,00")

# Este bloco garante que a aplicação
# será iniciada apenas quando este
# arquivo for executado diretamente.
#
# Se este arquivo for apenas importado
# por outro programa, o código abaixo
# não será executado.
if __name__ == "__main__":

    # Cria a janela principal da aplicação.
    app = appAgrupamentoDeColunas()

    # Inicia o loop principal do Tkinter.
    #
    # mainloop() mantém a janela aberta,
    # aguardando as ações do usuário,
    # como cliques, digitação e seleção
    # de componentes.
    #
    # Quando a janela é fechada, esse
    # laço termina e o programa é encerrado.
    app.mainloop()

















