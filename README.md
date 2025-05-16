# **utils.py**
* O **utils.py** tem funções para ajudar na criação dos prompts. \

## **get_codigo_da_classe**
**get_codigo_da_classe:** recupera a linha do arquivo de matriz de lingua portuguesa em csv e retorna as informações como um dicionário. \
**INPUT:** Recebe um codigo_da_classe da matriz do CAEd \
**OUTPUT:** e retorna as informações da linha da tabela como um dicionário. 

## **get_especificacao_tarefa_exemplo**
**get_especificacao_tarefa_exemplo:** recupera a linha do arquivo de comandos para geração de item e exmplo em csv e retorna as informações como um dicionário. \
**INPUT:** Id da linha \
**OUTPUT:** e retorna as informações da linha da tabela como um dicionário. 


# **remover_merge_matrix_xlsx_to_csv.py**

## remover_merge_matrix_xlsx_to_csv
* O arquivo **remover_merge_matrix_xlsx_to_csv.py** foi utilizado para auxiliar na conversão do arquivo de matriz que tinha muitas colunas mescladas. Ele basicamente faz com que a linha no arquivo csv não seja mais mesclada, repetindo a informação até achar um próximo valor.\
**INPUT:** Ele recebe como .xlsx, .ods, .csv, etc. \
**OUTPUT:** e retorna um .csv sem o mesclar copiando o de cima pra em baixo