

from pathlib import Path

from langchain_classic.chains import RetrievalQA
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS


# 1. TEXTO FIXO: base de conhecimento do sistema
TEXTO = """
Inteligência Artificial (IA) é a capacidade de sistemas computacionais simularem 
o raciocínio, o aprendizado e a tomada de decisões humanos. Em vez de apenas seguir regras 
fixas programadas manualmente, a IA analisa grandes volumes de dados, identifica padrões
e aprende com a experiência para resolver problemas.

"""


def criar_base_vetorial():
    """Divide o texto em chunks, gera embeddings e cria o índice FAISS."""
    documento = Document(
        page_content=TEXTO,
        metadata={"fonte": "texto_definido_no_codigo"},
    )

    separador = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
    )
    chunks = separador.split_documents([documento])

    print(f"\nTexto dividido em {len(chunks)} chunks.")

    # O Ollama gera um vetor para cada chunk.
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # FAISS recebe os documentos, gera os embeddings e cria o índice vetorial.
    banco_vetorial = FAISS.from_documents(chunks, embeddings)

    # Salva o índice localmente para consulta e reutilização.
    pasta_banco = Path("vector_db")
    banco_vetorial.save_local(str(pasta_banco))

    print(f"Banco vetorial FAISS criado e salvo em: {pasta_banco.resolve()}")
    return banco_vetorial


def criar_retrieval_qa(banco_vetorial):
    """Conecta o retriever FAISS ao modelo de linguagem por meio do RetrievalQA."""
    modelo = OllamaLLM(model="llama3.2", temperature=0)

    recuperador = banco_vetorial.as_retriever(
        search_kwargs={"k": 3}
    )

    cadeia_qa = RetrievalQA.from_chain_type(
        llm=modelo,
        chain_type="stuff",
        retriever=recuperador,
        return_source_documents=True,
        chain_type_kwargs={
            "prompt": PromptTemplate(
                input_variables=["context", "question"],
                template=(
                    "Responda à pergunta usando somente as informações "
                    "do contexto abaixo. Se a resposta não estiver no "
                    "contexto, diga que não encontrou essa informação.\n\n"
                    "Contexto:\n{context}\n\n"
                    "Pergunta: {question}\n"
                    "Resposta:"
                ),
            )
        },
    )

    return cadeia_qa


def main():
    print("=" * 60)
    print("SISTEMA RAG COM LANGCHAIN, FAISS E OLLAMA")
    print("=" * 60)

    try:
        banco_vetorial = criar_base_vetorial()
        cadeia_qa = criar_retrieval_qa(banco_vetorial)
    except Exception as erro:
        print("\nNão foi possível iniciar o sistema.")
        print(f"Detalhe: {erro}")
        print(
            "\nVerifique se o Ollama está instalado e em execução e se "
            "os modelos foram baixados:\n"
            "  ollama pull nomic-embed-text\n"
            "  ollama pull llama3.2"
        )
        return

    print("\nSistema pronto! Faça perguntas sobre o texto.")
    print("Digite 'sair' para encerrar.\n")

    while True:
        pergunta = input("Sua pergunta: ").strip()

        if pergunta.lower() in {"sair", "exit", "quit"}:
            print("Sistema encerrado.")
            break

        if not pergunta:
            print("Digite uma pergunta.\n")
            continue

        try:
            resultado = cadeia_qa.invoke({"query": pergunta})
            print(f"\nResposta: {resultado['result']}")

            fontes = resultado.get("source_documents", [])
            if fontes:
                print("\nTrechos recuperados pelo FAISS:")
                for numero, fonte in enumerate(fontes, start=1):
                    trecho = " ".join(fonte.page_content.split())
                    print(f"{numero}. {trecho[:220]}...")

            print("\n" + "-" * 60 + "\n")
        except Exception as erro:
            print(f"\nErro ao consultar o sistema: {erro}\n")


if __name__ == "__main__":
    main()
