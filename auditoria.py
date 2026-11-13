import os
from datetime import datetime

# Auditoria da fila de atendimento: toda entrada e saída de chamado é gravada como INSERT no arquivo logs.sql.


class AuditoriaSQL:
    def __init__(self, arquivo="logs.sql"): # Se o arquivo de logs ainda não existir, cria ele já com as tabelas.
        self.arquivo = arquivo
        if not os.path.exists(arquivo) or os.path.getsize(arquivo) == 0:
            self.escrever(
                "CREATE TABLE IF NOT EXISTS log_enfileiramentos (\n"
                "    chamado_id INTEGER,\n"
                "    assunto VARCHAR(255),\n"
                "    classe VARCHAR(50),\n"
                "    prioridade_original INTEGER,\n"
                "    horario_criacao TIMESTAMP\n"
                ");\n\n"
                "CREATE TABLE IF NOT EXISTS log_atendimentos (\n"
                "    chamado_id INTEGER,\n"
                "    assunto VARCHAR(255),\n"
                "    prioridade_final INTEGER,\n"
                "    tempo_espera_seg REAL,\n"
                "    estourou_sla INTEGER\n"
                ");\n\n"
            )

    def escrever(self, texto): # Adiciona o texto no final do arquivo de logs.
        with open(self.arquivo, "a", encoding="utf-8") as f:
            f.write(texto)

    def formatar_texto(self, texto): # Coloca o texto entre aspas simples e troca ' por '' para não quebrar o comando SQL.
        texto = str(texto).replace("'", "''")
        return f"'{texto}'"

    def registrar_enfileiramento(self, chamado): # Registra a entrada do chamado na fila.
        classe = chamado.__class__.__name__
        horario = datetime.fromtimestamp(chamado.horario_criacao).strftime("%Y-%m-%d %H:%M:%S")

        self.escrever(
            "INSERT INTO log_enfileiramentos (chamado_id, assunto, classe, prioridade_original, horario_criacao) \n"
            f"VALUES ({chamado.id}, {self.formatar_texto(chamado.assunto)}, '{classe}', {chamado.pr_original}, '{horario}');\n"
        )

    def registrar_atendimento(self, chamado): # Registra a saída do chamado com o tempo de espera, a prioridade final e se estourou o SLA.
        tempo_espera = round(chamado.calcular_tempo_espera(), 1)
        estourou = 1 if chamado.estourou_sla() else 0

        self.escrever(
            "INSERT INTO log_atendimentos (chamado_id, assunto, prioridade_final, tempo_espera_seg, estourou_sla) \n"
            f"VALUES ({chamado.id}, {self.formatar_texto(chamado.assunto)}, {chamado.pr_atual}, {tempo_espera}, {estourou});\n"
        )
