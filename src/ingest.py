import os
import time
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import settings

def get_embeddings():
    if settings.OPENAI_API_KEY:
        print("Using OpenAI Embeddings")
        return OpenAIEmbeddings(
            model=settings.OPENAI_EMBEDDING_MODEL, 
            api_key=settings.OPENAI_API_KEY
        )
    elif settings.GOOGLE_API_KEY:
        print("Using Google Generative AI Embeddings")
        return GoogleGenerativeAIEmbeddings(
            model=settings.GOOGLE_EMBEDDING_MODEL, 
            google_api_key=settings.GOOGLE_API_KEY
        )
    else:
        raise ValueError("Neither OPENAI_API_KEY nor GOOGLE_API_KEY found in environment.")

def ingest_pdf():
    if not os.path.exists(settings.PDF_PATH):
        print(f"Error: PDF file not found at {settings.PDF_PATH}")
        return

    print(f"Starting ingestion for: {settings.PDF_PATH}")
    loader = PyPDFLoader(settings.PDF_PATH)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from {settings.PDF_PATH}")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")

    try:
        embeddings = get_embeddings()
        
        vector_store = PGVector(
            embeddings=embeddings,
            collection_name=settings.PG_VECTOR_COLLECTION_NAME,
            connection=settings.DATABASE_URL,
            use_jsonb=True,
        )

        print(f"Adding {len(chunks)} chunks to pgVector (database: {settings.DATABASE_URL}, collection: {settings.PG_VECTOR_COLLECTION_NAME})...")
        
        batch_size = 5
        delay = 10
        
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            vector_store.add_documents(batch)
            print(f"Progress: {min(i + batch_size, len(chunks))}/{len(chunks)} chunks added.")
            
            if i + batch_size < len(chunks):
                print(f"Waiting {delay} seconds to avoid rate limits...")
                time.sleep(delay)
                
        print("Successfully ingested all chunks into the database.")
        
    except Exception as e:
        print(f"An error occurred during ingestion: {e}")

if __name__ == "__main__":
    ingest_pdf()