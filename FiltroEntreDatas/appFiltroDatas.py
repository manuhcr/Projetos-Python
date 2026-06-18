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
        self.atualizar()

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
        # Cria um LabelFrame para agrupar visualmente os
        # componentes responsáveis pelos filtros de pesquisa.
        #
        # O texto informado será exibido na borda superior
        # do frame, identificando sua finalidade.
        frameFiltro = tk.LabelFrame(
            self,
            text="Filtro entre datas (data inicial / data final / texto na descrição)"
        )

        # Exibe o frame na janela principal.
        #
        # fill="x" faz com que o frame ocupe toda a largura disponível.
        # padx e pady adicionam espaçamento externo.
        frameFiltro.pack(
            fill="x",
            padx=10,
            pady=10
        )

        # Cria o rótulo que identifica o campo
        # onde o usuário informará a data inicial.
        ttk.Label(
            frameFiltro,
            text="Data Inicial"
        ).grid(
            row=0,
            column=0,
            padx=6,
            pady=6,
            sticky="w"
        )

        # Campo utilizado para digitação da data inicial.
        #
        # O valor digitado será armazenado na variável
        # self.varDataIni através do mecanismo textvariable.
        insereDataIni = tk.Entry(
            frameFiltro,
            textvariable=self.varDataIni,
            width=16
        )

        # Posiciona o campo na grade do frame.
        insereDataIni.grid(
            row=0,
            column=1,
            padx=6,
            pady=6,
            sticky="w"
        )

        # Rótulo responsável por identificar o campo
        # de data final.
        ttk.Label(
            frameFiltro,
            text="Data Final"
        ).grid(
            row=0,
            column=2,
            padx=6,
            pady=6
        )

        # Campo utilizado para digitação da data final.
        #
        # O conteúdo digitado será armazenado
        # na variável self.varDataFim.
        insereDataFim = tk.Entry(
            frameFiltro,
            textvariable=self.varDataFim
        )

        insereDataFim.grid(
            row=0,
            column=3,
            padx=6,
            pady=6,
            sticky="w"
        )

        # Rótulo responsável por identificar o campo
        # utilizado para pesquisa textual.
        ttk.Label(
            frameFiltro,
            text="Descrição"
        ).grid(
            row=0,
            column=4,
            padx=6,
            pady=6,
            sticky="w"
        )

        # Campo onde o usuário poderá informar parte
        # da descrição do evento para realizar pesquisas.
        #
        # Exemplo:
        # "Python"
        # "Workshop"
        # "Relatório"
        #
        # O sistema utilizará esse valor para filtrar
        # os registros exibidos na tabela.
        insereDescricaoFiltro = tk.Entry(
            frameFiltro,
            textvariable=self.varTexto
        )

        insereDescricaoFiltro.grid(
            row=0,
            column=5,
            padx=6,
            pady=6,
            sticky="w"
        )

        # Botão responsável por aplicar os filtros
        # preenchidos pelo usuário.
        #
        # Ao ser clicado, executa o método atualizar(),
        # que realiza uma nova consulta ao banco de dados
        # utilizando os critérios informados.
        btnAplicar = ttk.Button(
            frameFiltro,
            text="Aplicar Filtro",
            command=self.atualizar
        )

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
            command=self.limpaFiltro
        )

        btnLimpar.grid(
            row=0,
            column=7,
            padx=6,
            pady=6
        )

        # Cria o frame central da aplicação.
        #
        # Este frame servirá como contêiner para:
        # - Tabela de eventos
        # - Formulário de cadastro
        frameCentro = ttk.Frame(self)

        frameCentro.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        # Cria o frame responsável por exibir os eventos
        # retornados pela consulta.
        frameTabela = ttk.LabelFrame(
            frameCentro,
            text="Eventos (conforme os filtros)"
        )

        frameTabela.pack(
            side="left",
            fill="both",
            padx=(0, 8)
        )

        # Define os identificadores das colunas
        # utilizadas pela Treeview.
        colunas = (
            "id",
            "dataEvento",
            "descricao"
        )

        # Cria a tabela responsável por exibir os eventos.
        #
        # A Treeview funciona como uma grade de dados,
        # semelhante a uma tabela encontrada em sistemas
        # desktop tradicionais.
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

        # Configura largura e alinhamento visual
        # das colunas da tabela.
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("dataEvento", width=120, anchor="center")
        self.tree.column("descricao", width=120, anchor="w")

        # Exibe a tabela dentro do frame.
        self.tree.pack(
            fill="both",
            expand=True
        )

        # Associa o evento de seleção de linha ao método
        # capturaSelecao().
        #
        # Sempre que o usuário selecionar um registro,
        # esse método será executado automaticamente.
        self.tree.bind(
            "<<TreeviewSelect>>",
            self.capturaSelecao
        )

        # Cria uma barra de rolagem vertical.
        #
        # Ela será utilizada quando a quantidade de eventos
        # ultrapassar o espaço visível da tabela.
        bsv = ttk.Scrollbar(
            frameTabela,
            orient="vertical",
            command=self.tree.yview
        )

        # Vincula a barra de rolagem à tabela.
        self.tree.configure(
            yscrollcommand=bsv.set
        )

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

        # Posiciona o formulário no lado direito da tela.
        #
        # side="right" posiciona o componente à direita.
        # fill="y" faz o frame ocupar toda a altura disponível.
        # padx adiciona espaçamento externo.
        frameFormulario.pack(
            side="right",
            fill="y",
            padx=(8, 0)
        )

        # Cria um rótulo para identificar o campo
        # onde será informada a descrição do evento.
        ttk.Label(
            frameFormulario,
            text="Descrição:"
        ).grid(
            row=0,
            column=0,
            padx=6,
            pady=(10, 6)
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

        # Posiciona o campo ao lado do rótulo.
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

        # Posiciona o campo de data no formulário.
        insereData.grid(
            row=1,
            column=1,
            padx=6,
            pady=6,
            sticky="w"
        )

        # Cria uma linha separadora horizontal.
        #
        # Sua função é apenas visual, ajudando a separar
        # os campos de entrada dos botões de ação.
        ttk.Separator(frameFormulario).grid(
            row=2,
            column=0,
            columnspan=2,
            padx=6,
            pady=10,
            sticky="ew"
        )

        # Cria o botão responsável pelo cadastro
        # de novos eventos no banco de dados.
        #
        # Quando clicado, executa o método
        # self.cadastraEvento().
        btnCadastrar = ttk.Button(
            frameFormulario,
            text="Cadastrar Evento",
            command=self.cadastraEvento
        )

        btnCadastrar.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=6,
            pady=6,
            sticky="w"
        )

        # Cria o botão responsável por excluir
        # o evento atualmente selecionado na tabela.
        #
        # Ao clicar no botão, o método
        # self.excluiEvento() será executado.
        #
        # Normalmente o sistema utiliza o ID do evento
        # armazenado em self.varIdSelecionado para localizar
        # o registro correto no banco de dados.
        btnExcluir = ttk.Button(
            frameFormulario,
            text="Excluir (evento selecionado)",
            command=self.excluiEvento
        )

        btnExcluir.grid(
            row=4,
            column=0,
            columnspan=2,
            padx=6,
            pady=6,
            sticky="ew"
        )

        # Cria o botão responsável por alterar
        # os dados do evento selecionado.
        #
        # Os novos valores informados nos campos
        # serão utilizados para atualizar o registro
        # correspondente no banco de dados.
        btnAlterar = ttk.Button(
            frameFormulario,
            text="Alterar (evento selecionado)",
            command=self.alteraEvento
        )

        btnAlterar.grid(
            row=5,
            column=0,
            columnspan=2,
            padx=6,
            pady=6,
            sticky="ew"
        )

        # Cria o botão responsável por limpar
        # todos os campos do formulário.
        #
        # Essa operação não remove dados do banco.
        # Apenas limpa os campos da interface,
        # permitindo um novo preenchimento.
        btnLimparForm = ttk.Button(
            frameFormulario,
            text="Limpar Formulário",
            command=self.limpaFormulario
        )

        btnLimparForm.grid(
            row=6,
            column=0,
            padx=6,
            pady=(6, 10),
            sticky="ew"
        )

        # Exibe uma mensagem de orientação para o usuário.
        #
        # Essa informação indica qual formato deve ser
        # utilizado ao informar datas no sistema.
        #
        # Exemplo válido:
        # 15/06/2026
        #
        # Exemplo inválido:
        # 2026-06-15
        ttk.Label(
            frameFormulario,
            text="Obs: Use o formato de dd/mm/aaaa.",
            foreground="#2C302E"
        ).grid(
            row=7,
            column=0,
            columnspan=2,
            padx=6,
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

    def atualizarEvento(self):

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

        # Consulta os eventos no repositório utilizando
        # os filtros informados pelo usuário.
        linhas = self.repo.listar(
            dataIni=dataInicio,
            dataFinal=dataFinal,
            textoDesc=textoDescricao
        )

        # Remove todos os registros atualmente exibidos
        # na Treeview para evitar duplicações.
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insere os eventos encontrados na Treeview.
        for evento in linhas:
            self.tree.insert(
                '',
                tk.END,
                values=(
                    evento.id,
                    self.formatarBR(evento.dataEvento)
                )
            )

        # Limpa a variável que armazena o identificador do evento selecionado.
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
        self.atualizarEvento()



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
