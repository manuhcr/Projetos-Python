import tkinter as tk
from tkinter import ttk


def apply_style(root: tk.Tk):
    # O Style gerencia a aparência global dos widgets (como o CSS de um site)
    styles = ttk.Style()

    # O tema 'clam' permite customizar cores de botões que o tema padrão bloqueia
    try:
        styles.theme_use('clam')
    except tk.TclError:
        pass

    # Define a fonte Arial tamanho 10 como padrão para todo o aplicativo
    pattern_font = ('Arial', 10)
    root.option_add('*font', pattern_font)

    # Configura o espaçamento interno das Labels (rótulos)
    styles.configure('TLabel', padding=(2, 2))

    # Configura as Entrys (caixas de texto) com preenchimento interno
    styles.configure('TEntry', padding=(4, 4))

    # Configura o botão: Fundo azul (#005fb8), texto branco e sem bordas 3D antigas
    styles.configure('TButton',
                     padding=(6, 4),
                     background='#005fb8',
                     foreground='white',
                     borderwidth=0)

    # Adiciona o efeito de mudar para azul escuro quando o mouse passar pelo botão
    styles.map('TButton', background=[('active', '#004a8f')])

    # Configura o espaçamento interno dos quadros de grupo (Labelframes)
    styles.configure('TLabelframe', padding=(8, 8))

    # Títulos de grupos e de colunas da tabela ficam em Arial Negrito (Semibold)
    styles.configure('TLabelframe.label', font=('Arial Bold', 10))
    styles.configure('Treeview.Heading', font=('Arial Bold', 10))


def apply_zebra_treeview(tree: ttk.Treeview):
    # Define as cores das linhas da tabela: uma cinza claro e a outra branca
    tree.tag_configure('oddrow', background='#F7F7F7')  # Linhas ímpares
    tree.tag_configure('evenrow', background='#FFFFFF')  # Linhas pares


def field_treeview(tree: ttk.Treeview, rows):
    # Limpa a tabela existente para não repetir os dados ao atualizar
    for i in tree.get_children():
        tree.delete(i)

    # Insere as novas informações linha por linha
    for idx, r in enumerate(rows):
        # Alterna as tags entre par e ímpar para criar o efeito visual de zebra
        # Se par (even) e ímpar (row)
        tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
        # Insere o dado na última posição da tabela com sua respectiva cor
        # tree.insert: Adiciona uma linha na visualização da tabela (Treeview)
        tree.insert(
        '',  # Nó pai (vazio significa que é um item da raiz)
        index='end',  # Coloca o novo item no final da lista
        values=r,  # 'r' é a tupla com os dados (id, nome, etc.) vinda do fetchall()

        # tags=(tag,): Aqui a vírgula é crucial!
        # O Tkinter exige que as tags sejam uma coleção.
        # Mesmo que você só queira aplicar UMA tag (ex: 'par' ou 'impar'),
        # você precisa passá-la dentro de uma tupla (tag,).
        tags=(tag,)
        )

