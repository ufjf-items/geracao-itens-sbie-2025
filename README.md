# Projeto

## 📌 Overview
Este projeto tem como objetivo gerar dados para pesquisa em **geração automática de itens**.  
Os itens foram criados a partir de **templates desenvolvidos por especialistas** e com o uso de **técnicas de engenharia de prompt**.  

No momento, contempla apenas **conteúdos de Língua Portuguesa** voltados para habilidades específicas.

---

## 🛠️ Tecnologias e Softwares
- Python  
- LangChain  
- OpenRouter  
- Prompt Engineering  
- IA Generativa
- LLMs (GPT4.1, Gemini 2.5, Deepseek v3)

---

## 🚀 Como instalar

### 1. Clonar o repositório
```bash
git clone link_do_repositorio
cd nome_do_repositorio
```

2. Criar ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. Instalar dependências

```bash
pip install -r requirements.txt
```

4. Configurar variáveis de ambiente

Para executar corretamente, é necessário criar um arquivo `.env` com sua chave de API.

1. Crie um arquivo chamado `.env` na raiz do projeto.
2. Adicione a linha com sua chave da API
  
## Arquivos de interesse

### **utils.py**
* O **utils.py** tem funções para recuperar informações dos aquivos .csv. \

### **app.py**  
* O **app.py** Define o Template do prompt, carrega as variáveis, incializa o modelo de linguagem e executa a geração dos Itens. 
