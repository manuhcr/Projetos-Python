import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from repositorio import RepoEventos

formBR = "%d/%m/%Y"
formISO = "%Y-%m-%d"


# Classe principal da aplicação.
# Herda da classe Tk do Tkinter, o que significa que esta classe possui
# todos os recursos de uma janela gráfica do Tkinter.
class AppFiltroEntreDatas(tk.Tk):

    # Método construtor da classe.
    # É executado automaticamente quando um objeto
    # AppFiltroEntreDatas é criado.
    def __init__(self) -> None:
        # Executa o construtor da classe pai (tk.Tk).
        # Esse comando inicializa toda a estrutura interna
        # da janela do Tkinter, permitindo utilizar métodos
        # como title(), geometry(), minsize(), mainloop(), etc.
        super().__init__()

        # Define o texto exibido na barra de título da janela.
        self.title('Filtro entre datas - Formato BR')

        # Chama o método responsável por centralizar a janela
        # na tela com largura de 1000 pixels e altura de 600 pixels.
        self.alinharCentro(1000, 600)

        # Define o tamanho mínimo permitido para a janela.
        # O usuário não poderá redimensioná-la para valores menores.
        self.minsize(900, 520)

        # Cria uma instância da classe RepoEventos.
        # Esse objeto será utilizado para realizar todas as operações
        # relacionadas ao banco de dados:
        # - Inserir eventos
        # - Atualizar eventos
        # - Excluir eventos
        # - Consultar eventos
        # - Gerar backups
        self.repo = RepoEventos()

        # Cria uma variável do Tkinter para armazenar a data inicial
        # informada pelo usuário. StringVar permite vincular o valor diretamente
        # a componentes gráficos como Entry.
        self.varDataIni = tk.StringVar()

        # Cria uma variável do Tkinter para armazenar a data final informada pelo usuário.
        # Essa variável será utilizada nos filtros de pesquisa por intervalo de datas.
        self.varDataFim = tk.StringVar()

        # Cria uma variável do Tkinter para armazenar textos digitados pelo usuário.
        # Pode ser utilizada em campos de pesquisa, filtros ou qualquer entrada
        # textual da interface.
        self.varTexto = tk.StringVar()

        # Cria uma variável responsável por armazenar a descrição de um evento.
        # Geralmente é vinculada ao campo onde o usuário informa ou edita
        # o nome/descrição do evento.
        self.varDesc = tk.StringVar()

        # Cria uma variável para armazenar a data informada pelo usuário.
        # Essa variável normalmente é associada a um campo Entry utilizado
        # para cadastro ou edição.
        self.varData = tk.StringVar()

        # Variável responsável por armazenar o ID do evento atualmente
        # selecionado pelo usuário na interface.
        # Quando um registro é selecionado em componentes como Treeview,
        # Listbox ou Combobox, o identificador do evento pode ser armazenado
        # nesta variável para que operações como edição, exclusão ou consulta
        # sejam realizadas sobre o registro correto.
        # O tipo "int | None" indica que a variável pode armazenar um número
        # inteiro (ID do evento) ou None quando nenhum item estiver selecionado.
        self.varIdSelecionado: int | None = None

        # Chama o método responsável por criar e organizar
        # todos os componentes gráficos da interface.
        self.montarLayoutUI()

        # Chama o método responsável por atualizar os dados
        # exibidos na tela logo após a inicialização da aplicação.
        # Esse método consulta o banco de dados, carrega os registros
        # existentes e preenche os componentes visuais da interface.
        # Dessa forma, o usuário já visualiza as informações
        # mais recentes ao abrir o sistema.
        self.atualizarTabelaEvento()

    # Método responsável por centralizar a janela
    # no centro da tela do usuário.
    # Recebe como parâmetros a largura e a altura
    # que a janela deverá possuir.
    def alinharCentro(self, largura: int, altura: int):
        # Força o Tkinter a processar imediatamente todas as
        # as atualizações pendentes da interface gráfica.

        # Quando uma janela ou componente é criado, o Tkinter
        # nem sempre calcula seu tamanho e posição imediatamente.
        # Muitas dessas operações ficam armazenadas em uma fila
        # interna aguardando processamento.

        # O método update_idletasks() executa essas tarefas
        # pendentes sem iniciar o loop principal da aplicação.

        # Isso garante que informações da interface, como
        # dimensões, layout e posicionamento dos componentes,
        # estejam atualizadas antes dos próximos cálculos.

        # Neste caso, ele é utilizado antes de calcular a posição
        # da janela para garantir que os valores utilizados
        # sejam os corretos.
        self.update_idletasks()

        # Obtém a largura total da tela do computador.
        # Exemplo: 1920 pixels.
        tl = self.winfo_screenwidth()

        # Obtém a altura total da tela do computador.
        # Exemplo: 1080 pixels.
        ta = self.winfo_screenheight()

        # Calcula a posição horizontal (eixo X)
        # necessária para centralizar a janela.
        # Exemplo:
        # Tela: 1920px
        # Janela: 1000px
        # (1920 / 2) - (1000 / 2)
        # 960 - 500 = 460
        # Utiliza divisão inteira (//) para garantir que
        # o resultado seja um número inteiro, evitando
        # posições com casas decimais ao definir a localização
        # da janela na tela.
        x = (tl // 2) - (largura // 2)

        # Calcula a posição vertical (eixo Y)
        # necessária para centralizar a janela.
        # Exemplo:
        # Tela: 1080px
        # Janela: 600px
        # (1080 / 2) - (600 / 2)
        # 540 - 300 = 240
        # Também utiliza a divisão inteira
        y = (ta // 2) - (altura // 2)

        # Define o tamanho da janela e sua posição.
        # Formato:
        # largura x altura + posiçãoX + posiçãoY
        # Exemplo:
        # 1000x600+460+240
        # Resultado:
        # Janela com 1000x600 pixels,
        # centralizada na tela.
        self.geometry(f"{largura}x{altura}+{x}+{y}")

    # Método responsável por construir toda a interface gráfica
    # da aplicação.
    #
    # Neste método são criados e organizados todos os componentes
    # visuais que o usuário utilizará durante a execução do sistema,
    # incluindo:
    #
    # - Área de filtros
    # - Campos para pesquisa
    # - Botões de consulta
    # - Tabela de resultados
    # - Formulário de cadastro
    # - Botões de manutenção dos registros
    #
    # A interface é dividida em duas grandes seções:
    #
    # 1. Parte superior:
    #    Utilizada para filtrar os eventos cadastrados.
    #
    # 2. Parte central:
    #    Exibe a tabela de eventos e o formulário de cadastro,
    #    alteração e exclusão.
    def montarLayoutUI(self):
        # Cria uma área visual com borda e título para agrupar
        # os componentes relacionados aos filtros de pesquisa.
        #
        # self:
        #     Indica que o LabelFrame será criado dentro da
        #     janela principal da aplicação.
        #
        # text:
        #     Define o título exibido na borda superior do frame,
        #     ajudando o usuário a identificar sua finalidade.
        frameFiltro = tk.LabelFrame(
            self,
            text="Filtro entre datas (data inicial / data final / texto na descrição)"
        )

        # Exibe o frame na janela principal.
        #
        # fill="x":
        #     Faz o frame ocupar toda a largura disponível
        #     da janela, acompanhando redimensionamentos.
        #
        # padx=10:
        #     Adiciona 10 pixels de espaço externo nas laterais.
        #
        # pady=10:
        #     Adiciona 10 pixels de espaço externo acima e abaixo.
        frameFiltro.pack(
            fill="x",
            padx=10,
            pady=10
        )
        # Cria um texto fixo na tela para informar ao usuário
        # qual informação deve ser digitada no campo ao lado.
        #
        # frameFiltro:
        #     Define que o rótulo será exibido dentro do frame de filtros.
        #
        # text:
        #     Conteúdo textual que será exibido ao usuário.
        # grid:
        # Posiciona o componente utilizando uma grade semelhante a uma planilha de Excel.
        #
        # row=0:
        #     Primeira linha da grade.
        #
        # column=0:
        #     Primeira coluna da grade.
        #
        # padx=6 e pady=6:
        # Espaçamento externo para melhorar a organização visual.
        #
        # sticky="w":
        #     Alinha o componente à esquerda da célula.
        ttk.Label(
            frameFiltro,
            text="Data Inicial").grid(
         row=0,
         column=0,
         padx=6,
         pady=6,
         sticky="w"
        )

        # Cria um campo de texto onde o usuário poderá
        # digitar a data inicial do filtro.
        #
        # frameFiltro:
        #     Frame que conterá o campo.
        #
        # textvariable=self.varDataIni:
        #     Conecta o campo à variável varDataIni.
        #     Tudo que o usuário digitar será armazenado nela.
        #
        # width=14:
        #     Define aproximadamente a quantidade de caracteres
        #     visíveis no campo.
        insereDataIni = tk.Entry(
            frameFiltro,
            textvariable=self.varDataIni,
            width=14
        )

        # Posiciona o campo de data inicial dentro do frame
        # utilizando o gerenciador de layout grid().
        #
        # row=0:
        #     Coloca o campo na primeira linha da grade.
        #
        # column=1:
        #     Coloca o campo na segunda coluna da grade.
        #     A coluna 0 já está sendo utilizada pelo Label
        #     "Data Inicial".
        #
        # padx=6:
        #     Adiciona um espaçamento externo horizontal de
        #     6 pixels nas laterais do componente.
        #
        # pady=6:
        #     Adiciona um espaçamento externo vertical de
        #     6 pixels acima e abaixo do componente.
        #
        # sticky="w":
        #     Alinha o campo à esquerda da célula da grade.
        #     O "w" significa West (Oeste), que no Tkinter
        #     representa o lado esquerdo.
        insereDataIni.grid(
            row=0,
            column=1,
            padx=6,
            pady=6,
            sticky="w"
        )
        # Cria um rótulo (texto fixo) para identificar
        # o campo onde o usuário deverá informar a data final
        # utilizada no filtro de pesquisa.
        ttk.Label(
            frameFiltro,
            text="Data Final"
        ).grid(

            # Primeira linha da grade.
            row=0,

            # Terceira coluna da grade.
            # As colunas 0 e 1 já estão sendo utilizadas
            # pelo rótulo e pelo campo da data inicial.
            column=2,

            # Espaçamento externo horizontal.
            padx=6,

            # Espaçamento externo vertical.
            pady=6
        )

        # Cria um campo de texto onde o usuário poderá
        # digitar a data final do filtro.
        #
        # textvariable=self.varDataFim:
        #     Vincula o conteúdo digitado à variável
        #     self.varDataFim, permitindo acessar o valor
        #     posteriormente através do método get().
        #
        # width=14:
        #     Define a largura aproximada do campo em caracteres.
        #     Esse tamanho é suficiente para exibir datas no
        #     formato dd/mm/aaaa.
        insereDataFim = tk.Entry(
            frameFiltro,
            textvariable=self.varDataFim,
            width=14
        )

        # Posiciona o campo de data final ao lado do rótulo.
        insereDataFim.grid(

            # Primeira linha da grade.
            row=0,

            # Quarta coluna da grade.
            # Fica logo após o rótulo "Data Final".
            column=3,

            # Espaçamento externo horizontal.
            padx=6,

            # Espaçamento externo vertical.
            pady=6,

            # Alinha o campo à esquerda da célula.
            # "w" significa West (Oeste).
            sticky="w"
        )

        # Cria um rótulo para identificar o campo de
        # pesquisa por descrição.
        #
        # O usuário poderá digitar palavras ou trechos
        # de texto para localizar eventos específicos.
        ttk.Label(
            frameFiltro,
            text="Descrição"
        ).grid(

            # Primeira linha da grade.
            row=0,

            # Quinta coluna da grade.
            column=4,

            # Espaçamentos externos.
            padx=6,
            pady=6,

            # Mantém o texto alinhado à esquerda.
            sticky="w"
        )

        # Cria o campo utilizado para pesquisar eventos
        # através de palavras presentes na descrição.
        #
        # Exemplo:
        # "Python"
        # "Workshop"
        # "Reunião"
        #
        # textvariable=self.varTexto:
        #     Armazena automaticamente o texto digitado
        #     pelo usuário na variável self.varTexto.
        #
        # width=40:
        #     Define uma largura maior para facilitar a
        #     digitação de descrições mais longas.
        insereDescricaoFiltro = tk.Entry(
            frameFiltro,
            textvariable=self.varTexto,
            width=40
        )

        # Posiciona o campo de descrição ao lado do
        # rótulo "Descrição".
        insereDescricaoFiltro.grid(

            # Primeira linha da grade.
            row=0,

            # Sexta coluna da grade.
            column=5,

            # Espaçamentos externos.
            padx=6,
            pady=6,

            # Mantém o campo alinhado à esquerda.
            sticky="w"
        )

        # Cria um botão que executará a pesquisa dos eventos.
        #
        # text:
        #     Texto exibido no botão.
        #
        # command=self.atualizarTabelaEvento:
        #     Define qual método será executado quando
        #     o usuário clicar no botão.
        #
        # width=22:
        #     Largura aproximada do botão em caracteres.
        btnAplicar = ttk.Button(
            frameFiltro,
            text="Aplicar Filtro",
            command=self.atualizarTabelaEvento,
            width=22
        )

        # Posiciona o botão "Aplicar Filtro" na grade do frame.
        #
        # row=0:
        #     Primeira linha da grade.
        #
        # column=6:
        #     Sétima coluna da grade. O botão é exibido após
        #     os campos de data inicial, data final e descrição.
        #
        # padx=6:
        #     Adiciona espaçamento horizontal externo.
        #
        # pady=6:
        #     Adiciona espaçamento vertical externo.
        btnAplicar.grid(
            row=0,
            column=6,
            padx=6,
            pady=6
        )

        # Botão responsável por limpar todos os filtros
        # preenchidos na área de pesquisa.
        #
        # Após a limpeza, normalmente todos os registros
        # voltam a ser exibidos.
        btnLimpar = ttk.Button(
            frameFiltro,
            text="Limpar Filtros",
            command=self.limpaFiltro,
            width=22
        )

        # Posiciona o botão "Limpar Filtros" na grade do frame.
        #
        # row=0:
        #     Primeira linha da grade.
        #
        # column=7:
        #     Oitáva coluna da grade. O botão é exibido após
        #     os campos de data inicial, data final e descrição.
        #
        # padx=6:
        #     Adiciona espaçamento horizontal externo.
        #
        # pady=6:
        #     Adiciona espaçamento vertical externo.
        btnLimpar.grid(
            row=0,
            column=7,
            padx=6,
            pady=6
        )

        # Cria um Frame que servirá como contêiner principal
        # da área central da aplicação.
        #
        # Um Frame funciona como uma "caixa organizadora",
        # permitindo agrupar e posicionar outros componentes.
        #
        # Neste caso, ele armazenará:
        # - A tabela de eventos;
        # - O formulário de cadastro, alteração e exclusão.
        frameCentro = ttk.Frame(self)

        # Exibe o frame central na janela principal.
        #
        # fill="both":
        #     Faz o frame ocupar toda a largura e altura
        #     disponíveis na janela.
        #
        # expand=True:
        #     Permite que o frame aumente de tamanho quando
        #     a janela for redimensionada.
        #
        # padx=10 e pady=5:
        #     Adicionam espaçamentos externos para melhorar
        #     a organização visual da interface.
        frameCentro.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        # Cria uma área com borda e título para exibir
        # os eventos retornados pela consulta.
        #
        # O LabelFrame ajuda a separar visualmente a
        # tabela das demais áreas da aplicação.
        #
        # text:
        #     Texto exibido na borda superior do componente.
        frameTabela = ttk.LabelFrame(
            frameCentro,
            text="Eventos (conforme os filtros)"
        )

        # Posiciona o frame da tabela no lado esquerdo
        # da área central da aplicação.
        #
        # side="left":
        #     Mantém a tabela à esquerda do formulário.
        #
        # fill="both":
        #     Faz o frame ocupar toda a largura e altura
        #     disponíveis na região onde foi inserido.
        #
        # expand=True:
        #     Permite que a tabela cresça quando houver
        #     espaço livre na janela.
        frameTabela.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Define os identificadores internos das colunas
        # que serão utilizadas pela Treeview.
        #
        # Esses nomes não são necessariamente exibidos
        # ao usuário, mas são utilizados pelo Tkinter
        # para identificar cada coluna da tabela.
        colunas = (
            "id",
            "dataEvento",
            "descricao"
        )

        # Cria uma tabela para exibir os eventos
        # retornados pelo banco de dados.
        #
        # columns=colunas:
        #     Define quais colunas existirão na tabela.
        #
        # show="headings":
        #     Exibe apenas os cabeçalhos e os dados,
        #     ocultando a coluna de árvore padrão.
        #
        # height=18:
        #     Define a quantidade aproximada de linhas
        #     visíveis simultaneamente.
        self.tree = ttk.Treeview(
            frameTabela,
            columns=colunas,
            show="headings",
            height=18
        )

        # Define os títulos que serão exibidos
        # no cabeçalho de cada coluna.
        self.tree.heading("id", text="ID do evento")
        self.tree.heading("dataEvento", text="Data do evento")
        self.tree.heading("descricao", text="Descrição do evento")

        # Configura a aparência da coluna de descrição.
        #
        # width=250:
        #     Define a largura da coluna em pixels.
        #
        # anchor="w":
        #     Alinha o conteúdo à esquerda da célula.
        #     "w" significa West (Oeste).
        #     "center" significa centro.
        self.tree.column(
            "descricao",
            width=250,
            anchor="w"
        )
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("dataEvento", width=120, anchor="center")
        self.tree.column("descricao", width=250, anchor="w")

        # Exibe a Treeview dentro do frame da tabela.
        #
        # fill="both":
        #     Faz a tabela ocupar todo o espaço disponível
        #     tanto na largura quanto na altura do frame.
        #
        # expand=True:
        #     Permite que a tabela aumente ou diminua de tamanho
        #     automaticamente quando a janela for redimensionada,
        #     aproveitando todo o espaço disponível.
        #
        # Sem essas configurações, a Treeview ocuparia apenas
        # o tamanho mínimo necessário para exibir seu conteúdo.
        self.tree.pack(
            fill="both",
            expand=True
        )

        # Associa o evento de seleção de linha ao método
        # capturaSelecao().
        #
        # Sempre que o usuário clicar em um registro da
        # tabela, o método será executado automaticamente,
        # carregando os dados do evento para o formulário.
        self.tree.bind(
            "<<TreeviewSelect>>",
            self.capturaSelecao
        )

        # Cria uma barra de rolagem vertical que será utilizada
        # para navegar pelos registros da tabela quando a quantidade
        # de eventos ultrapassar o espaço visível da Treeview.
        #
        # frameTabela:
        #     Define que a barra será exibida dentro do frame
        #     que contém a tabela.
        #
        # orient="vertical":
        #     Indica que a barra de rolagem será exibida na vertical.
        #
        # command=self.tree.yview:
        #     Conecta a barra de rolagem à movimentação vertical
        #     da Treeview. Quando o usuário movimentar a barra,
        #     a tabela também será movimentada.
        bsv = ttk.Scrollbar(
            frameTabela,
            orient="vertical",
            command=self.tree.yview
        )
        # Conecta a Treeview à barra de rolagem vertical.
        #
        # yscrollcommand=bsv.set:
        #     Sempre que a posição da tabela mudar,
        #     o método set() da Scrollbar será chamado
        #     automaticamente para atualizar a posição
        #     visual da barra.
        #
        # Dessa forma, a barra acompanha a movimentação
        # da tabela e permanece sincronizada com os dados
        # exibidos na tela.
        self.tree.configure(
            yscrollcommand=bsv.set
        )

        # Exibe a barra de rolagem na interface.
        #
        # side="right":
        #     Posiciona a barra no lado direito do frame
        #     que contém a tabela.
        #
        # fill="y":
        #     Faz a barra ocupar toda a altura disponível
        #     do frame, acompanhando o tamanho da Treeview.
        bsv.pack(
            side="right",
            fill="y"
        )

        # Cria um LabelFrame que agrupa todos os componentes
        # relacionados ao cadastro, alteração e exclusão de eventos.
        #
        # O LabelFrame funciona como um contêiner visual,
        # permitindo organizar os campos e botões em uma área
        # específica da interface.
        frameFormulario = ttk.LabelFrame(
            frameCentro,
            text="Cadastrar Evento / Alterar Evento / Excluir Evento"
        )

        # Exibe o frame do formulário dentro do frame central.
        #
        # side="right":
        #     Posiciona o formulário no lado direito da tela,
        #     deixando a tabela de eventos no lado esquerdo.
        #
        # fill="y":
        #     Faz o frame ocupar toda a altura disponível
        #     do contêiner onde está inserido.
        #
        # padx=(8, 0):
        #     Adiciona um espaçamento externo de 8 pixels
        #     à esquerda do formulário e 0 pixels à direita.
        #     Isso evita que o formulário fique encostado
        #     na tabela.
        frameFormulario.pack(
            side="right",
            fill="y",
            padx=(8, 0)
        )

        # Cria um rótulo (Label) para identificar o campo
        # onde o usuário deverá informar a descrição do evento.
        #
        # frameFormulario:
        #     Define que o rótulo será exibido dentro do
        #     formulário de cadastro.
        #
        # text="Descrição:":
        #     Texto exibido ao usuário para indicar
        #     qual informação deve ser preenchida.
        ttk.Label(
            frameFormulario,
            text="Descrição:"
        ).grid(

            # Primeira linha da grade do formulário.
            row=0,

            # Primeira coluna da grade.
            column=0,

            # Espaçamento externo horizontal de 6 pixels.
            padx=6,

            # Espaçamento externo vertical de 6 pixels.
            pady=6,

            # Mantém o texto alinhado à esquerda da célula.
            #
            # "w" significa West (Oeste), que representa
            # o lado esquerdo no sistema de posicionamento
            # utilizado pelo Tkinter.
            sticky="w"
        )

        # Campo utilizado para digitação da descrição do evento.
        #
        # O texto digitado será armazenado automaticamente
        # na variável self.varDesc.
        #
        # Exemplo:
        # "Workshop Python"
        # "Reunião Comercial"
        # "Entrega Relatório Final"
        insereDescricao = ttk.Entry(
            frameFormulario,
            textvariable=self.varDesc,
            width=36
        )

        # Posiciona o campo de descrição ao lado do rótulo.
        #
        # row=0:
        #     Primeira linha da grade.
        #
        # column=1:
        #     Segunda coluna da grade. A primeira coluna
        #     já está ocupada pelo Label "Descrição".
        #
        # padx=6:
        #     Espaçamento horizontal externo.
        #
        # pady=(10, 6):
        #     Adiciona 10 pixels acima e 6 pixels abaixo.
        #
        # sticky="w":
        #     Mantém o campo alinhado à esquerda da célula.
        insereDescricao.grid(
            row=0,
            column=1,
            padx=6,
            pady=(10, 6),
            sticky="w"
        )

        # Cria um rótulo para identificar o campo
        # de data do evento.
        ttk.Label(
            frameFormulario,
            text="Data do evento:"
        ).grid(
            row=1,
            column=0,
            padx=6,
            pady=6,
            sticky="w"
        )

        # Campo utilizado para informar a data
        # em que o evento ocorrerá.
        #
        # O valor digitado será armazenado
        # na variável self.varData.
        #
        # Exemplo:
        # 15/06/2026
        # 01/01/2030
        insereData = ttk.Entry(
            frameFormulario,
            textvariable=self.varData,
            width=16
        )

        # Posiciona o campo de data ao lado do rótulo
        # "Data do evento".
        #
        # row=1:
        #     Segunda linha da grade.
        #
        # column=1:
        #     Segunda coluna da grade.
        #
        # sticky="w":
        #     Mantém o campo alinhado à esquerda.
        insereData.grid(
            row=1,
            column=1,
            padx=6,
            pady=6,
            sticky="w"
        )

        # Cria uma linha horizontal utilizada apenas para
        # melhorar a organização visual da interface.
        #
        # row=2:
        #     Terceira linha da grade.
        #
        # columnspan=2:
        #     Faz a linha ocupar duas colunas da grade,
        #     atravessando toda a largura do formulário.
        #
        # sticky="ew":
        #     Faz a linha se estender da esquerda (west)
        #     para a direita (east), ocupando toda a célula.
        ttk.Separator(frameFormulario).grid(
            row=2,
            column=0,
            columnspan=2,
            padx=6,
            pady=10,
            sticky="ew"
        )

        # Cria um botão responsável por cadastrar
        # um novo evento no banco de dados.
        #
        # text:
        #     Texto exibido ao usuário.
        #
        # command=self.cadastraEvento:
        #     Método executado quando o botão for clicado.
        #     Esse método valida os dados e realiza o cadastro.
        btnCadastrar = ttk.Button(
            frameFormulario,
            text="Cadastrar Evento",
            command=self.cadastraEvento
        )

        # Posiciona o botão de cadastro.
        #
        # row=3:
        #     Quarta linha da grade.
        #
        # columnspan=2:
        #     Faz o botão ocupar as duas colunas
        #     do formulário.
        #
        # sticky="ew":
        #     Faz o botão ocupar toda a largura
        #     disponível da linha.
        btnCadastrar.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=6,
            pady=6,
            sticky="ew"
        )

        # Cria um botão responsável por excluir
        # um evento no banco de dados e na tabela.
        #
        # text:
        #     Texto exibido ao usuário.
        #
        # command=self.excluiEvento:
        #     Executa o método responsável por remover
        #     o evento atualmente selecionado na tabela.
        btnExcluir = ttk.Button(
            frameFormulario,
            text="Excluir (evento selecionado)",
            command=self.excluiEvento

        )

        # Posiciona o botão de excluir.
        #
        # row=4:
        #     Quinta linha da grade.
        #
        # columnspan=2:
        #     Faz o botão ocupar as duas colunas
        #     do formulário.
        #
        # sticky="ew":
        #     Faz o botão ocupar toda a largura
        #     disponível da linha.
        btnExcluir.grid(
            row=4,
            column=0,
            columnspan=2,
            padx=6,
            pady=6,
            sticky="ew"
        )

        # Cria um botão responsável por alterar
        # um evento selecionado no banco de dados
        # e na tabela.
        #
        # text:
        #     Texto exibido ao usuário.
        #
        # command=self.alteraEvento:
        #     Executa o método responsável por atualizar
        #     os dados do evento selecionado.
        btnAlterar = ttk.Button(
            frameFormulario,
            text="Alterar (evento selecionado)",
            command=self.alteraEvento
        )

        # Posiciona o botão de cadastro.
        #
        # row=5:
        #     Sexta linha da grade.
        #
        # columnspan=2:
        #     Faz o botão ocupar as duas colunas
        #     do formulário.
        #
        # sticky="ew":
        #     Faz o botão ocupar toda a largura
        #     disponível da linha.
        btnAlterar.grid(
            row=5,
            column=0,
            columnspan=2,
            padx=6,
            pady=6,
            sticky="ew"
        )

        # Cria um botão responsável por limpar
        # o formulário
        #
        # text:
        #     Texto exibido ao usuário.
        #
        # command=self.limpaFormulario:
        #     Executa o método responsável por limpar
        #     o formulário
        btnLimparForm = ttk.Button(
            frameFormulario,
            text="Limpar Formulário",
            command=self.limpaFormulario
        )

        # Posiciona o botão de limpar formulário.
        #
        # row=6:
        #     Sétima linha da grade.
        #
        # columnspan=2:
        #     Faz o botão ocupar as duas colunas
        #     do formulário.
        #
        # sticky="ew":
        #     Faz o botão ocupar toda a largura
        #     disponível da linha.
        btnLimparForm.grid(
            row=6,
            column=0,
            columnspan=2,
            padx=6,
            pady=(6, 10),
            sticky="ew"
        )

        # Cria um rótulo contendo uma mensagem de orientação
        # para o usuário sobre o formato correto das datas.
        #
        # text:
        #     Texto que será exibido na tela.
        #
        # foreground="#2C302E":
        #     Define a cor do texto utilizando um código hexadecimal.
        #     Essa configuração é apenas visual e não altera
        #     o funcionamento do sistema.

        ttk.Label(
            frameFormulario,
            text="Obs: Use o formato de dd/mm/aaaa.",
            foreground="#2C302E"
        ).grid(

            # O rótulo será exibido na oitava linha da grade.
            row=7,

            # Inicia na primeira coluna da grade.
            column=0,

            # Faz o componente ocupar duas colunas da grade.
            # Como o formulário possui os componentes distribuídos
            # entre as colunas 0 e 1, essa configuração permite
            # que a mensagem fique centralizada e utilize toda
            # a largura disponível.
            columnspan=2,

            # Espaçamento horizontal externo.
            padx=6,

            # Espaçamento vertical externo.
            #
            # 0 pixels acima e 10 pixels abaixo da mensagem.
            pady=(0, 10)
        )

    # Recebe uma data digitada pelo usuário no formato
    # brasileiro (DD/MM/AAAA) e converte esse texto
    # para um objeto do tipo date, permitindo que a
    # aplicação realize operações e validações com a data.
    #
    # Caso o campo esteja vazio, retorna None.
    # Caso a data informada seja inválida, exibe uma
    # mensagem de aviso ao usuário.
    def converterTextoParaData(self, textoData: str) -> date | None:

        # Remove espaços em branco e garante que o valor
        # seja uma string válida mesmo que None seja recebido.
        textoData = (textoData or "").strip()

        # Verifica se o usuário não informou nenhuma data.
        if not textoData:
            return None

        try:
            # Converte o texto para um objeto date utilizando
            # o padrão brasileiro DD/MM/AAAA.
            return datetime.strptime(
                textoData,
                "%d/%m/%Y"
            ).date()

        except ValueError:
            # Executado quando a data possui formato inválido
            # ou representa uma data inexistente.
            messagebox.showwarning(
                "Data inválida",
                f"Informe a data no formato {formBR}: {textoData}"
            )

    # Define um método estático. Esse tipo de método é
    # utilizado quando a operação não depende dos dados
    # armazenados no objeto, servindo apenas para executar
    # uma funcionalidade específica da classe.
    @staticmethod
    def formatarBR(d: date) -> str:
        # O método strftime() converte um objeto date para texto.
        # Neste caso, a data será formatada utilizando o padrão
        # brasileiro definido na constante formBR, normalmente
        # representado por DD/MM/AAAA.
        #
        # Exemplo:
        # date(2026, 6, 18) -> "18/06/2026"
        return d.strftime(formBR)

    def atualizarTabelaEvento(self):

        # Obtém as datas informadas nos campos da tela
        # e converte os textos para objetos do tipo date.
        dataInicio = self.converterTextoParaData(self.varDataIni.get())
        dataFinal = self.converterTextoParaData(self.varDataFim.get())

        # Obtém a descrição informada pelo usuário,
        # removendo espaços extras no início e no fim.
        # Caso o campo esteja vazio, atribui None.
        textoDescricao = self.varDesc.get().strip() or None

        # Verifica se ambas as datas foram informadas
        # e se a data final é anterior à data inicial.
        # Nesse caso, exibe uma mensagem de aviso e
        # interrompe a execução do método.
        if dataInicio and dataFinal and dataFinal < dataInicio:
            messagebox.showwarning(
                "Intervalo de datas inválido",
                "A data final não pode ser menor que a data de início."
            )
            return

        # Solicita ao repositório a busca dos eventos cadastrados
        # no banco de dados utilizando os filtros informados pelo usuário.
        # O resultado será uma lista contendo apenas os registros
        # que atendem aos critérios de pesquisa definidos.
        linhas = self.repo.listar(
            dataIni=dataInicio,
            dataFim=dataFinal,
            textoDesc=textoDescricao
        )

        # Percorre todas as linhas atualmente exibidas na Treeview
        # e as remove da tabela. Essa limpeza é necessária para
        # evitar que os registros antigos permaneçam na tela ou
        # sejam duplicados após uma nova consulta.
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Percorre a lista de eventos retornada pelo repositório
        # e adiciona cada registro na Treeview para exibição ao usuário.
        for evento in linhas:
            # Insere uma nova linha na tabela contendo:
            # - O ID do evento;
            # - A data formatada no padrão brasileiro (dd/mm/aaaa);
            # - A descrição do evento.
            self.tree.insert(
                '',
                tk.END,
                values=(
                    evento.id,
                    self.formatarBR(evento.dataEvento),
                    evento.descricao
                )
            )
        # Limpa a variável que armazena o identificador do evento
        # selecionado.
        self.varidSelecionado = None

    def limpaFiltro(self):

        # Remove os valores informados nos campos
        # de data inicial, data final e descrição.
        self.varDataIni.set("")
        self.varDataFim.set("")
        self.varDesc.set("")

        # Recarrega a tabela de eventos sem aplicar
        # nenhum critério de pesquisa, exibindo todos
        # os registros disponíveis.
        self.atualizarTabelaEvento()

    # Obtém o evento selecionado na tabela e transfere
    # suas informações para os campos do formulário.
    # Dessa forma, o usuário pode visualizar, alterar
    # ou excluir os dados do registro escolhido.
    def capturaSelecao(self, _e=None):

        # Obtém a linha atualmente selecionada na Treeview.
        # O método selection() retorna o identificador interno
        # da linha que foi clicada pelo usuário.
        selecionado = self.tree.selection()

        # Caso nenhuma linha esteja selecionada, não existe
        # informação para carregar no formulário, então a
        # execução do método é encerrada.
        if not selecionado:
            return

        # Recupera os dados armazenados na linha selecionada.
        # O resultado será uma sequência contendo os valores
        # exibidos nas colunas da tabela, como ID, data e descrição.
        valores = self.tree.item(selecionado[0], "values")

        # Garante que a linha selecionada realmente possui dados.
        # Essa verificação evita erros caso a linha esteja vazia
        # ou ocorra algum problema ao recuperar as informações.
        if not valores:
            return

        # Obtém o ID do evento e o converte para inteiro.
        # Esse valor é armazenado para que o sistema saiba
        # exatamente qual registro deverá ser alterado ou
        # excluído quando o usuário clicar nos botões.
        self.idSelecionado = int(valores[0])

        # Copia a data do evento selecionado para o campo
        # de data do formulário, permitindo sua visualização
        # ou edição pelo usuário.
        self.varData.set(valores[1])

        # Copia a descrição do evento selecionado para o
        # campo de descrição do formulário.
        self.varDesc.set(valores[2])

    # Verifica se os dados obrigatórios do formulário
    # foram preenchidos corretamente antes de realizar
    # operações de cadastro ou atualização.
    #
    # Retorna uma tupla contendo:
    # - True e a data convertida, quando a validação
    #   for concluída com sucesso;
    # - False e None, quando existir algum erro nos
    #   dados informados pelo usuário.
    def validaFormulario(self) -> tuple[bool, date | None]:

        # Obtém o texto informado no campo de descrição e
        # remove possíveis espaços em branco digitados
        # no início ou no final do conteúdo.
        descricao = self.varDesc.get().strip()

        # Verifica se a descrição foi preenchida, pois
        # esse campo é obrigatório para identificar o evento.
        if not descricao:
           # Exibe uma mensagem informando ao usuário que
           # a descrição do evento deve ser preenchida.
           messagebox.showwarning("Atenção!", "Informe a descrição do evento.")

           # Interrompe a validação indicando que os dados
           # informados não atendem aos requisitos necessários.
           return False, None

        # Converte a data digitada pelo usuário para um
        # objeto do tipo date, permitindo sua validação
        # e utilização em operações do sistema.
        data = self.converterTextoParaData(self.varData.get())

        # Verifica se a data informada é válida e se a
        # conversão para o tipo date foi realizada com sucesso.
        if data is None:
            # Interrompe a validação devido à existência de
            # erros nos dados informados pelo usuário.
            return False, None

        # Retorna a confirmação de que os dados foram
        # validados com sucesso juntamente com a data convertida.
        return True, data

    def cadastraEvento(self):

        # Valida os dados informados no formulário e
        # obtém a data convertida para o tipo date.
        ok, data = self.validaFormulario()

        # Interrompe o cadastro caso existam erros nos
        # dados informados pelo usuário.
        if not ok:
            return

        # Tenta realizar o cadastro do evento no banco de dados.
        try:
            # Solicita ao repositório o cadastro do evento no banco
            # de dados utilizando a descrição e a data informadas.
            # Após a inserção, o método retorna o ID gerado para o
            # novo registro, que é armazenado na variável novoId.
            novoId = self.repo.inserir(self.varDesc.get().strip(), data)

            # Apresenta uma mensagem de confirmação ao usuário,
            # informando que o evento foi cadastrado com sucesso
            # e exibindo o ID gerado para o novo registro.
            messagebox.showinfo("Sucesso!",
                                f"Evento {novoId} inserido com sucesso!")

            # Atualiza a tabela de eventos para exibir
            # o registro recém-cadastrado.
            self.atualizarTabelaEvento()
            # Limpa os campos do formulário após a
            # conclusão do cadastro.
            self.limpaFormulario()

        # Captura possíveis erros ocorridos durante
        # o processo de cadastro do evento.
        except Exception as e:
            # Exibe ao usuário a descrição do erro
            # ocorrido durante o cadastro.
            messagebox.showerror("Erro ao cadastrar evento.", str(e))

    def alteraEvento(self):

        # Verifica se existe um evento selecionado,
        # pois somente registros selecionados podem ser alterados.
        if self.idSelecionado is None:
            # Informa ao usuário que é necessário selecionar
            # um evento antes de realizar a alteração.
            messagebox.showwarning("Atenção!" ,
                                   "Selecione um evento para alterar.")

            # Interrompe a operação por não existir um registro selecionado.
            return

        # Valida os dados informados no formulário e
        # obtém a data convertida para o tipo date.
        ok, data = self.validaFormulario()

        # Interrompe a alteração caso os dados informados sejam inválidos.
        if not ok:
            return

        # Tenta executar a atualização do evento no banco de dados.
        try:
            # Atualiza no banco de dados o evento selecionado, utilizando os novos
            # valores informados no formulário.
            self.repo.atualizar(self.idSelecionado, self.varDesc.get().strip(), data)

            # Informa ao usuário que a atualização foi realizada com sucesso.
            messagebox.showinfo("Sucesso!",
                                f"Evento {self.idSelecionado} atualizado com sucesso!")

            # Atualiza a tabela para exibir os dados mais recentes do evento alterado.
            self.atualizarTabelaEvento()

            # Limpa os campos do formulário após a conclusão da atualização.
            self.limpaFormulario()



        # Captura possíveis erros ocorridos durante o processo de atualização do evento.
        except Exception as e:
            # Exibe ao usuário informações sobre o erro ocorrido
            # durante a atualização do registro.
            messagebox.showerror("Erro ao atualizar!" , str(e))

    # Realiza a exclusão do evento selecionado.
    def excluiEvento(self):

        # Verifica se existe um evento selecionado na tabela.
        # Caso nenhum registro tenha sido escolhido pelo usuário,
        # não é possível saber qual evento deve ser excluído.
        if self.idSelecionado is None:
            # Exibe uma mensagem solicitando que o usuário
            # selecione um evento antes de continuar.
            messagebox.showwarning(
                "Atenção!",
                "Selecione um evento para excluir."
            )

            # Encerra a execução do método.
            return

        # Solicita uma confirmação antes de remover o evento.
        # O método askyesno() retorna:
        # True  -> quando o usuário clica em "Sim"
        # False -> quando o usuário clica em "Não"
        #
        # O operador "not" inverte o resultado.
        # Portanto, se o usuário NÃO confirmar a exclusão,
        # a operação é cancelada.
        if not messagebox.askyesno(
                "Confirmação",
                f"Excluir evento (ID: {self.idSelecionado})?"
        ):
            return

        try:

            # Solicita ao repositório a remoção do evento
            # correspondente ao ID selecionado.
            self.repo.excluir(self.idSelecionado)

            # Informa ao usuário que a exclusão foi realizada
            # com sucesso.
            messagebox.showinfo(
                "Sucesso!",
                f"Evento {self.idSelecionado} excluído com sucesso!"
            )

            # Atualiza a tabela para remover da visualização
            # o evento que acabou de ser excluído.
            self.atualizarTabelaEvento()

            # Limpa os campos do formulário e remove a
            # referência ao evento anteriormente selecionado.
            self.limpaFormulario()

        except Exception as e:

            # Captura qualquer erro ocorrido durante o
            # processo de exclusão e exibe a mensagem
            # correspondente ao usuário.
            messagebox.showerror(
                "Erro ao excluir evento!",
                str(e)
            )

    # Limpa todos os campos do formulário e remove a referência ao
    # evento atualmente selecionado, deixando a tela preparada
    # para uma nova operação.
    def limpaFormulario(self):

        # Remove o ID do evento selecionado.
        # Isso indica que nenhum registro está
        # atualmente associado ao formulário.
        self.idSelecionado = None

        # Limpa o campo de descrição do evento.
        self.varDesc.set("")

        # Limpa o campo de data final.
        self.varDataFim.set("")

        # Limpa o campo de data do evento.
        self.varData.set("")



# Verifica se este arquivo está sendo executado diretamente.
#
# A variável especial __name__ recebe o valor "__main__"
# quando o arquivo é executado pelo Python.
#
# Caso este arquivo seja importado em outro módulo,
# o código dentro deste bloco não será executado.
if __name__ == '__main__':
    # Cria uma instância da classe principal da aplicação.
    #
    # Neste momento o método construtor (__init__) é executado,
    # realizando toda a configuração inicial da interface gráfica.
    app = AppFiltroEntreDatas()

    # Inicia o loop principal do Tkinter.
    #
    # O método mainloop() mantém a janela aberta e processa
    # continuamente os eventos da interface, como:
    # - Cliques do mouse
    # - Digitação do teclado
    # - Seleção de componentes
    # - Atualizações da tela
    #
    # Sem essa instrução a janela seria criada e encerrada
    # imediatamente após a execução do programa.
    app.mainloop()
