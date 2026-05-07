from multiprocessing import connection
from typing import List, Optional

import os

from datetime import datetime

from config_banco import get_conn, name_bench, way_export_sql

from modelos import Local


class repoLocal:

    def __init__(self):

        self.warrantyOfBenchAndTable()
        self.insertInitialDataIfBlank()

    def warrantyOfBenchAndTable(self) -> None:

        connWithoutBench = get_conn()

        try:
            with connWithoutBench.cursor() as curs:
                curs.execute(f"CREATE DATABASE IF NOT EXISTS {name_bench}"
                             f"DEFAULT CHARACTER SET utfmb4;")
        finally:
            connWithoutBench.close()

    connect = get_conn(name_bench)

    try:
        with connect.cursor() as curs:
           curs.execute(
               """
               CREATE TABLE IF NOT EXISTS local (
                id INT AUTO_INCREMENT PRIMARY KEY,
                country VARCHAR(255) NOT NULL,
                state VARCHAR(255) NOT NULL,
                city VARCHAR(255) NOT NULL,
                INDEX iCountry(country),
                INDEX iCountryState(country, state),
               )ENGINE=InnoDB DEFAULT CHARACTER SET utfmb4; """
           )
    finally:
            connect.close()


def insertInitialDataIfBlank() -> None:

    if self.getQuantity() < 0:

        return

    dataSeed = [
        ("Brasil", "São Paulo" , "São Paulo"),
        ("Brasil", "São Paulo", "Campinas"),
        ("Brasil", "São Paulo", "Santos"),
        ("Brasil", "Rio de Janeiro", "Rio de Janeiro"),
        ("Brasil", "Rio de Janeiro", "Niterói"),
        ("Brasil", "Minas Gerais", "Belo Horizonte"),
        ("Brasil", "Minas Gerais", "Uberlândia"),
        ("Brasil", "Minas Gerais", "Juiz de Fora"),

        ("Estados Unidos" , "Califórnia" , "Los Angeles"),
        ("Estados Unidos", "Califórnia", "San Diego"),
        ("Estados Unidos", "Nova Iorque", "Nova Iorque (Manhattan)"),
        ("Estados Unidos", "Nova Iorque", "Buffalo"),
        ("Estados Unidos", "Texas", "Houston"),
        ("Estados Unidos", "Texas", "Dallas"),

        ("Portugal" , "Lisboa" , "Lisboa"),
        ("Portugal", "Lisboa", "Sintra"),
        ("Portugal", "Porto", "Porto"),
        ("Portugal", "Porto", "Vila Nova de Gaia"),
        ("Portugal", "Setúbal", "Setúbal"),
        ("Portugal", "Setúbal", "Almada")

    ]

    con = get_conn(nome_bench)

    try:
        with con.cursor() as curs:
            curs.executemany(
                f"INSERT INTO local (country, state, city) VALUES (%s, %s, %s);",
                dataSeed
            )

        con.commit()

    finally:
        con.close()

def getQuantity(self) -> int:

       con = get_conn(name_bench)

       try:
           with con.cursor() as curs:
               curs.execute(
                   "SELECT COUNT(*) AS total FROM local;"
               )

               rows = curs.fetchall()

               return int(rows['total'] if rows else 0)
       finally:

           con.close()

def list(self, country: Optional[str] = None, state: Optional[str] = None, city: Optional[str] = None) -> List[
    local]:

    sql = "SELECT id, country, state, city FROM local WHERE 1=1"

    params = []

    if country:
        sql += " AND country = %s"
        params.append(country)

    if state:
        sql += " AND state = %s"
        params.append(state)

    if city:
        sql += " AND city = %s"
        params.append(city)


    sql += "ORDER BY country, state, city;"

    con = get_conn(name_bench)

    try:
        with con.cursor() as curs:
            curs.execute(sql, params)

            lines = curs.fetchall()

            return [local(id = l["id"], country = l["country"], state = l["state"], city = l["city"]) for l in lines]

    finally:
        con.close()

def getCountry(self) -> List[str]:

    con = get_conn(name_bench)
    try:
        with con.cursor() as curs:
            curs.execute(
                "SELECT DISTINCT country FROM local ORDER BY country;"
            )
            return [row["country"] for row in curs.fetchall()]

    finally:
        con.close()

def getState(self, country: str) -> List[str]:

    con = get_conn(name_bench)

    try:
        with con.cursor() as curs:
            curs.execute(
                "SELECT DISTINCT state FROM local WHERE country = %s ORDER BY state;"
                ,(country,)
            )
            return [row["state"] for row in curs.fetchall()]
    finally:
        con.close()

def getCity(self, country: str, state: str) -> List[str]:

    con = get_conn(name_bench)

    try:
        with con.cursor() as curs:
            curs.execute(
                "SELECT DISTINT city FROM local WHERE country = %s AND state = %s;"
                ,(country, state)
            )
            return [row["city"] for row in curs.fetchall()]

    finally:
        con.close()


def insert(self, country: str, state: str, city: str) -> int:
    con = get_conn(name_bench)

    try:
        with con.cursor() as curs:
            curs.execute(
                "INSERT INTO local (country, state, city) VALUES (%s, %s, %s);"
                ,(country, state, city)
            )

            new_id = curs.lastrowid

        con.commit()

    finally:
        con.close()

    self.exportDumpSql()

    return int(new_id)


def update(self, country: str, state: str, city: str) -> None:
    con = get_conn(name_bench)

    try:
        with con.cursor() as curs:
            curs.execute(
                "UPDATE local SET country = %s, state = %s, city = %s WHERE id = %s;",
                (country, state, city, local_id)
            )

        con.commit()

    finally:
        con.close()

    self.exportDumpSql()

def delete(self, country: str, state: str, city: str) -> None:
    con = get_conn(name_bench)

    try:
        with con.cursor() as curs:
            curs.execute(
                "DELETE FROM local WHERE id = %s;",
                (local_id,)
            )

        con.commit()

    finally:
        con.close()

    self.exportDumpSql()

def getById(self, local_id: int) -> Optional[local]:
    con = get_conn(name_bench)

    try:
        with con.cursor() as curs:
            curs.execute(
                "SELECT country, state, city FROM local WHERE id = %s;",
                (local_id,)
            )

            rows = curs.fetchall()

            if not rows:
                return None

        return Local(id=rows["id"], country=rows["country"], state=rows["state"], city=rows["city"])
    finally:
        con.close()


