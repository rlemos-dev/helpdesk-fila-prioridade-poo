CREATE TABLE IF NOT EXISTS log_enfileiramentos (
    chamado_id INTEGER,
    assunto VARCHAR(255),
    classe VARCHAR(50),
    prioridade_original INTEGER,
    horario_criacao TIMESTAMP
);

CREATE TABLE IF NOT EXISTS log_atendimentos (
    chamado_id INTEGER,
    assunto VARCHAR(255),
    prioridade_final INTEGER,
    tempo_espera_seg REAL,
    estourou_sla INTEGER
);

INSERT INTO log_enfileiramentos (chamado_id, assunto, classe, prioridade_original, horario_criacao) 
VALUES (103, 'Queda do Servidor de Banco de Dados', 'ChamadoCritico', 4, '2026-11-22 18:47:45');
INSERT INTO log_enfileiramentos (chamado_id, assunto, classe, prioridade_original, horario_criacao) 
VALUES (102, 'Falha na Rede Sem Fio - Bloco B', 'ChamadoAlto', 3, '2026-11-22 18:47:45');
INSERT INTO log_enfileiramentos (chamado_id, assunto, classe, prioridade_original, horario_criacao) 
VALUES (101, 'Lente da Câmera Suja', 'ChamadoMedio', 2, '2026-11-22 18:47:45');
INSERT INTO log_enfileiramentos (chamado_id, assunto, classe, prioridade_original, horario_criacao) 
VALUES (100, 'Atualização de Antivírus', 'ChamadoBaixo', 1, '2026-11-22 18:47:45');
INSERT INTO log_enfileiramentos (chamado_id, assunto, classe, prioridade_original, horario_criacao) 
VALUES (104, 'Solicitação de Recarga de Toner', 'ChamadoBaixo', 1, '2026-11-22 18:47:45');
