import os
import getpass
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.chat_models import init_chat_model
from utils import get_codigo_da_classe,get_especificacao_tarefa_exemplo, get_variables
from openRouter import ChatOpenRouter
import pandas as pd

load_dotenv()

"""
if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")
"""

template ="""

# Template BNCC para língua portuguesa
### CÓDIGO DO TEMPLATE BNCC : {BNCC}

{exemplo}

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
  - **Justificativa para cada alternativa** Quero uma justificativa completa para cada resposta criada, tanto gabarito quanto distratores.

</contexto>

<formato>

## Formato Esperado

{{
  "Questões": [
    {{
      "Competência avaliada": "[Inserir competência]",
      "Comando 1": "[Inserir comando 1]",

      "Texto suporte": "[Inserir suporte]",
      "Comando 2": "[Inserir comando 2]",
      "Opções": {{
        "a": "[Opção A]",
        "b": "[Opção B]",
        "c": "[Opção C]",
        "d": "[Opção D]"
      }},
      "Resposta correta": "[Letra da resposta correta]",
      "Justificativas": {{
        "a": "[Justificativa detalhada passo a passo para a opção A]",
        "b": "[Justificativa detalhada passo a passo para a opção B]",
        "c": "[Justificativa detalhada passo a passo para a opção C]",
        "d": "[Justificativa detalhada passo a passo para a opção D]"
      }},
      "->": {cot}
    }}
  ]
}

</formato>

<instrucao> Com base no <contexto>, e se inspirando no <exemplo>, crie 5 questões de múltipla escolha seguindo o formato: <formato>
{usar_cot}{ep}
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

#llm = ChatOpenRouter( model_name="deepseek/deepseek-chat-v3-0324:free" )



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


def iniciar(id_tarefa, output, session_id ="user123", CoT = False, Ep = False, few_shot = False):
    
    vars_prompt = get_variables(id_tarefa)
    vars_prompt['input'] = "Gerar Questões"


    
    exemplo = """
<exemplo>

{comando1_exemplo}

**Texto suporte:**

{suporte_exemplo}

**Pergunta:**
{comando2_exemplo}
{respostas_exemplo}

**Justificativa das alternativas**\
{justificativas_exemplo}

</exemplo> """ if few_shot else ""

    
    ep = "A educação brasileira depende fortemente disso." if Ep else ""
    usar_cot = "Pense passo a passo e explique cada parte do seu raciocínio ao final de cada questão gerada." if CoT else ""
    cot = "[Linha de raciocínio detalhada para a construção da questão]" if CoT else ""
    vars_prompt['usar_cot'] = usar_cot
    vars_prompt['ep']=ep
    vars_prompt['cot'] = cot
    vars_prompt['exemplo'] = exemplo
        

    resposta = chat_with_history.invoke(
        vars_prompt,
        config={
            'configurable': {'session_id': session_id} 
        }
    )
    print('RESPOSTA:', resposta.content)


    # Salvar a resposta em um arquivo CSV
    resposta_json = resposta.content

    with open(output, 'w') as f:
        f.write(resposta_json)
    

import json

def transformar_json_em_txt(caminho_json, caminho_txt):
    with open(caminho_json, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    linhas = []

    for i, questao in enumerate(dados["questoes"], start=1):
        linhas.append(f"Questão {i}")
        linhas.append(f"Competência Avaliada: {questao['Competencia Avaliada']}")
        linhas.append(f"Comando: {questao['Comando 1']}")
        linhas.append("Texto de Suporte:")
        linhas.append(questao['texto_suporte'])
        linhas.append("Pergunta:")
        linhas.append(questao['pergunta'])
        linhas.append("Opções:")

        for letra, opcao in questao['opcoes'].items():
            prefixo = "->" if letra == questao['resposta_correta'] else "  "
            linhas.append(f"{prefixo} {letra}) {opcao}")

        linhas.append("Justificativas:")
        for letra, justificativa in questao['justificativas'].items():
            linhas.append(f"{letra}) {justificativa}")
          

        linhas.append("\n" + "-"*80 + "\n")


    with open(caminho_txt, 'w', encoding='utf-8') as f:
        f.write("\n".join(linhas))

    print(f"Arquivo gerado com sucesso em: {caminho_txt}")




    

if __name__ == "__main__":

  iniciar(5, 'saidaCL223EFCL2_Gemini_2.0_flash.json', session_id="user123", CoT=True, Ep = True, few_shot = True)

  #transformar_json_em_txt('saidaCL223EFCL2_Gemini_2.0_flash.json', 'saidaCL223EFCL2_Gemini_2.0_flash.txt')
  
    
  