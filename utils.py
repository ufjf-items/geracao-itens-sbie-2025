import pandas as pd



def get_codigo_da_classe(codigo = 'D01-1EF-CL1'):
    # Lê o CSV (ajuste o caminho e encoding se necessário)
    df = pd.read_csv('matriz_lp.csv', encoding='utf-8-sig')  # 'utf-8-sig' remove o BOM (﻿)

    return df.loc[df['Código da Classe'] == codigo].iloc[0].to_dict()


def get_especificacao_tarefa_exemplo(id = 0):
    # Lê o CSV (ajuste o caminho e encoding se necessário)
    df = pd.read_csv('especificacao_tarefa_exemplo.csv', encoding='utf-8-sig')  # 'utf-8-sig' remove o BOM (﻿)

    return df.loc[df['ID'] == id].iloc[0].to_dict()


def get_variables(id = 0):
    tarefa = get_especificacao_tarefa_exemplo(id)
    classe = get_codigo_da_classe(tarefa['ID_CLASSE'])

    chave_map = {
        "BNCC": "BNCC",
        "classe": "Classes",
        "tipo_de_texto": "Nível de Complexidade do Texto",
        "descritor" : "Descritor"
    }
    for nova, antiga in chave_map.items():
        tarefa[nova] = classe[antiga]

    return tarefa






