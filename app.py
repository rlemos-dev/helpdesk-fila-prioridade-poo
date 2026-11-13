import streamlit as st
from classes import (
    ChamadoAlto,
    ChamadoBaixo,
    ChamadoCritico,
    ChamadoMedio,
    FilaAtendimento,
)
from massa_dados import gerar_massa_de_testes

# Configurar a página da web
st.set_page_config(page_title="Central de Atendimento TI", layout="wide")

st.title("🖥️ Central de Atendimento TI - Monitoramento de Fila e SLAs")

# Mantém a fila guardada na memória enquanto a página estiver aberta
if "fila" not in st.session_state:
    st.session_state.fila = FilaAtendimento()
    st.session_state.contador_id = 1

fila: FilaAtendimento = st.session_state.fila

# Atualiza a fila aplicando o aging automaticamente a cada interação
fila.atualizar_fila()

# --- MENU LATERAL PARA GERIR CHAMADOS ---
with st.sidebar:
    st.header("➕ Abrir Novo Chamado")
    with st.form("form_chamado", clear_on_submit=True):
        assunto = st.text_input(
            "Assunto / Problema", placeholder="Ex: Computador não liga"
        )
        prioridade = st.selectbox(
            "Prioridade Base",
            options=[1, 2, 3, 4],
            format_func=lambda x: {
                1: "1 - Baixa (SLA 120s)",
                2: "2 - Média (SLA 90s)",
                3: "3 - Alta (SLA 60s)",
                4: "4 - Crítica (SLA 30s)",
            }[x],
        )

        btn_adicionar = st.form_submit_button(
            "Adicionar à Fila", use_container_width=True
        )

        if btn_adicionar and assunto.strip():
            # Instancia a subclasse específica respeitando o SLA original de cada uma
            if prioridade == 4:
                novo_chamado = ChamadoCritico(
                    id=st.session_state.contador_id, titulo=assunto
                )
            elif prioridade == 3:
                novo_chamado = ChamadoAlto(
                    id=st.session_state.contador_id, titulo=assunto
                )
            elif prioridade == 2:
                novo_chamado = ChamadoMedio(
                    id=st.session_state.contador_id, titulo=assunto
                )
            else:
                novo_chamado = ChamadoBaixo(
                    id=st.session_state.contador_id, titulo=assunto
                )

            fila.enfileirar(novo_chamado)
            st.session_state.contador_id += 1
            st.success("Chamado adicionado com sucesso!")
            st.rerun()

    st.markdown("---")
    st.header("⚙️ Ações da Fila")

    if st.button("✅ Atender Próximo Chamado", use_container_width=True):
        if not fila.esta_vazia():
            atendido = fila.desenfileirar()
            st.toast(
                f"Atendendo Chamado #{atendido.id}: {atendido.assunto}",
                icon="🛠️",
            )
            st.rerun()
        else:
            st.warning("A fila está vazia!")

    if st.button("📦 Carregar Massa de Testes", use_container_width=True):
        gerar_massa_de_testes(fila)
        st.toast("Massa de testes carregada na fila!", icon="📥")
        st.rerun()

    if st.button("🔄 Atualizar Tela", use_container_width=True):
        st.rerun()

# --- MÉTRICAS NO TOPO ---
total_na_fila = fila.tamanho()
estourados = sum(1 for c in fila.chamados if c.estourou_sla())
dentro_sla = total_na_fila - estourados

col1, col2, col3 = st.columns(3)
col1.metric("📄 Total na Fila", total_na_fila)
col2.metric("🟢 Dentro do SLA", dentro_sla)
col3.metric("🔴 SLA Estourado", estourados)

st.markdown("---")
st.subheader("Fila de Espera em Tempo Real")

# --- TABELA DA FILA ---
if fila.esta_vazia():
    st.info("Nenhum chamado na fila neste momento.")
else:
    dados_tabela = []
    for c in fila.chamados:
        status_sla = "🔴 Estourado" if c.estourou_sla() else "🟢 No Prazo"
        dados_tabela.append(
            {
                "ID": c.id,
                "Assunto": c.assunto,
                "Prioridade Original": c.pr_original,
                "Prioridade Atual (Aging)": c.pr_atual,
                "Tempo de Espera (s)": round(c.calcular_tempo_espera(), 1),
                "Limite SLA (s)": c.tempo_limite_sla,
                "Status SLA": status_sla,
            }
        )

    st.dataframe(dados_tabela, use_container_width=True)