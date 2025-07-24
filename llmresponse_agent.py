import os
import time
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from mcp import MCPMessage, mcp_queue

load_dotenv()

class LLMResponseAgent:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found")
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=api_key)

    def create_prompt(self, query, context_chunks):
        context_text = "\n".join([chunk.page_content for chunk in context_chunks])
        prompt = f"Answer the question using the context below:\n\nContext:\n{context_text}\n\nQuestion: {query}"
        return prompt

    def get_answer(self, query, context_chunks):
        prompt = self.create_prompt(query, context_chunks)
        response = self.llm.predict(prompt)
        return response

    def run(self):
        while True:
            try:
                msg = mcp_queue.get(timeout=1)
                if msg.receiver == "LLMResponseAgent" and msg.type == "LLM_GENERATE_RESPONSE":
                    query = msg.payload.get("query")
                    context_chunks = msg.payload.get("context_chunks")

                    # Rebuild Document objects if needed
                    from langchain_core.documents import Document
                    chunks = [Document(**chunk) if isinstance(chunk, dict) else chunk for chunk in context_chunks]

                    final_answer = self.get_answer(query, chunks)

                    final_msg = MCPMessage.create(
                        sender="LLMResponseAgent",
                        receiver="UIAgent",
                        type_="FINAL_RESPONSE",
                        payload={"answer": final_answer}
                    )
                    mcp_queue.put(final_msg)
                else:
                    mcp_queue.put(msg)
            except Exception:
                time.sleep(0.1)
