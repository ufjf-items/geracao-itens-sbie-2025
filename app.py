import os
import getpass
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.chat_models import init_chat_model
from utils import get_codigo_da_classe,get_especificacao_tarefa_exemplo, get_variables
import pandas as pd

load_dotenv()

"""
if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")
"""

template ="""

# Template BNCC para língua portuguesa
### CÓDIGO DO TEMPLATE BNCC : {BNCC}

<exemplo>

{comando1_exemplo}

**Texto suporte:**

{suporte_exemplo}

**Pergunta:**
{comando2_exemplo}
{respostas_exemplo}

**Justificativa das alternativas**\
{justificativas_exemplo}

</exemplo>

<contexto>

Você é um elaborador de itens avaliativos para Língua Portuguesa, com experiência em criar questões de múltipla escolha para estudantes do Ensino Fundamental. Você deve seguir as diretrizes e especificações fornecidas para criar questões que sejam claras, objetivas e que avaliem adequadamente as competências e habilidades dos alunos.
## Objetivo
Criar questões avaliativas de **Língua Portuguesa** para estudantes do **Ensino Fundamental**, seguindo as especificações de uma avaliação em larga escala. As questões devem ser adequadas ao nível educacional das crianças e contribuir para métricas que avaliam a qualidade da educação.


## Especificações das Questões

- **Competência Avaliada**: {descritor}
- **Tipo de Texto**: {tipo_de_texto}
- **Habilidade Avaliada**: {classe}
- **Estrutura da Questão**:
  - **Comando 1** {comando1}
  - **Texto suporte** {suporte}
  - **Comando 2** {comando2}
  - **Gabarito** {gabarito}
  - **Distratores** {distratores}
  - **Justificativa para cada alternativa** Quero uma justificativa passo a passo, completa para cada resposta criada, tanto gabarito quanto distratores.

</contexto>

<formato>

## Formato Esperado

Cada questão deve seguir rigorosamente este formato:\
**Texto suporte:** [Inserir suporte]\
P**ergunta:** [Inserir enunciado da questão]\
a) [Opção A]\
b) [Opção B]\
c) [Opção C]\
d) [Opção D]\
**Resposta correta:** [Letra da resposta correta]\

**Justificativas das alternativas:**\
a) [Justificativa detalhada passo a passo para a opção A]\
b) [Justificativa detalhada passo a passo para a opção B]\
c) [Justificativa detalhada passo a passo para a opção C]\
d) [Justificativa detalhada passo a passo para a opção D]

</formato>

<instrucao> Com base no <contexto>, e se inspirando no <exemplo>, crie 4 questões de múltipla escolha seguindo o formato: <formato>
</instrucao>

Historico da conversa:
{history}

Entrada do usuário:
{input}"""



prompt = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)


llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

chain = prompt | llm

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    
    return store[session_id]

chat_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)


def iniciar(id_tarefa = 0, session_id ="user123"):
    
    vars_prompt = get_variables(id_tarefa)
    vars_prompt['input'] = "Gerar Questões"

    resposta = chat_with_history.invoke(
        vars_prompt,
        config={
            'configurable': {'session_id': session_id} 
        }
    )
    print('RESPOSTA:', resposta.content)
    

if __name__ == "__main__":

    iniciar()
