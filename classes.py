import time
from abc import ABC, abstractmethod

# Sistema de suporte de Ti, acontecem chamados de diferentes proiridades e precisamos tratar isso para evitar problemas de Starvation.


class Chamado(ABC):
    def __init__(self, id, titulo): # Classe Abstrata para chamados, com atributos comuns a todos os tipos de chamados.
        self.id = id
        self.assunto = titulo
        self.pr_original = 0
        self.pr_atual = 0
        self.horario_criacao = time.time()
        self.tempo_limite_sla = 0

    def calcular_tempo_espera(self): # Método para calcular o tempo de espera do chamado, subtraindo o horário de criação do horário atual.
        tempo_gasto = time.time() - self.horario_criacao
        return tempo_gasto

    def estourou_sla(self): # Método para verificar se o chamado estourou o SLA, comparando o tempo de espera com o tempo limite do SLA.
        return self.calcular_tempo_espera() > self.tempo_limite_sla

    @abstractmethod
    def aplicar_aging(self): # Método abstrato para aplicar o aging, que será implementado nas subclasses de chamados.
        pass

    def __lt__(self, other): # Método para comparar dois chamados, primeiro comparando a prioridade atual e, em caso de empate, comparando o horário de criação.
        if self.pr_atual != other.pr_atual:
            return self.pr_atual > other.pr_atual
        return self.horario_criacao < other.horario_criacao


class ChamadoCritico(Chamado): # Chamado de prioridade crítica, com prioridade original 4 e tempo limite de SLA de 30 segundos.
    def __init__(self, id, titulo):
        super().__init__(id, titulo)
        self.pr_original = 4
        self.pr_atual = self.pr_original
        self.tempo_limite_sla = 30

    def aplicar_aging(self):
        pass


class ChamadoAlto(Chamado): # Chamado de prioridade alta, com prioridade original 3 e tempo limite de SLA de 60 segundos.
    def __init__(self, id, titulo):
        super().__init__(id, titulo)
        self.pr_original = 3
        self.pr_atual = self.pr_original
        self.tempo_limite_sla = 60

    def aplicar_aging(self): # Método para aplicar o aging, que aumenta a prioridade do chamado se ele estiver esperando há muito tempo.
        tempo_espera = self.calcular_tempo_espera()
        if tempo_espera > 20 and self.pr_atual < 4:
            self.pr_atual = 4


class ChamadoMedio(Chamado): # Chamado de prioridade média, com prioridade original 2 e tempo limite de SLA de 90 segundos.
    def __init__(self, id, titulo):
        super().__init__(id, titulo)
        self.pr_original = 2
        self.pr_atual = self.pr_original
        self.tempo_limite_sla = 90

    def aplicar_aging(self): # Método para aplicar o aging, que aumenta a prioridade do chamado se ele estiver esperando há muito tempo.
        tempo_espera = self.calcular_tempo_espera()
        if tempo_espera > 40 and self.pr_atual < 4:
            self.pr_atual = 4
        elif tempo_espera > 20 and self.pr_atual < 3:
            self.pr_atual = 3


class ChamadoBaixo(Chamado): # Chamado de prioridade baixa, com prioridade original 1 e tempo limite de SLA de 120 segundos.
    def __init__(self, id, titulo):
        super().__init__(id, titulo)
        self.pr_original = 1
        self.pr_atual = self.pr_original
        self.tempo_limite_sla = 120

    def aplicar_aging(self): # Método para aplicar o aging, que aumenta a prioridade do chamado se ele estiver esperando há muito tempo.
        tempo_espera = self.calcular_tempo_espera()
        if tempo_espera > 40 and self.pr_atual < 4:
            self.pr_atual = 4
        elif tempo_espera > 25 and self.pr_atual < 3:
            self.pr_atual = 3
        elif tempo_espera > 10 and self.pr_atual < 2:
            self.pr_atual = 2

class FilaAtendimento:
    def __init__(self, auditoria=None): # Recebe opcionalmente um objeto AuditoriaSQL para registrar as entradas e saídas da fila.
        self.chamados: list[Chamado] = []
        self.auditoria = auditoria

    def enfileirar(self, chamado: Chamado): # Método para adicionar um chamado à fila de atendimento, aplicando o aging e reordenando a lista de chamados.
        self.chamados.append(chamado)
        self.reordenar()
        if self.auditoria is not None:
            self.auditoria.registrar_enfileiramento(chamado)

    def desenfileirar(self): # Método para remover e retornar o chamado com maior prioridade da fila de atendimento, aplicando o aging e reordenando a lista de chamados.
        if not self.esta_vazia():
            chamado = self.chamados.pop(0)
            if self.auditoria is not None:
                self.auditoria.registrar_atendimento(chamado)
            return chamado
        return None

    def espiar(self): # Método para retornar o chamado com maior prioridade da fila de atendimento sem removê-lo, aplicando o aging e reordenando a lista de chamados.
        if not self.esta_vazia():
            return self.chamados[0]
        return None

    def atualizar_fila(self): # Método para atualizar a fila de atendimento, aplicando o aging a todos os chamados e reordenando a lista de chamados.
        for chamado in self.chamados:
            chamado.aplicar_aging()
        self.reordenar()

    def reordenar(self):
        self.chamados.sort()  # Ordena a lista de chamados com base na prioridade e no tempo de criação.

    def esta_vazia(self):
        return len(self.chamados) == 0

    def tamanho(self):
        return len(self.chamados)
    