import tkinter as tk
from tkinter import messagebox
from repositorio import Local

class AppCombosDependentes(tk.Tk):


    def __init__(self):

       super().__init__()

       self.title("Combobox Dependentes - Pais / Estado / Cidade (Mysql + Pymysql)")

       self.centerTable(1000, 600)

       self.minsize(900,520)

       self.varCountryFilter = tk.StringVar()
       self.varStateFilter = tk.StringVar()
       self.varCityFilter = tk.StringVar()

       self.varCountryForm = tk.StringVar()
       self.varStateForm = tk.StringVar()
       self.varCityForm = tk.StringVar()

       self.selectedId: int | None = None

       self.buildLayout()

       self.loadInitialCountry()

       self.updateTable()


    def centerTable(self, width: int, height: int):

        self.update_idletasks()

        sx = self.winfo_screenwidth()
        sy = self.winfo_screenheight()

        x = (sx // 2) - (width // 2)
        y = (sy // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")


    def buildLayout(self):

        frameFilters = ttk.LabelFrame(self, text="Filtros (Comboboxes Dependentes)")
        frameFilters.pack(fill="x", padx=10, pady=10)

        ttk.Label(frameFilters, text = "País:").grid(row=0, column=0, padx=6, pady=6, sticky="w")

        self.comboCountry = ttk.Combobox(frameFilters, textvariable=self.varCountryFilter, state="readonly", width=28)
        self.comboCountry.grid(row=0, column=1, padx=6, pady=6, sticky="w")
        self.comboCountry.bind("<<ComboboxSelected>>", self.onChosenCountry)

        ttk.Label(frameFilters, text = "Estado:").grid(row=0, column=2, padx=6, pady=6, sticky="w")

        self.comboState = ttk.Combobox(frameFilters, textvariable=self.varStateFilter, state="readonly", width=28)
        self.comboState.grid(row=0, column=3, padx=6, pady=6, sticky="w")
        self.comboState.bind("<<ComboboxSelected>>", self.onChosenState)

        ttk.Label(frameFilters, text = "Cidade:").grid(row=0, column=4, padx=6, pady=6, sticky="w")

        self.comboCity = ttk.Combobox(frameFilters, textvariable=self.varCityFilter, state="readonly", width=28)
        self.comboCity.grid(row=0, column=5, padx=6, pady=6, sticky="w")
        self.comboCity.bind("<<ComboboxSelected>>",  lambda e: self.updateTable())

        btnClean = ttk.Button(frameFilters, text="Limpar filtros", command=self.onCleanFilters)
        btnClean.grid(row=0, column=6, padx=10, pady=6)

        centerFrame = ttk.Frame(self)
        centerFrame.pack(fill="both", expand=True, padx=10, pady=5)

        frameTable = ttk.LabelFrame(centerFrame, text="Locais (conforme filtros)")
        frameTable.pack(fill="x", fill="both", expand=True, padx=(8 ,8))

        columns = ("id" , "pais" , "estado" , "cidade")

        self.tree = ttk.Treeview(frameTable, columns=columns, show="headings", height=18)
        self.tree.heading("id", text="Id")
        self.tree.heading("pais", text = "País")
        self.tree.heading("estado", text = "Estado")
        self.tree.heading("cidade", text = "Cidade")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("pais", width=180)
        self.tree.column("estado", width=180)
        self.tree.column("cidade", width=180)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.captureSelection)

        vsb = ttk.Scrollbar(frameTable, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")

        frameForm = ttk.LabelFrame(centerFrame, text="Cadastrar / Editar / Excluir")
        frameForm.pack(side="right", fill="y", padx=(8, 0))
        ttk.Label(frameForm, text = "País").grid(row=0, column=0, padx=6, pady=(10, 6), sticky="w")

        self.enterCountry = ttk.Entry(frameForm, textvariable=self.varCountryForm, width=28)
        self.enterCountry.grid(row=0, column=1, padx=6, pady=(10, 6), sticky="w")

        ttk.Label(frameForm, text = "Estado").grid(row=1, column=0, padx=6, pady=6, sticky="w")

        self.enterState = ttk.Entry(frameForm, textvariable=self.varStateForm, width=28)
        self.enterState.grid(row=1, column=1, padx=6, pady=6, sticky="w")

        ttk.Label(frameForm, text = "Cidade").grid(row=2, column=0, padx=6, pady=6, sticky="w")

        self.enterCity = ttk.Entry(frameForm, textvariable=self.varCityForm, width=28)
        self.enterCity.grid(row=2, column=1, padx=6, pady=6, sticky="w")

        ttk.Separator(frameForm).grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=6,
            pady=10
        )

        btnCadastrate = ttk.Button(frameForm, text="Cadastrar", command=self.onCadastrate)
        btnCadastrate.grid(row=4, column=0, padx=6, pady=6, sticky="ew", columnspan=2)

        btnUpdate = ttk.Button(frameForm, text="Alterar (Linha selecionada)", command=self.onUpdate)
        btnUpdate.grid(row=5, column=0, padx=6, pady=6, sticky="ew", columnspan=2)

        btnDelete = ttk.Button(frameForm, text="Excluir (Linha selecionada)", command=self.onDelete)
        btnDelete.grid(row=6, column=0, padx=6, pady=6, sticky="ew", columnspan=2)

        btnCleanForm = ttk.Button(frameForm, text="Limpar Form", command=self.onCleanForm)
        btnCleanForm.grid(row=7, column=0, padx=6, pady=(6, 10), sticky="ew", columnspan=2)

        lblInfo = ttk.Label(frameForm, text="Dica: Selecione uma linha na tabela para carregar o\n"
                                            "Formulário e então Alterar/Excluir" , foreground="#333")
        lblInfo.grid(row=0, column=0, columnspan=2, padx=6, pady=(0, 10))

    def loadInitialCountry(self):

        countries = self.repo.getCountry()
        self.comboCountry["values"] = ["Todos"] + countries
        self.comboCountry.set("(Todos)")

        self.comboState.set["values"] = ["Todos"]
        self.comboState.set("(Todos)")

        self.comboCity.set["values"] = ["Todos"]
        self.comboCity.set("(Todos)")


    def onChosenCountry(self, _event: None):

        country = self.varCountryFilter.get()

        if country == "(Todos)":

            self.comboState["values"] = ["Todos"]
            self.comboState.set("(Todos)")

            self.comboCity["values"] = ["Todos"]
            self.comboCity.set("(Todos)")

            self.updateTable()

            return

        estados = self.repo.getEstados(country)

        self.comboState["values"] = ["(Todos)"] + estados
        self.comboState.set("(Todos)")

        self.comboCity["values"] = ["(Todos)"]
        self.comboCity.set("(Todos)")

        self.updateTable()

    def onChosenState(self, _event: None):

        country = self.varStateFilter.get()
        state = self.varStateFilter.get()

        if state == "(Todos)" or not country or country == "(Todos)":

            self.comboCity["values"] = ["Todos"]
            self.comboCity.set("(Todos)")

            self.updateTable()

            return

        city = self.repo.getCity(country, city)

        self.comboCity["values"] = ["(Todos)"] + city
        self.comboCity.set("(Todos)")

        self.updateTable()

    def updateTable(self):

        country = self.varCountryFilter.get()
        state  = self.varStateFilter.get()
        city = self.varCityFilter.get()

        countryF = None if not country or country == "(Todos)" else country
        stateF = None if not state or state == "(Todos)" else state
        cityF = None if not city or city == "(Todos)" else city

        lines = self.repo.list(country=countryF, state=stateF, city=cityF)

        for item in self.tree.get_children():

            self.tree.delete(item)

        for loc in lines:

            self.tree.insert("", tk.END, values=(loc.id, loc.country, loc.state, loc.city))

        self.selectedId = None

    def captureSelection(self , _event: None):

        sel = self.tree.selection()

        if not sel:
            return

        values = self.tree.item(sel[0], "values")

        if not values:
            return

        self.selectedId = int(values[0])

        self.varCityForm.set(values[1])
        self.varStateForm.set(values[2])
        self.varCountryForm.set(values[3])

    def cleanFilter(self):

        self.loadInitialCountry()

        self.updateTable()

    def cleanForm(self):

        self.selectedId = None

        self.varCountryForm.set("")
        self.varStateForm.set("")
        self.varCityForm.set("")

    def validateForm(self) -> bool:

        if not self.varCountryForm.get().strip():

            messagebox.showwarning("Atenção" , "Informe o País.")

            return False

        if not self.varStateForm.get().strip():

            messagebox.showwarning("Atenção" , "Informe o Estado.")

            return False

        if not self.varCityForm.get().strip():

            messagebox.showwarning("Atenção" , "Informe a Cidade.")

            return False

        return True

   # def cadastrate(self):














if __name__ == "__main__":

    app = AppCombosDependentes()
    app.mainloop()












