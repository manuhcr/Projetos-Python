-- Dump gerado em 2026-07-02 19:43:13 --
SET NAMES utf8mb4;
CREATE DATABASE IF NOT EXISTS agrupamentoTabelasDB DEFAULT CHARACTER SET utf8mb4;
USE agrupamentoTabelasDB;

DROP TABLE IF EXISTS vendas;

            CREATE TABLE vendas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nomeCliente VARCHAR(100) NOT NULL,
                total DECIMAL(12,2) NOT NULL,
                cidade VARCHAR(80) NOT NULL,
                setor VARCHAR(60) NOT NULL,
                produto VARCHAR(100) NOT NULL,
                quantidade INT NOT NULL,
                precoUnitario DECIMAL(12,2) NOT NULL,
                dataVenda DATE NOT NULL,
                INDEX indexCliente (nomeCliente),
                INDEX indexDataVenda (dataVenda)
            ) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4;
            


                INSERT INTO vendas
                (
                    nomeCliente,
                    total,
                    cidade,
                    setor,
                    produto,
                    quantidade,
                    precoUnitario,
                    dataVenda
                )
                VALUES
                
(1, 'Alpha SA', 4500.00, 'São Paulo', 'Varejo', 'Notebook 14', 5, 900.00, '2025-01-10'),
(2, 'Alpha SA', 2100.00, 'São Paulo', 'Varejo', 'Mouse sem fio', 30, 70.00, '2025-01-12'),
(3, 'Beta Ltda', 7800.00, 'Rio de Janeiro', 'Serviços', 'Servidor Torre', 2, 3900.00, '2025-02-03'),
(4, 'Beta Ltda', 960.00, 'Rio de Janeiro', 'Serviços', 'Teclado Mecânico', 12, 80.00, '2025-02-05'),
(5, 'Delta EPP', 6250.00, 'Curitiba', 'Atacado', 'Monitor 27"', 10, 625.00, '2025-04-02'),
(6, 'Delta EPP', 480.00, 'Curitiba', 'Atacado', 'Cabo HDMI 2m', 40, 12.00, '2025-04-04'),
(7, 'Gamma ME', 3200.00, 'Belo Horizonte', 'Indústria', 'Impressora Laser', 4, 800.00, '2025-03-15'),
(8, 'Gamma ME', 1540.00, 'Belo Horizonte', 'Indústria', 'HD Externo 1TB', 14, 110.00, '2025-03-22'),
(9, 'Omega SA', 10350.00, 'Porto Alegre', 'Educação', 'Chromebook', 15, 690.00, '2025-04-18'),
(10, 'Omega SA', 2750.00, 'Porto Alegre', 'Educação', 'Headset USB', 25, 110.00, '2025-04-19'),
(11, 'Sigma ME', 4200.00, 'Salvador', 'Saúde', 'Desktop Slim', 6, 700.00, '2025-05-08'),
(12, 'Sigma ME', 1620.00, 'Salvador', 'Saúde', 'Webcam HD', 18, 90.00, '2025-05-12');