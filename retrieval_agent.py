# retrieval_agent.py

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from dotenv import load_dotenv
import os

load_dotenv()

class RetrievalAgent:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        self.embedding_model = OpenAIEmbeddings(openai_api_key=api_key)
        self.vectorstore = None

    def prepare_chunks(self, docs):
        all_chunks = []
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        for doc in docs:
            chunks = splitter.split_text(doc["content"])
            for chunk in chunks:
                all_chunks.append(Document(page_content=chunk, metadata={"source": doc["filename"]}))
        return all_chunks

    def index(self, docs):
        chunks = self.prepare_chunks(docs)
        self.vectorstore = FAISS.from_documents(chunks, self.embedding_model)

    def retrieve(self, query, k=3):
        return self.vectorstore.similarity_search(query, k=k)
