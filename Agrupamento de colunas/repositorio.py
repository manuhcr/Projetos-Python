from typing import List, Optional
from datetime import date, datetime
import os
from configBanco import obtConexao, nomeBanco, caminhoExportarSQL
from modelos import Venda

class RepoVendas:

    def __init__(self):

        self.garantirBancoEtabela = obtConexao()
        self.inserirDadosSeVazio()

    def garantirBancoEtabela(self):

        raizConexao = obtConexao()

        try:
            with raizConexao.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {nomeBanco} DEFAULT CHARACTER SET 'utf8mb4';")

            raizConexao.connect()

        finally:
            raizConexao.close()

        conexao = obtConexao(nomeBanco)

        try:
            with conexao.cursor() as cursor:
                cursor.execute(
                """
                  CREATE TABLE IF NOT EXISTS Vendas (
                      id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                      nomeCliente  VARCHAR(100) NOT NULL,
                      total DECIMAL(12,2) NOT NULL,
                      cidade  VARCHAR(80) NOT NULL,
                      setor  VARCHAR(60) NOT NULL,
                      produto VARCHAR(100) NOT NULL,
                      quantidade  INT NOT NULL,
                      precoUnitario  DECIMAL(12,2) NOT NULL,
                      dataVenda  DATE NOT NULL,
                      INDEX indexCliente (nomeCliente)
                      INDEX indexDataVenda (dataVenda)
                  ) ENGINE=InnoDB DEFAULT CHARACTER SET 'utf8mb4';
                 """
                )

            conexao.commit()

        finally:
            conexao.close()

    def inserirDadosSeVazio(self):

        if self.obtQnt() > 0:
            return

        dados = [
            #parei aqui
        ]

