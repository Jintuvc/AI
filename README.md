# Agentic RAG Chatbot using MCP

A modular, agent-based Retrieval-Augmented Generation (RAG) chatbot system that allows users to upload documents (PDFs, DOCX, PPTX, CSVs, etc.) and ask questions grounded in the uploaded content.
It uses intelligent agents, FAISS for vector search, and OpenAI GPT-3.5 via LangChain to generate accurate and context-aware responses.

## Features
- Upload and parse documents (PDF, DOCX, CSV, PPTX)
- Retrieve relevant chunks using FAISS vector store
- LLM-powered answers via LangChain (GPT-3.5)
- Modular design using custom agents with Model Context Protocol (MCP)
- Streamlit-based user interface
- Chat history and document-aware Q&A

## Installation

1. Clone the Repository
   ``` sh
   git clone https://github.com/Jintuvc/AI.git
   cd AI
   ```
2. Create a Virtual Environment
   ```
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   ````
3. Install Dependencies
   ```
   pip install -r requirements.txt
   ```
4. Set OpenAI API Key
   ```
   Create a .env file in the root directory and add your OpenAI API key:
   OPENAI_API_KEY=your_openai_api_key
   ```
5. Run the App
   ```
   streamlit run main.py
   ```

## How It Works
- Upload Document → Parsed by IngestionAgent
- Embeddings generated and stored in FAISS vector store
- Query Entered → Forwarded to RetrievalAgent
- Relevant Chunks retrieved based on query
- LLMResponseAgent formats context and generates answer
- Response Displayed in UI with source snippets

## Tech Stack
- Python
- LangChain + OpenAI (GPT-3.5)
- FAISS (Vector Search)
- Streamlit (UI)
- PyMuPDF, python-docx, python-pptx, pandas (for document parsing)
