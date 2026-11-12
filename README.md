# 🎫 Helpdesk System: Gerenciador de Chamados com Aging & SLA

> **Projeto Prático A3 — Programação de Soluções Computacionais (PSC)**  
> Sistema de gestão de chamados em Python utilizando **Orientação a Objetos (POO)**, fila de prioridades com mecanismo de **Aging** (*fairness*) contra *starvation*, monitoramento de **SLA** em tempo real via **Streamlit** e auditoria transacional exportada em **SQL**.

---

## 📌 Sobre o Projeto

Em sistemas corporativos de Helpdesk, a implementação de prioridades rígidas frequentemente causa a **inanição (*starvation*)** de chamados secundários, deixando tickets de menor urgência travados indefinidamente no fim da fila.

Este projeto resolve esse problema implementando um algoritmo de **Aging (Envelhecimento Temporal)**: à medida que o tempo de espera avança, a prioridade atual do chamado é promovida progressivamente até a criticidade máxima, assegurando um atendimento justo sem violar as regras de prioridade e respeitando a ordem de chegada (FIFO) em casos de empate.

---

## 🚀 Funcionalidades Principais

* **Arquitetura POO Abstrata:** Classe base abstrata `Chamado(ABC)` e 4 subclasses concretas (`ChamadoCritico`, `ChamadoAlto`, `ChamadoMedio`, `ChamadoBaixo`).
* **Mecanismo Anti-Starvation (Aging):** Reavaliação automática da prioridade dos tickets com subida progressiva baseada no tempo decorrido.
* **Ordenação Nativa FIFO (`__lt__`):** Sobrecarga do operador de comparação para manter a fila reordenada por urgência e tempo de criação.
* **Métricas e Qualidade de SLA:** Cálculo dinâmico do tempo de espera com identificação visual de descumprimento de prazos.
* **Interface Web Interativa:** Frontend intuitivo em **Streamlit** para cadastro manual, carga rápida de testes e atendimento de chamados ao vivo.
* **Auditoria SQL (Logs Transacionais):** Registro estruturado de operações de enfileiramento e desenfileiramento para persistência em arquivo `.sql`.

---

## 📐 Estrutura de Classes (Backend POO)

```text
               +-------------------+
               |   Chamado (ABC)   |
               +-------------------+
                         |
      +------------------+------------------+------------------+
      |                  |                  |                  |
+-------------+  +-------------+  +-------------+  +-------------+
|ChamadoCritico| | ChamadoAlto |  | ChamadoMedio|  | ChamadoBaixo|
+-------------+  +-------------+  +-------------+  +-------------+
```

### Detalhamento Completo das Classes

#### 1. Classe Abstrata `Chamado(ABC)`
* **Atributos:**
  * `id` (int): Identificador único do chamado.
  * `assunto` (str): Descrição/título do chamado.
  * `pr_original` (int): Nível de prioridade inicial atribuído na criação (1 a 4).
  * `pr_atual` (int): Nível de prioridade corrente (ajustado dinamicamente pelo aging).
  * `horario_criacao` (float): Timestamp (`time.time()`) registrado no momento da criação.
  * `tempo_limite_sla` (float): Janela máxima tolerada em segundos para o cumprimento do SLA.
* **Métodos:**
  * `calcular_tempo_espera()`: Retorna a diferença em segundos entre o tempo atual e o horário de criação.
  * `estourou_sla()`: Retorna um valor booleano indicando se o tempo de espera ultrapassou o limite do SLA.
  * `aplicar_aging()` *(Método Abstrato)*: Define a regra temporal de promoção de prioridade específica de cada subclasse.
  * `__lt__(other)`: Sobrecarga do operador `<` para comparação. Ordena por `pr_atual` (decrescente) e desempata por `horario_criacao` (crescente/FIFO).

#### 2. Subclasses Concretas
* **`ChamadoCritico`**: Prioridade inicial 4 (máxima). SLA: $30s$. Não possui aging por já estar na prioridade máxima.
* **`ChamadoAlto`**: Prioridade inicial 3. SLA: $60s$. Aging: promove para prioridade 4 após $20s$ de espera.
* **`ChamadoMedio`**: Prioridade inicial 2. SLA: $90s$. Aging: promove para prioridade 3 aos $20s$ e para 4 aos $40s$.
* **`ChamadoBaixo`**: Prioridade inicial 1. SLA: $120s$. Aging: promove para prioridade 2 aos $10s$, 3 aos $25s$ e 4 aos $40s$.

#### 3. Classe Gerenciadora `FilaAtendimento`
* **Atributos:**
  * `chamados` (list[Chamado]): Lista interna que armazena os chamados ativos na fila.
* **Métodos:**
  * `enfileirar(chamado)`: Adiciona um novo chamado à lista e executa a reordenação automática.
  * `desenfileirar()`: Remove e retorna o chamado do topo da fila (índice 0). Retorna `None` se a fila estiver vazia.
  * `espiar()`: Consulta e retorna o chamado do topo da fila sem removê-lo.
  * `atualizar_fila()`: Percorre a fila executando `aplicar_aging()` em cada ticket e aciona o reordenamento.
  * `reordenar()`: Dispara `self.chamados.sort()`, invocando nativamente a lógica de comparação do `__lt__`.
  * `esta_vazia()`: Retorna `True` se a lista não contiver elementos (programação defensiva).
  * `tamanho()`: Retorna a quantidade total de chamados aguardando atendimento.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **Interface Gráfica:** Streamlit
* **Paradigma:** Orientação a Objetos (POO)
* **Auditoria & Persistência:** SQL (`logs.sql`)

---

## 🔧 Como Executar o Projeto

### Pré-requisitos
Certifique-se de ter o Python 3.10+ instalado no seu sistema.

### 1. Clonar o repositório
```bash
git clone https://github.com/SEU-USUARIO/helpdesk-fila-prioridade-poo.git
cd helpdesk-fila-prioridade-poo
```

### 2. Instalar dependências
```bash
pip install streamlit
```

### 3. Rodar a aplicação
```bash
streamlit run app.py
```

---

## 📜 Registro de Auditoria (SQL)

Todas as ações de entrada (`enfileirar`) e saída (`desenfileirar`) são registradas no arquivo de auditoria `logs.sql` pela classe `AuditoriaSQL` (`auditoria.py`). Para ativar, basta passar a auditoria ao criar a fila:

```python
from auditoria import AuditoriaSQL

fila = FilaAtendimento(auditoria=AuditoriaSQL("logs.sql"))
```

Na primeira execução o arquivo é criado com as tabelas `log_enfileiramentos` e `log_atendimentos`. Depois disso, cada operação gera um `INSERT`:

```sql
-- Entrada na fila (enfileirar)
INSERT INTO log_enfileiramentos (chamado_id, assunto, classe, prioridade_original, horario_criacao) 
VALUES (103, 'Queda do Servidor', 'ChamadoCritico', 4, '2026-11-12 17:32:42');

-- Saída da fila (desenfileirar)
INSERT INTO log_atendimentos (chamado_id, assunto, prioridade_final, tempo_espera_seg, estourou_sla) 
VALUES (103, 'Queda do Servidor', 4, 35.2, 1);
```

O arquivo pode ser importado direto no banco (ex.: `sqlite3 banco.db < logs.sql`).

---

## 👥 Integrantes do Grupo e Divisão de Tarefas

* **Desenvolvedor Backend POO & Algoritmo de Fila:** Modelagem das classes, regras de aging, SLA e método `__lt__`.
* **Desenvolvedor Frontend (Streamlit):** Construção da interface gráfica, formulários e visualização da fila em tempo real.
* **Modelagem de Banco de Dados & Logs SQL:** Estruturação da auditoria e exportação de logs `.sql`.
* **Documentação Técnica & UML:** Elaboração do relatório técnico, diagramas UML e dicionário de métodos.