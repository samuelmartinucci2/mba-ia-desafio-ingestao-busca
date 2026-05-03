# Desafio MBA Engenharia de Software com IA - Full Cycle

Este projeto implementa uma solução de ingestão e busca de documentos PDF utilizando LangChain, pgVector e PostgreSQL.

## Pré-requisitos

Para executar este projeto, você precisará das seguintes ferramentas instaladas:

- **Python 3.13+** (Recomendado utilizar [pyenv](https://github.com/pyenv/pyenv))
- **Docker** (v20.10+) e **Docker Compose** (v2.20+)
- **Chave de API**: [OpenAI](https://platform.openai.com/) ou [Google Gemini](https://aistudio.google.com/)

## Configuração do Ambiente

1. **Python**:
   Certifique-se de estar utilizando a versão correta do Python:
   ```bash
   python --version
   ```
   Se não estiver utilizando a versão correta, instale a versão correta do Python e crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Dependências**:
   Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```

4. **Variáveis de Ambiente**:
   Copie o arquivo `.env.example` para `.env`:
   ```bash
   cp .env.example .env
   ```
   Abra o arquivo `.env` e configure as seguintes variáveis:
   - **Chaves de API**: Adicione sua `OPENAI_API_KEY` ou `GOOGLE_API_KEY`.
   - **Configuração do Banco**:
     - `POSTGRES_USER=postgres`
     - `POSTGRES_PASSWORD=sua_senha_segura`
     - `POSTGRES_DB=rag`
     - `PG_VECTOR_COLLECTION_NAME=pdf_chunks`
   - **Modelos e Arquivos**:
     - `GOOGLE_EMBEDDING_MODEL=models/gemini-embedding-001`
     - `GOOGLE_CHAT_MODEL=models/gemini-flash-latest`
     - `PDF_PATH=document.pdf`

> [!TIP]
> Para alterar a senha do banco após a primeira execução, edite o `.env` e reinicie com `docker-compose down -v && docker-compose up -d` para limpar os volumes antigos e aplicar a nova credencial.

5. **Infraestrutura**:
   Suba o banco de dados PostgreSQL com pgVector:
   ```bash
   docker-compose up -d
   ```

## Como Executar

### 1. Ingestão de Dados
Certifique-se de que o banco de dados está rodando (`docker-compose up -d`) e então execute o script para processar o PDF e armazenar os vetores:
```bash
python src/ingest.py
```
*Nota: O script de ingestão agora processa os documentos em pequenos lotes com intervalos de tempo para evitar erros de cota (429) comuns no nível gratuito das APIs.*

### 2. Busca e Chat
Para iniciar o chat interativo no terminal:
```bash
python src/chat.py
```
Para fazer uma pergunta única e sair:
```bash
python src/chat.py "Sua pergunta aqui entre aspas"
```
O chat buscará os 10 fragmentos mais relevantes do PDF para gerar cada resposta.

### 3. Encerrar a Infraestrutura
Para parar os containers do banco de dados:
```bash
docker-compose stop
```
Para remover completamente os containers e os volumes de dados (limpar o banco):
```bash
docker-compose down -v
```
