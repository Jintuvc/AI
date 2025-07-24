#🤖 Agentic RAG Chatbot using MCP

A modular, agent-based Retrieval-Augmented Generation (RAG) chatbot system that allows users to upload documents (PDFs, DOCX, PPTX, CSVs, etc.) and ask questions grounded in the uploaded content.
It uses intelligent agents, FAISS for vector search, and OpenAI GPT-3.5 via LangChain to generate accurate and context-aware responses.

##Features
1.Upload and parse documents (PDF, DOCX, CSV, PPTX)
2.Retrieve relevant chunks using FAISS vector store
3.LLM-powered answers via LangChain (GPT-3.5)
4.Modular design using custom agents with Model Context Protocol (MCP)
5.Streamlit-based user interface
6.Chat history and document-aware Q&A

##⚙️ Setup Instructions
1. Clone the Repository
git clone https://github.com/Jintuvc/rag.git
cd rag
2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Set OpenAI API Key
Create a .env file in the root directory and add your OpenAI API key:
OPENAI_API_KEY=your_openai_api_key_here
5. Run the App
streamlit run main.py

##🧠 How It Works
1.Upload Document → Parsed by IngestionAgent
2.Embeddings generated and stored in FAISS vector store
3.Query Entered → Forwarded to RetrievalAgent
4.Relevant Chunks retrieved based on query
5.LLMResponseAgent formats context and generates answer
6.Response Displayed in UI with source snippets

##📌 Tech Stack
1.Python
2.LangChain + OpenAI (GPT-3.5)
3.FAISS (Vector Search)
4.Streamlit (UI)
5.PyMuPDF, python-docx, python-pptx, pandas (for document parsing)


