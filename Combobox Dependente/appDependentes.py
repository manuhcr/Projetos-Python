# 1. Importo o Tkinter, que é a caixa de ferramentas usada para construir a interface gráfica.
# É ele quem cria a janela, os botões, as tabelas e os campos que o usuário vê na tela.
import tkinter as tk

# 2. Importo componentes auxiliares do Tkinter:
# - messagebox: serve para conversar com o usuário através de mensagens.
# - ttk: fornece versões mais bonitas e modernas dos componentes visuais.
from tkinter import messagebox, ttk

# 3. Importo o repositório de dados.
# Ele funciona como uma ponte entre a interface e o banco de dados,
# permitindo buscar, cadastrar, alterar e excluir informações.
from repositorio import repoLocal


# Classe principal da aplicação.
# Herdamos de tk.Tk para transformar a própria classe em uma janela Tkinter.
class AppCombosDependentes(tk.Tk):

    def __init__(self):

        # Inicializa a janela principal do Tkinter.
        super().__init__()

        # Cria uma instância do repositório, responsável por conversar com o banco de dados.
        self.repo = repoLocal()

        # Define o título exibido na barra superior da janela.
        self.title("Combobox Dependentes - Pais / Estado / Cidade (Mysql + Pymysql)")

        # Centraliza a janela na tela com largura 1000 e altura 600.
        self.centerTable(1000, 600)

        # Define o tamanho mínimo que o usuário pode redimensionar a janela.
        self.minsize(900, 520)

        # Variáveis ligadas aos filtros da parte superior da tela.
        # Elas armazenam o país, estado e cidade selecionados nas Comboboxes.
        self.varCountryFilter = tk.StringVar()
        self.varStateFilter = tk.StringVar()
        self.varCityFilter = tk.StringVar()

        # Variáveis ligadas ao formulário de cadastro/edição.
        # Elas armazenam os valores digitados pelo usuário.
        self.varCountryForm = tk.StringVar()
        self.varStateForm = tk.StringVar()
        self.varCityForm = tk.StringVar()

        # Guarda o ID da linha atualmente selecionada na tabela.
        # Se for None, significa que nenhuma linha está selecionada.
        self.selectedId: int | None = None

        # Cria e organiza todos os componentes visuais da interface.
        self.buildLayout()

        # Carrega inicialmente os países nas Comboboxes de filtro.
        self.loadInitialCountry()

        # Carrega os registros do banco e preenche a tabela.
        self.updateTable()

    def centerTable(self, width: int, height: int):

        # 1. Atualiza todas as informações pendentes da janela.
        # Isso garante que o Tkinter já saiba o tamanho da tela corretamente.
        self.update_idletasks()

        # 2. Descobre a largura total da tela do usuário.
        sx = self.winfo_screenwidth()

        # 3. Descobre a altura total da tela do usuário.
        sy = self.winfo_screenheight()

        # 4. Calcula a posição horizontal (X) para deixar a janela centralizada.
        # Pegamos o centro da tela e subtraímos metade da largura da janela.
        x = (sx // 2) - (width // 2)

        # 5. Calcula a posição vertical (Y) para deixar a janela centralizada.
        # Pegamos o centro da tela e subtraímos metade da altura da janela.
        y = (sy // 2) - (height // 2)

        # 6. Define o tamanho e a posição final da janela.
        # Formato: largura x altura + posiçãoX + posiçãoY
        self.geometry(f"{width}x{height}+{x}+{y}")

    def buildLayout(self):

        # 1. ÁREA DE FILTROS
        # Esta caixa agrupa as Comboboxes responsáveis pelos filtros da tabela.
        # Como elas são dependentes, a escolha do País influencia os Estados,
        # e a escolha do Estado influencia as Cidades.
        frameFilters = ttk.LabelFrame(self, text="Filtros (Comboboxes Dependentes)")
        frameFilters.pack(fill="x", padx=10, pady=10)

        # 2. CAMPO PAÍS
        # Exibe o texto "País" e a Combobox onde o usuário escolhe um país.
        # Quando um país é selecionado, o método chosenCountry() é executado
        # para carregar os estados correspondentes.
        ttk.Label(frameFilters, text="País:").grid(row=0, column=0, padx=6, pady=6, sticky="w")

        self.comboCountry = ttk.Combobox(frameFilters, textvariable=self.varCountryFilter, state="readonly", width=28)
        self.comboCountry.grid(row=0, column=1, padx=6, pady=6, sticky="w")
        self.comboCountry.bind("<<ComboboxSelected>>", self.chosenCountry)

        # 3. CAMPO ESTADO
        # Exibe o texto "Estado" e a Combobox dos estados.
        # Ela será preenchida de acordo com o país escolhido anteriormente.
        # Ao selecionar um estado, o método chosenState() será executado.
        ttk.Label(frameFilters, text="Estado:").grid(row=0, column=2, padx=6, pady=6, sticky="w")

        self.comboState = ttk.Combobox(frameFilters, textvariable=self.varStateFilter, state="readonly", width=28)
        self.comboState.grid(row=0, column=3, padx=6, pady=6, sticky="w")
        self.comboState.bind("<<ComboboxSelected>>", self.chosenState)

        # 4. CAMPO CIDADE
        # Exibe o texto "Cidade" e a Combobox das cidades.
        # Ela será preenchida conforme o estado selecionado.
        # Quando uma cidade é escolhida, a tabela é atualizada.
        ttk.Label(frameFilters, text="Cidade:").grid(row=0, column=4, padx=6, pady=6, sticky="w")

        self.comboCity = ttk.Combobox(frameFilters, textvariable=self.varCityFilter, state="readonly", width=28)
        self.comboCity.grid(row=0, column=5, padx=6, pady=6, sticky="w")
        self.comboCity.bind("<<ComboboxSelected>>", lambda e: self.updateTable())

        # 5. BOTÃO LIMPAR FILTROS
        # Remove todos os filtros aplicados e recarrega os dados.
        btnClean = ttk.Button(frameFilters, text="Limpar filtros", command=self.cleanFilters)
        btnClean.grid(row=0, column=6, padx=10, pady=6)

        # 6. ÁREA CENTRAL DA TELA
        # Funciona como um contêiner para a tabela (esquerda)
        # e para o formulário CRUD (direita).
        centerFrame = ttk.Frame(self)
        centerFrame.pack(fill="both", expand=True, padx=10, pady=5)

        # 7. TABELA DE REGISTROS
        # Exibe os locais cadastrados no banco de dados.
        # Os registros mostrados respeitam os filtros selecionados.
        frameTable = ttk.LabelFrame(centerFrame, text="Locais (conforme filtros)")
        frameTable.pack(side="left", fill="both", expand=True, padx=(8, 8))

        # 8. DEFINIÇÃO DAS COLUNAS DA TABELA
        # Cada coluna representa uma informação armazenada no banco.
        columns = ("id", "pais", "estado", "cidade")

        # 9. TREEVIEW
        # Componente visual utilizado para exibir os registros em formato de tabela.
        self.tree = ttk.Treeview(frameTable, columns=columns, show="headings", height=18)

        # 10. CABEÇALHOS DA TABELA
        # Define os nomes exibidos no topo de cada coluna.
        self.tree.heading("id", text="Id")
        self.tree.heading("pais", text="País")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("cidade", text="Cidade")

        # 11. CONFIGURAÇÃO DAS COLUNAS
        # Define larguras e alinhamentos da tabela.
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("pais", width=180)
        self.tree.column("estado", width=180)
        self.tree.column("cidade", width=180)

        # 12. EXIBE A TABELA NA TELA
        self.tree.pack(fill="both", expand=True)

        # 13. EVENTO DE SELEÇÃO
        # Quando uma linha é selecionada, os dados são carregados
        # automaticamente no formulário para edição ou exclusão.
        self.tree.bind("<<TreeviewSelect>>", self.captureSelection)

        # 14. BARRA DE ROLAGEM
        # Permite navegar pela tabela quando houver muitos registros.
        vsb = ttk.Scrollbar(frameTable, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")

        # 15. FORMULÁRIO CRUD
        # Área responsável por cadastrar, editar e excluir registros.
        frameForm = ttk.LabelFrame(centerFrame, text="Cadastrar / Editar / Excluir")
        frameForm.pack(side="right", fill="y", padx=(8, 0))

        # 16. CAMPO PAÍS DO FORMULÁRIO
        # Utilizado para informar ou alterar o país do registro.
        ttk.Label(frameForm, text="País").grid(row=0, column=0, padx=6, pady=(10, 6), sticky="w")

        self.enterCountry = ttk.Entry(frameForm, textvariable=self.varCountryForm, width=28)
        self.enterCountry.grid(row=0, column=1, padx=6, pady=(10, 6), sticky="w")

        # 17. CAMPO ESTADO DO FORMULÁRIO
        ttk.Label(frameForm, text="Estado").grid(row=1, column=0, padx=6, pady=6, sticky="w")

        self.enterState = ttk.Entry(frameForm, textvariable=self.varStateForm, width=28)
        self.enterState.grid(row=1, column=1, padx=6, pady=6, sticky="w")

        # 18. CAMPO CIDADE DO FORMULÁRIO
        ttk.Label(frameForm, text="Cidade").grid(row=2, column=0, padx=6, pady=6, sticky="w")

        self.enterCity = ttk.Entry(frameForm, textvariable=self.varCityForm, width=28)
        self.enterCity.grid(row=2, column=1, padx=6, pady=6, sticky="w")

        # 19. SEPARADOR VISUAL
        # Apenas organiza visualmente o formulário.
        ttk.Separator(frameForm).grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=6,
            pady=10
        )

        # 20. BOTÃO CADASTRAR
        # Insere um novo registro no banco de dados.
        btnCadastrate = ttk.Button(frameForm, text="Cadastrar", command=self.cadastrate)
        btnCadastrate.grid(row=4, column=0, padx=6, pady=6, sticky="ew", columnspan=2)

        # 21. BOTÃO ALTERAR
        # Atualiza os dados do registro selecionado.
        btnUpdate = ttk.Button(frameForm, text="Alterar (Linha selecionada)", command=self.update)
        btnUpdate.grid(row=5, column=0, padx=6, pady=6, sticky="ew", columnspan=2)

        # 22. BOTÃO EXCLUIR
        # Remove o registro atualmente selecionado.
        btnDelete = ttk.Button(frameForm, text="Excluir (Linha selecionada)", command=self.delete)
        btnDelete.grid(row=6, column=0, padx=6, pady=6, sticky="ew", columnspan=2)

        # 23. BOTÃO LIMPAR FORMULÁRIO
        # Limpa os campos e remove a seleção atual.
        btnCleanForm = ttk.Button(frameForm, text="Limpar Form", command=self.cleanForm)
        btnCleanForm.grid(row=7, column=0, padx=6, pady=(6, 10), sticky="ew", columnspan=2)

        # 24. MENSAGEM DE AJUDA
        # Orienta o usuário sobre como utilizar a tabela junto do formulário.
        lblInfo = ttk.Label(frameForm, text="Dica: Selecione uma linha na tabela para carregar o\n"
                                            "Formulário e então Alterar/Excluir", foreground="#333")
        lblInfo.grid(row=9, column=0, columnspan=2, padx=6, pady=(0, 10))

    def loadInitialCountry(self):

        # 1. Pede ao repositório a lista de todos os países cadastrados no banco.
        countries = self.repo.getCountry()

        # 2. Preenche a Combobox de países.
        # Adicionamos "Todos" no início para permitir consultas sem filtro.
        self.comboCountry["values"] = ["Todos"] + countries

        # 3. Define "(Todos)" como valor inicialmente exibido na Combobox.
        self.comboCountry.set("(Todos)")

        # 4. Como nenhum país foi escolhido ainda,
        # a Combobox de estados começa apenas com a opção "Todos".
        self.comboState["values"] = ["Todos"]

        # 5. Exibe "(Todos)" como valor padrão da Combobox de estados.
        self.comboState.set("(Todos)")

        # 6. Como nenhum estado foi escolhido ainda,
        # a Combobox de cidades também começa apenas com a opção "Todos".
        self.comboCity["values"] = ["Todos"]

        # 7. Exibe "(Todos)" como valor padrão da Combobox de cidades.
        self.comboCity.set("(Todos)")

    def chosenCountry(self, _event: None):

        # 1. Descobre qual país o usuário acabou de selecionar na Combobox.
        country = self.varCountryFilter.get()

        # 2. Se o usuário escolheu "(Todos)",
        # significa que ele não quer filtrar por país.
        if country == "(Todos)":
            # 3. Reinicia a Combobox de estados,
            # deixando apenas a opção "(Todos)".
            self.comboState["values"] = ["Todos"]
            self.comboState.set("(Todos)")

            # 4. Reinicia a Combobox de cidades,
            # deixando apenas a opção "(Todos)".
            self.comboCity["values"] = ["Todos"]
            self.comboCity.set("(Todos)")

            # 5. Atualiza a tabela para mostrar todos os registros.
            self.updateTable()

            # 6. Encerra a função, pois não há mais nada para fazer.
            return

        # 7. Se um país específico foi escolhido,
        # pedimos ao banco todos os estados daquele país.
        states = self.repo.getState(country)

        # 8. Preenche a Combobox de estados.
        # Adicionamos "(Todos)" para permitir visualizar
        # todos os estados daquele país.
        self.comboState["values"] = ["(Todos)"] + states

        # 9. Define "(Todos)" como seleção inicial.
        self.comboState.set("(Todos)")

        # 10. Como o estado ainda não foi escolhido,
        # limpamos a Combobox de cidades.
        self.comboCity["values"] = ["(Todos)"]

        # 11. Define "(Todos)" como valor padrão da cidade.
        self.comboCity.set("(Todos)")

        # 12. Atualiza a tabela aplicando o filtro do país escolhido.
        self.updateTable()

    def chosenState(self, _event: None):

        # 1. Descobre qual país e qual estado o usuário selecionou.
        # Vamos precisar dessas informações para buscar as cidades corretas.
        country = self.varCountryFilter.get()
        state = self.varStateFilter.get()

        # 2. Verifica se o usuário escolheu "(Todos)"
        # ou se nenhum país válido foi selecionado.
        if state == "(Todos)" or not country or country == "(Todos)":
            # 3. Como não existe um estado específico selecionado,
            # limpamos a Combobox de cidades.
            self.comboCity["values"] = ["Todos"]

            # 4. Definimos "(Todos)" como valor exibido.
            self.comboCity.set("(Todos)")

            # 5. Atualizamos a tabela para mostrar os registros
            # de acordo com os filtros atuais.
            self.updateTable()

            # 6. Encerramos a função, pois não há cidades específicas para carregar.
            return

        # 7. Se existe um país e um estado válidos,
        # pedimos ao banco todas as cidades desse estado.
        city = self.repo.getCity(country, state)

        # 8. Preenchemos a Combobox de cidades.
        # Adicionamos "(Todos)" para permitir visualizar
        # todas as cidades daquele estado.
        self.comboCity["values"] = ["(Todos)"] + city

        # 9. Define "(Todos)" como opção inicial.
        self.comboCity.set("(Todos)")

        # 10. Atualiza a tabela aplicando os filtros atuais.
        self.updateTable()

    def updateTable(self):

        # 1. Lê os valores atualmente selecionados nas Comboboxes de filtro.
        # Esses valores serão usados para decidir quais registros mostrar.
        country = self.varCountryFilter.get()
        state = self.varStateFilter.get()
        city = self.varCityFilter.get()

        # 2. Converte "(Todos)" em None.
        # O repositório entende None como "não aplicar filtro".
        #
        # Exemplo:
        # País = "(Todos)" → None
        # País = "Brasil"   → "Brasil"
        countryF = None if not country or country == "(Todos)" else country
        stateF = None if not state or state == "(Todos)" else state
        cityF = None if not city or city == "(Todos)" else city

        # 3. Pede ao banco de dados todos os registros
        # que atendem aos filtros selecionados.
        #
        # Se todos forem None, traz tudo.
        # Se houver filtros, traz apenas os registros correspondentes.
        lines = self.repo.list(
            country=countryF,
            state=stateF,
            city=cityF
        )

        # 4. Antes de colocar os novos registros na tabela,
        # removemos todos os registros antigos.
        #
        # get_children() devolve todas as linhas atualmente exibidas.
        for item in self.tree.get_children():
            # Remove cada linha encontrada.
            self.tree.delete(item)

        # 5. Agora inserimos os registros atualizados.
        #
        # Cada objeto Local retornado pelo banco
        # vira uma linha dentro da Treeview.
        for loc in lines:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    loc.id,
                    loc.country,
                    loc.state,
                    loc.city
                )
            )

        # 6. Como a tabela foi recriada,
        # removemos qualquer seleção anterior.
        self.selectedId = None

    def captureSelection(self, _event: None):

        # 1. Descobre qual linha da tabela está selecionada.
        # selection() devolve uma lista com os itens selecionados.
        sel = self.tree.selection()

        # 2. Se nenhuma linha estiver selecionada,
        # não há nada para carregar no formulário.
        if not sel:
            return

        # 3. Obtém os valores armazenados na primeira linha selecionada.
        # O resultado será algo parecido com:
        # ('1', 'Brasil', 'São Paulo', 'Campinas')
        values = self.tree.item(sel[0], "values")

        # 4. Se por algum motivo a linha não possuir valores,
        # encerramos a função.
        if not values:
            return

        # 5. Guarda o ID do registro selecionado.
        # Esse ID será utilizado posteriormente
        # nas operações de Alterar e Excluir.
        self.selectedId = int(values[0])

        # 6. Carrega os dados da linha selecionada
        # para dentro do formulário.
        self.varCountryForm.set(values[1])
        self.varStateForm.set(values[2])
        self.varCityForm.set(values[3])

    def cleanFilters(self):

        # 1. Recarrega os filtros para o estado inicial.
        # País recebe todos os países disponíveis,
        # enquanto Estado e Cidade voltam para "(Todos)".
        self.loadInitialCountry()

        # 2. Atualiza a tabela removendo qualquer filtro aplicado.
        self.updateTable()

    def cleanForm(self):

        # 1. Remove qualquer registro selecionado.
        # Isso faz o sistema voltar ao modo de cadastro.
        self.selectedId = None

        # 2. Limpa o campo País do formulário.
        self.varCountryForm.set("")

        # 3. Limpa o campo Estado do formulário.
        self.varStateForm.set("")

        # 4. Limpa o campo Cidade do formulário.
        self.varCityForm.set("")

    def validateForm(self) -> bool:

        # 1. Verifica se o campo País está vazio.
        # strip() remove espaços em branco do começo e do fim.
        # Assim, "   " também será considerado vazio.
        if not self.varCountryForm.get().strip():
            # 2. Exibe uma mensagem avisando o usuário
            # que o campo País precisa ser preenchido.
            messagebox.showwarning("Atenção", "Informe o País.")

            # 3. Como a validação falhou,
            # retornamos False.
            return False

        # 4. Verifica se o campo Estado está vazio.
        if not self.varStateForm.get().strip():
            # 5. Exibe um aviso ao usuário.
            messagebox.showwarning("Atenção", "Informe o Estado.")

            # 6. Informa que a validação falhou.
            return False

        # 7. Verifica se o campo Cidade está vazio.
        if not self.varCityForm.get().strip():
            # 8. Exibe um aviso ao usuário.
            messagebox.showwarning("Atenção", "Informe a Cidade.")

            # 9. Informa que a validação falhou.
            return False

        # 10. Se todas as verificações passaram,
        # significa que o formulário está válido.
        return True

    def cadastrate(self):

        # 1. Antes de tentar cadastrar,
        # verificamos se todos os campos obrigatórios foram preenchidos.
        if not self.validateForm():
            # 2. Se a validação falhar,
            # interrompemos a execução da função.
            return

        try:

            # 3. Envia os dados do formulário para o repositório.
            # O repositório será responsável por inserir o registro no banco.
            #
            # strip() remove espaços extras no início e no final do texto.
            newId = self.repo.insert(
                self.varCountryForm.get().strip(),
                self.varStateForm.get().strip(),
                self.varCityForm.get().strip(),
            )

            # 4. Se a inserção ocorreu com sucesso,
            # exibimos uma mensagem informando o ID gerado pelo banco.
            messagebox.showinfo(
                "Sucesso!",
                f"Registro inserido: id {newId}."
            )

            # 5. Atualiza a tabela para que o novo registro apareça imediatamente.
            self.updateTable()

            # 6. Recarrega os filtros.
            # Isso garante que novos países, estados ou cidades
            # apareçam nas Comboboxes caso tenham sido cadastrados.
            self.loadInitialCountry()

        except Exception as err:

            # 7. Se ocorrer qualquer erro durante a inserção,
            # mostramos a mensagem retornada pela exceção.
            messagebox.showerror(
                "Erro ao inserir",
                str(err)
            )

    def update(self):

        # 1. Antes de atualizar qualquer coisa,
        # verificamos se existe uma linha selecionada na tabela.
        #
        # selectedId guarda o ID do registro selecionado.
        if self.selectedId is None:
            # 2. Se nenhuma linha foi selecionada,
            # mostramos um aviso ao usuário.
            messagebox.showwarning(
                "Atenção!",
                "Selecione uma linha para atualizar."
            )

            # 3. Encerramos a função,
            # pois não sabemos qual registro alterar.
            return

        # 4. Depois verificamos se o formulário está preenchido corretamente.
        if not self.validateForm():
            # 5. Se a validação falhar,
            # interrompemos a atualização.
            return

        try:

            # 6. Envia os dados atualizados para o repositório.
            #
            # O primeiro parâmetro é o ID do registro que será alterado.
            # Os demais são os novos valores do formulário.
            self.repo.update(
                self.selectedId,
                self.varCountryForm.get().strip(),
                self.varStateForm.get().strip(),
                self.varCityForm.get().strip(),
            )

            # 7. Informa ao usuário que a atualização foi concluída.
            messagebox.showinfo(
                "Sucesso!",
                f"Registro ID: {self.selectedId} atualizado!"
            )

            # 8. Atualiza a tabela para exibir os dados novos.
            self.updateTable()

            # 9. Atualiza as Comboboxes de filtro.
            # Isso é importante caso algum país, estado ou cidade
            # tenha sido alterado.
            self.loadInitialCountry()

        except Exception as err:

            # 10. Se ocorrer qualquer erro,
            # mostramos a mensagem retornada pela exceção.
            messagebox.showerror(
                "Erro ao atualizar.",
                str(err)
            )

    def delete(self):

        # 1. Antes de excluir, verificamos se existe
        # algum registro selecionado na tabela.
        if self.selectedId is None:
            # 2. Se não existir seleção,
            # mostramos um aviso ao usuário.
            messagebox.showwarning(
                "Atenção!",
                "Selecione uma linha na tabela para deletar."
            )

            # 3. Encerramos a função,
            # pois não há registro para excluir.
            return

        # 4. Exibe uma caixa de confirmação.
        # askyesno() retorna:
        # True  -> Usuário clicou em "Sim"
        # False -> Usuário clicou em "Não"
        if messagebox.askyesno(
                "Confirmação",
                f"Deseja realmente deletar o ID {self.selectedId}?"
        ):

            try:

                # 5. Solicita ao repositório a exclusão
                # do registro selecionado.
                self.repo.delete(self.selectedId)

                # 6. Informa ao usuário que a exclusão foi concluída.
                messagebox.showinfo(
                    "Sucesso",
                    "Registro deletado com sucesso!"
                )

                # 7. Limpa o formulário,
                # removendo os dados do registro excluído.
                self.cleanForm()

                # 8. Atualiza a tabela para remover
                # visualmente o registro apagado.
                self.updateTable()

                # 9. Atualiza os filtros.
                # Isso é importante caso a exclusão tenha removido
                # o único país, estado ou cidade existente.
                self.loadInitialCountry()

            except Exception as err:

                # 10. Se ocorrer algum erro,
                # exibimos a mensagem retornada pela exceção.
                messagebox.showerror(
                    "Erro ao deletar",
                    str(err)
                )

# 1. Este bloco só será executado quando este arquivo
# for iniciado diretamente pelo Python.
#
# Se este arquivo for apenas importado por outro arquivo,
# o código abaixo não será executado.
if __name__ == "__main__":

    # 2. Cria uma instância da janela principal da aplicação.
    # Nesse momento o __init__() da classe é executado,
    # construindo toda a interface gráfica.
    app = AppCombosDependentes()

    # 3. Inicia o loop principal do Tkinter.
    # A partir daqui a janela permanece aberta,
    # aguardando cliques, digitações e outros eventos do usuário.
    app.mainloop()
