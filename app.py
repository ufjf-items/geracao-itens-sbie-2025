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

Criar questões avaliativas de **Língua Portuguesa** para estudantes do **Ensino Fundamental**.

## Especificações das Questões

- **Competência Avaliada**: {descritor}
- **Tipo de Texto**: {tipo_de_texto}
- **Habilidade Avaliada**: {classe}
- **Estrutura da Questão**:
  - **Comando 1** {comando1}
  - **Texto suporte** {suporte}. Use exatamente esse suporte.
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
}}

</formato>

<instrucao> Com base no <contexto>, e se inspirando no <exemplo>, crie uma questão de múltipla escolha seguindo o formato: <formato>
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

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    
    return store[session_id]




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


    format_exemplo = exemplo.format(
        comando1_exemplo=vars_prompt.get('comando1_exemplo', ''),
        suporte_exemplo=vars_prompt.get('suporte_exemplo', ''),
        comando2_exemplo=vars_prompt.get('comando2_exemplo', ''),
        respostas_exemplo=vars_prompt.get('respostas_exemplo', ''),
        justificativas_exemplo=vars_prompt.get('justificativas_exemplo', ''),
    )

    ep = "A educação brasileira depende fortemente disso." if Ep else ""
    usar_cot = "Pense passo a passo e explique cada parte do seu raciocínio ao final de cada questão gerada." if CoT else ""
    cot = "[Linha de raciocínio detalhada para a construção da questão]" if CoT else ""
    vars_prompt['usar_cot'] = usar_cot
    vars_prompt['ep']=ep
    vars_prompt['cot'] = cot
    vars_prompt['exemplo'] = format_exemplo


    # # Construir o prompt completo
    # prompt_completo = template.format(
    #     BNCC=vars_prompt.get('BNCC', ''),
    #     descritor=vars_prompt.get('descritor', ''),
    #     tipo_de_texto=vars_prompt.get('tipo_de_texto', ''),
    #     classe=vars_prompt.get('classe', ''),
    #     comando1=vars_prompt.get('comando1', ''),
    #     suporte=vars_prompt.get('suporte', ''),
    #     comando2=vars_prompt.get('comando2', ''),
    #     gabarito=vars_prompt.get('gabarito', ''),
    #     distratores=vars_prompt.get('distratores', ''),
    #     cot=cot,
    #     usar_cot=usar_cot,
    #     ep=ep,
    #     exemplo=format_exemplo,
    #     history='',  # Você pode adicionar o histórico se necessário
    #     input=vars_prompt['input']
    # )

    # print("="*80)
    # print("PROMPT QUE SERÁ ENVIADO:")
    # print("="*80)
    # print(prompt_completo)
    # print("="*80)

    # print("\n HISTÓRICO ANTES DO .invoke():")
    # hist = get_session_history(session_id)
    # for i, msg in enumerate(hist.messages):
    #     print(f"{i+1}. [{msg.type}] {msg.content[:400]}...")

    resposta = chat_with_history.invoke(
        vars_prompt,
        config={
            'configurable': {'session_id': session_id} 
        }
    )
    # print('RESPOSTA:', resposta.content)

    # print("\n HISTÓRICO DEPOIS DO .invoke():")
    # hist = get_session_history(session_id)
    # for i, msg in enumerate(hist.messages):
    #     print(f"{i+1}. [{msg.type}] {msg.content[:400]}...")



    # Salvar a resposta em um arquivo CSV
    resposta_json = resposta.content

    with open(output, 'w') as f:
        f.write(resposta_json)
    

import json

def transformar_json_em_txt(caminho_json, caminho_txt):
    
    with open(caminho_json, 'r', encoding='utf-8') as f:

        texto = f.read()

        inicio = texto.find("```json")
        fim = texto.find("```", inicio + 7)  # 7 = len("```json")

        if inicio == -1 or fim == -1:
            raise ValueError("Delimitadores ```json e ``` não encontrados.")

        json_str = texto[inicio + 7:fim].strip()  # Extrai o JSON puro

        dados = json.loads(json_str)

    linhas = []

    for i, questao in enumerate(dados["Questões"], start=1):
        linhas.append(f"Questão {i}")
        linhas.append(f"Competência Avaliada: {questao['Competência avaliada']}")
        linhas.append(f"Comando: {questao['Comando 1']}")
        linhas.append("Texto de Suporte:")
        linhas.append(questao['Texto suporte'])
        linhas.append("Pergunta:")
        linhas.append(questao['Comando 2'])
        linhas.append("Opções:")

        for letra, opcao in questao['Opções'].items():
            prefixo = "->" if letra == questao['Resposta correta'] else "  "
            linhas.append(f"{prefixo} {letra}) {opcao}")

        linhas.append("Justificativas:")
        for letra, justificativa in questao['Justificativas'].items():
            linhas.append(f"{letra}) {justificativa}")
          

        linhas.append("\n" + "-"*80 + "\n")


    with open(caminho_txt, 'w', encoding='utf-8') as f:
        f.write("\n".join(linhas))




if __name__ == "__main__":
  

    
    # modelos = [
    #     #"gemini-2.0-flash",
    #     "openai/gpt-4.1",
    #     #"openai/o3"
    #     "deepseek/deepseek-chat-v3-0324"
        
    # ]

    # tecnicas = [
    #     {"nome": "baseline", "CoT": False, "Ep": False, "few_shot": False},
    #     # {"nome": "CoT", "CoT": True, "Ep": False, "few_shot": False},
    #     # {"nome": "Ep", "CoT": False, "Ep": True, "few_shot": False},
    #     {"nome": "fewshot", "CoT": False, "Ep": False, "few_shot": True},
    #     {"nome": "CoT_Ep", "CoT": True, "Ep": True, "few_shot": False},
    #     # {"nome": "CoT_fewshot", "CoT": True, "Ep": False, "few_shot": True},
    #     # {"nome": "Ep_fewshot", "CoT": False, "Ep": True, "few_shot": True},
    #     {"nome": "CoT_Ep_fewshot", "CoT": True, "Ep": True, "few_shot": True},
    # ]

    # for modelo in modelos:
    #     # Define o modelo para cada rodada

    #     if modelo == "gemini-2.0-flash":
    #         llm = init_chat_model(modelo, model_provider="google_genai", temperature=0.0, top_p=1.0, verbose=True)
    #     else:
    #         llm = ChatOpenRouter(model_name=modelo, temperature=0.0, top_p=1.0)

        
        
    #     chain = prompt | llm

    #     chat_with_history = RunnableWithMessageHistory(
    #         chain,
    #         get_session_history,
    #         input_messages_key="input",
    #         history_messages_key="history"
    #     )

    #     for tecnica in tecnicas:
    #         for i in range(5):
    #             nome_tecnica = tecnica["nome"]
    #             nome_modelo = modelo.split("/")[-1]
    #             output_path = f"output_SBIE_2025/CL223EFCL2_{nome_modelo}_{nome_tecnica}_suporte_{i}.json"

    #             print(f"\n### Executando com modelo {modelo} e técnica {nome_tecnica} ###\n")

    #             id = nome_modelo + "_" + nome_tecnica

    #             iniciar(
    #                 id_tarefa=6,
    #                 output=output_path,
    #                 session_id=id,
    #                 CoT=tecnica["CoT"],
    #                 Ep=tecnica["Ep"],
    #                 few_shot=tecnica["few_shot"]
    #             )

    #             #transformar_json_em_txt(output_path, f"output_SBIE_2025_TXT/CL223EFCL2_{modelo}_{nome_tecnica}_{i}.txt")
    


    # path = "output_SBIE_2025"

    # arquivos = os.listdir(path)

    # os.makedirs("output_SBIE_2025_TXT", exist_ok=True)


    # for arquivo in arquivos:
    #     try:
    #         transformar_json_em_txt(os.path.join(path,arquivo), os.path.join("output_SBIE_2025_TXT", arquivo.replace(".json", ".txt")))
        
    #     except Exception as e:
    #         print(f"Erro ao processar o arquivo {arquivo}: {e}")
    #         continue


    path = "output_SBIE_2025/CL223EFCL2_gemini-2.0-flash_CoT_Ep_fewshot_suporte_4.json"

    transformar_json_em_txt(path, "output_SBIE_2025_TXT/CL223EFCL2_gemini-2.0-flash_CoT_Ep_fewshot_suporte_4.txt")