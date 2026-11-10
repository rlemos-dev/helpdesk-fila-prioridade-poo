from classes import (
    ChamadoAlto,
    ChamadoBaixo,
    ChamadoCritico,
    ChamadoMedio,
    FilaAtendimento,
)


def gerar_massa_de_testes(fila: FilaAtendimento):
    """Insere um conjunto fixo de chamados para a demonstração ao vivo."""
    exemplos = [
        (ChamadoBaixo, "Atualização de Antivírus"),
        (ChamadoMedio, "Lente da Câmera Suja"),
        (ChamadoAlto, "Falha na Rede Sem Fio - Bloco B"),
        (ChamadoCritico, "Queda do Servidor de Banco de Dados"),
        (ChamadoBaixo, "Solicitação de Recarga de Toner"),
    ]

    for id_temp, (classe_chamado, titulo) in enumerate(exemplos, start=100):
        ticket = classe_chamado(id=id_temp, titulo=titulo)
        fila.enfileirar(ticket)


# --- BLOCO PARA TESTAR NO VS CODE ---
if __name__ == "__main__":
    # 1. Cria uma instância da fila
    minha_fila = FilaAtendimento()

    # 2. Chama a função de massa de testes para preencher a fila
    gerar_massa_de_testes(minha_fila)

    # 3. Imprime o conteúdo da fila no terminal
    print(f"Total de chamados carregados: {minha_fila.tamanho()}\n")
    for chamado in minha_fila.chamados:
        print(
            f"ID: {chamado.id} | Titulo: {chamado.assunto} | Prioridade: {chamado.pr_atual}"
        )