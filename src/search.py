import os
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import settings

def get_embeddings():
    if settings.OPENAI_API_KEY:
        return OpenAIEmbeddings(
            model=settings.OPENAI_EMBEDDING_MODEL,
            api_key=settings.OPENAI_API_KEY
        )
    elif settings.GOOGLE_API_KEY:
        return GoogleGenerativeAIEmbeddings(
            model=settings.GOOGLE_EMBEDDING_MODEL,
            google_api_key=settings.GOOGLE_API_KEY
        )
    else:
        raise ValueError("Neither OPENAI_API_KEY nor GOOGLE_API_KEY found in environment.")

def search_documents(query, k=10):
    embeddings = get_embeddings()
    
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=settings.PG_VECTOR_COLLECTION_NAME,
        connection=settings.DATABASE_URL,
        use_jsonb=True,
    )

    return vector_store.similarity_search_with_score(query, k=k)

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(question=None):
    if not question:
        return "Nenhuma pergunta fornecida."
    
    results = search_documents(question)
    contexto = "\n\n".join([doc.page_content for doc, score in results])
    
    return PROMPT_TEMPLATE.format(contexto=contexto, pergunta=question)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(search_prompt(" ".join(sys.argv[1:])))