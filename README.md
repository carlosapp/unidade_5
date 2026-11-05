# unidade_4
Construção de um Sistema de Recuperação de Informações usando VectorDB e RetrievalQA
# Sistema RAG com FAISS

Projeto acadêmico de recuperação de informações utilizando **Python, LangChain, Ollama, embeddings, FAISS e RetrievalQA**.

O sistema utiliza um texto sobre Inteligência Artificial definido diretamente no código. Esse texto é dividido em pequenos trechos (*chunks*), convertido em embeddings e armazenado em um índice vetorial FAISS. Quando o usuário faz uma pergunta, o sistema recupera os trechos mais semelhantes e utiliza um modelo de linguagem para elaborar a resposta.

## Tecnologias utilizadas

- **Python 3.12**: linguagem de programação.
- **LangChain**: integração das etapas do sistema RAG.
- **Ollama**: execução local dos modelos.
- **nomic-embed-text**: modelo utilizado para gerar embeddings.
- **FAISS**: armazenamento e busca por similaridade entre vetores.
- **llama3.2**: modelo de linguagem utilizado para gerar as respostas.
- **RetrievalQA**: cadeia que combina recuperação de documentos e geração de respostas.

## Estrutura do projeto

```text
sistema-rag-com-faiss/
├── main.py
├── requirements.txt
├── README.md
└── vector_db/          # criado automaticamente na primeira execução
```

## 1. Preparação do ambiente

As instruções abaixo consideram Windows e PowerShell.

### 1.1. Instalar o Python

Instale o **Python 3.12** e confirme a instalação:

```powershell
py -3.12 --version
```

### 1.2. Criar e ativar o ambiente virtual

Abra o terminal na pasta do projeto e execute:

```powershell
py -3.12 -m venv .venv
```

Ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação do ambiente, execute o comando abaixo nessa janela e tente ativar novamente:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 1.3. Atualizar o pip e instalar as dependências

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Instalar e preparar o Ollama

O Ollama executa os modelos localmente. Instale-o pelo site oficial:

https://ollama.com/download

Depois da instalação, abra o terminal e baixe os dois modelos utilizados pelo projeto:

```powershell
ollama pull nomic-embed-text
ollama pull llama3.2
```

Confira se os modelos estão disponíveis:

```powershell
ollama list
```

O Ollama precisa estar em execução durante o uso do sistema. No Windows, normalmente ele fica disponível após iniciar o aplicativo Ollama.

## 3. Executar o projeto

Com o ambiente virtual ativado e o Ollama em execução, execute:

```powershell
python main.py
```

Na primeira execução, o programa:

1. Carrega o texto sobre Inteligência Artificial definido em `main.py`.
2. Divide o texto em chunks de até 500 caracteres, com sobreposição de 80 caracteres.
3. Gera embeddings com o modelo `nomic-embed-text`.
4. Cria o índice vetorial FAISS e salva os dados na pasta `vector_db`.
5. Configura o `RetrievalQA` com o modelo `llama3.2`.
6. Aguarda perguntas digitadas pelo usuário.

Para encerrar, digite:

```text
sair
```

## 4. Exemplos de perguntas

**Pergunta:**

```text
O que é IA
```


As respostas são geradas pelo modelo com base nos trechos recuperados da base de conhecimento. Como o modelo é executado localmente, as respostas podem variar.

## 5. Como o sistema funciona

```text
Texto definido no código
          |
          v
Divisão em chunks
          |
          v
Geração de embeddings
          |
          v
Armazenamento/indexação no FAISS
          |
          v
Pergunta do usuário
          |
          v
Embedding da pergunta e busca por similaridade
          |
          v
Recuperação dos trechos mais relevantes
          |
          v
RetrievalQA + modelo llama3.2
          |
          v
Resposta baseada no contexto recuperado
```

## 6. Parâmetros principais

No arquivo `main.py`:

- `chunk_size=500`: tamanho máximo de cada trecho.
- `chunk_overlap=80`: quantidade de caracteres repetidos entre trechos consecutivos.
- `search_kwargs={"k": 3}`: quantidade de trechos recuperados para cada pergunta.
- `temperature=0`: configuração para respostas menos aleatórias.

## 7. Observações

- O texto de conhecimento está diretamente na variável `TEXTO`, no arquivo `main.py`. Ele pode ser alterado conforme o tema escolhido.
- A pasta `vector_db` é criada automaticamente quando o índice FAISS é salvo.
- Se o texto ou o modelo de embeddings for alterado, execute novamente o programa para reconstruir o índice.
- O projeto utiliza modelos locais do Ollama; por isso, não exige uma chave de API de serviços externos.



Projeto desenvolvido para atividade acadêmica sobre recuperação de informações utilizando VectorDB e RetrievalQA.
