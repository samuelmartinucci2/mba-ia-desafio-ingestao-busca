import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from search import search_prompt
from config import settings

def get_llm():
    if settings.OPENAI_API_KEY:
        return ChatOpenAI(
            model=settings.OPENAI_CHAT_MODEL,
            api_key=settings.OPENAI_API_KEY
        )
    elif settings.GOOGLE_API_KEY:
        return ChatGoogleGenerativeAI(
            model=settings.GOOGLE_CHAT_MODEL,
            google_api_key=settings.GOOGLE_API_KEY
        )
    else:
        raise ValueError("Neither OPENAI_API_KEY nor GOOGLE_API_KEY found in environment.")

def main():
    try:
        llm = get_llm()
        print("\n--- Chat RAG Iniciado (digite 'sair' para encerrar) ---")
        
        while True:
            pergunta = input("\nVocê: ")
            if pergunta.lower() in ["sair", "exit", "quit"]:
                break
            
            if not pergunta.strip():
                continue

            prompt = search_prompt(pergunta)
            
            print("Processando...", end="\r")
            try:
                response = llm.invoke(prompt)
                print(f"IA: {response.content}")
            except Exception as e:
                print(f"\nErro ao chamar a LLM: {e}")
                
    except Exception as e:
        print(f"Erro de inicialização: {e}")

if __name__ == "__main__":
    main()