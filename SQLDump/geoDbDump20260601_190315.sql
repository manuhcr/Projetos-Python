--- Dump gerado em 2026-06-01 19:03:15
SET NAMES utf8mb4;
CREATE DATABASE IF NOT EXISTS geo_db;
USE geo_db;
DROP TABLE IF EXISTS local;

            CREATE TABLE local
            (
                id      INT PRIMARY KEY AUTO_INCREMENT,
                country VARCHAR(60) NOT NULL,
                state   VARCHAR(60) NOT NULL,
                city    VARCHAR(80) NOT NULL,
                INDEX   iCountry (country),
                INDEX   iCountryState (country, state)
            ) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4;
            
INSERT INTO local (id, country, state, city) VALUES
(21, 'Brasil', 'Minas Gerais', 'Belo Horizonte'),
(23, 'Brasil', 'Minas Gerais', 'Belo Horizonte'),
(8, 'Brasil', 'Minas Gerais', 'Juiz de Fora'),
(22, 'Brasil', 'Minas Gerais', 'Juiz de Fora'),
(7, 'Brasil', 'Minas Gerais', 'Uberlândia'),
(5, 'Brasil', 'Rio de Janeiro', 'Niterói'),
(4, 'Brasil', 'Rio de Janeiro', 'Rio de Janeiro'),
(25, 'Brasil', 'Santa Catarina', 'Ponte Alta do Norte'),
(26, 'Brasil', 'Santa Catarina', 'Ponte Alta do Norte'),
(27, 'Brasil', 'Santa Catarina', 'Ponte Alta do Norte'),
(28, 'Brasil', 'Santa Catarina', 'Ponte Alta do Norte'),
(3, 'Brasil', 'São Paulo', 'Santos'),
(1, 'Brasil', 'São Paulo', 'São Paulo'),
(2, 'Brasil', 'São Paulo', 'Sorocaba'),
(24, 'Brasil', 'Tocantins', 'Palmas'),
(9, 'Estados Unidos', 'Califórnia', 'Los Angeles'),
(10, 'Estados Unidos', 'Califórnia', 'San Diego'),
(11, 'Estados Unidos', 'Nova Iorque', 'Nova Iorque (Manhattan)'),
(14, 'Estados Unidos', 'Texas', 'Dallas'),
(13, 'Estados Unidos', 'Texas', 'Houston'),
(15, 'Portugal', 'Lisboa', 'Lisboa'),
(16, 'Portugal', 'Lisboa', 'Sintra'),
(17, 'Portugal', 'Porto', 'Porto'),
(18, 'Portugal', 'Porto', 'Vila Nova de Gaia'),
(20, 'Portugal', 'Setúbal', 'Almada'),
(19, 'Portugal', 'Setúbal', 'Setúbal');