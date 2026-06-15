from typing import List, Optional
from datetime import date, datetime
import os
from configBanco import obterConexao , nomeBanco, host, porta, usuario, senha
from modelos import Evento

class RepoEventos:
    def __init__(self):
        self.garantirBancoEtabela()
        self.insertSeedSeVazio()

    def garantirBancoEtabela(self) -> None:
        