-- Dump gerado em 2026-06-22 19:47:56 --
SET NAMES utf8mb4;
CREATE DATABASE IF NOT EXISTS agendaDatasBrDb DEFAULT CHARACTER SET utf8mb4;
USE agendaDatasBrDb;

DROP TABLE IF EXISTS eventos;

            CREATE TABLE eventos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                descricao VARCHAR(200) NOT NULL,
                dataEvento DATE NOT NULL,
                INDEX indexDataEvento (dataEvento)
            ) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4;
            

INSERT INTO eventos(id, descricao, dataEvento) VALUES
(1, 'Workshop Excel Avançado', '2024-11-15'),
(2, 'Implantação Power BI Loja A', '2024-12-03'),
(3, 'Revisão Relatório Vendas Q4', '2024-12-28'),
(4, 'Virada de Ano - Planejamento 2030', '2024-12-31'),
(24, 'Planejamento 2026', '2025-12-20'),
(21, 'Onboarding Novos Analistas', '2026-01-15'),
(22, 'Workshop: Modelagem de Dados', '2026-02-04'),
(23, 'Hackday Automação Relatórios', '2026-03-10'),
(5, 'Reunião Kickoff Projetos 2030', '2030-01-06'),
(6, 'Entrega Dashboard Financeiro', '2030-01-20'),
(7, 'Treinamento Python p/ Dados', '2030-02-10'),
(8, 'Sprint BI - Sem. 1', '2030-02-17'),
(9, 'Sprint BI - Sem. 2', '2030-02-24'),
(10, 'Auditoria de Indicadores', '2030-03-12'),
(11, 'Palestra: Boas Práticas SQL', '2030-03-25'),
(12, 'Fechamento Q2', '2030-03-31'),
(13, 'Oficina: Tkinter na Prática', '2030-04-08'),
(14, 'Atualização KPIs Comercial', '2030-04-19'),
(15, 'Revisão Meta Trimestral', '2030-04-30'),
(16, 'Entrega Relatório Semestral', '2030-06-30'),
(17, 'Kickoff Campanha Black Friday', '2030-09-01'),
(18, 'Prévia Black Friday (Stress Test)', '2030-10-15'),
(19, 'Black Friday', '2030-11-28'),
(20, 'Pós-Mortem Black Friday', '2030-12-05');